# This was kindly provided by Max Rakitin and Dmitri Gavrilov

import datetime
from ophyd import Device, Component, Signal, DeviceStatus, EpicsSignal, EpicsSignalRO, Kind
from ophyd.areadetector.filestore_mixins import resource_factory
from ophyd.sim import new_uid
from ophyd.status import SubscriptionStatus
from collections import deque
from event_model import compose_resource
from pathlib import Path
import numpy
from PIL import Image

import bmm_tools.tools.md       # obtain a profile's value for RE, RE.md
md = bmm_tools.tools.md.common_md


class ExternalFileReference(Signal):
    """
    A pure software Signal that describe()s an image in an external file.
    """

    def describe(self):
        resource_document_data = super().describe()
        resource_document_data[self.name].update(
            {
                "external": "FILESTORE:",
                "dtype": "array",
            }
        )
        return resource_document_data

class BMM_JPEG_HANDLER:
    def __init__(self, resource_path):
        # resource_path is really a template string with a %d in it
        self._template = resource_path

    def __call__(self, index):
        filepath = self._template % index
        return numpy.asarray(Image.open(filepath))

    
class AxisCaprotoCam(Device):
    '''Simple ophyd class for capturing an Axis Web camera
    '''
    write_dir = Component(EpicsSignal, "write_dir", string=True)
    file_name = Component(EpicsSignal, "file_name", string=True)
    full_file_path = Component(EpicsSignalRO, "full_file_path", string=True)
    ioc_stage = Component(EpicsSignal, "stage", string=True)
    acquire = Component(EpicsSignal, "acquire", string=True)

    image = Component(ExternalFileReference, kind=Kind.normal)

    def __init__(self, *args, root_dir=None, **kwargs):
        super().__init__(*args, **kwargs)
        if root_dir is None:
            msg = "The 'root_dir' kwarg cannot be None"
            raise RuntimeError(msg)
        self._root_dir = root_dir
        self._resource_document, self._datum_factory = None, None
        self._asset_docs_cache = deque()

    def _update_paths(self):
        self._root_dir = self.root_path_str

    @property
    def root_path_str(self):
        root_path = f"/nsls2/data3/bmm/proposals/{md['cycle']}/{md['data_session']}/assets/"
        return root_path


    def collect_asset_docs(self):
        """The method to collect resource/datum documents."""
        items = list(self._asset_docs_cache)
        self._asset_docs_cache.clear()
        yield from items

    def stage(self):
        self._update_paths()
        super().stage()

        # Clear asset docs cache which may have some documents from the previous failed run.
        self._asset_docs_cache.clear()

        assets_dir = self.name + datetime.datetime.now().strftime('/%Y/%m/%d')
        data_file_no_ext = f"{self.name}_{new_uid()}"
        data_file_with_ext = f"{data_file_no_ext}.jpeg"

        self._resource_document, self._datum_factory, _ = compose_resource(
            start={"uid": "needed for compose_resource() but will be discarded"},
            spec="BMM_JPEG_HANDLER",
            root=self._root_dir,
            resource_path=str(Path(assets_dir) / Path(data_file_with_ext)),
            resource_kwargs={},
        )

        # now discard the start uid, a real one will be added later
        self._resource_document.pop("run_start")
        self._asset_docs_cache.append(("resource", self._resource_document))

        # Update caproto IOC parameters:
        self.write_dir.put(str(Path(self._root_dir) / Path(assets_dir)))
        self.file_name.put(data_file_with_ext)
        self.ioc_stage.put(1)

    def describe(self):
        res = super().describe()
        res[self.image.name].update(
            {"shape": (1080, 1920), "dtype_str": "<f4"}
        )
        return res

    def trigger(self):

        def done_callback(value, old_value, **kwargs):
            """The callback function used by ophyd's SubscriptionStatus."""
            # print(f"{old_value = } -> {value = }")
            if old_value == "acquiring" and value == "idle":
                return True
            return False

        status = SubscriptionStatus(self.acquire, run=False, callback=done_callback)

        # Reuse the counter from the caproto IOC
        self.acquire.put(1)

        datum_document = self._datum_factory(datum_kwargs={})
        self._asset_docs_cache.append(("datum", datum_document))

        self.image.put(datum_document["datum_id"])

        return status

    def unstage(self):
        self._resource_document = None
        self._datum_factory = None
        self.ioc_stage.put(0)
        super().unstage()


# axis_cam5 = AxisCaprotoCam("XF:06BM-ES{AxisCaproto:5}:", name="webcam-2",
#                            root_dir="/nsls2/data3/bmm/proposals/2024-2/pass-301027/assets")
# axis_cam6 = AxisCaprotoCam("XF:06BM-ES{AxisCaproto:6}:", name="webcam-1",
#                            root_dir="/nsls2/data3/bmm/proposals/2024-2/pass-301027/assets")

# def acquire_axis(cam=axis_cam5, write_dir=f"/nsls2/data3/bmm/proposals/{md['cycle']}/{md['data_session']}/assets/default/"):
#     cam.write_dir.put(write_dir)
#     cam.file_name.put(f"{cam.name}_{uuid.uuid4()}.jpeg")

#     cam.ioc_stage.put(0)
#     cam.ioc_stage.put(1)

#     cam.acquire.put(1)
    
#     print(cam.full_file_path.get())

