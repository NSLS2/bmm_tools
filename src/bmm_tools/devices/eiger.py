'''AreaDetector interface to the Eiger, customized for use at BMM.
'''    

from pathlib import PurePath
from itertools import count
from collections import deque, OrderedDict
import time as ttime
from tqdm import tqdm

from ophyd import EpicsSignal, EpicsSignalRO, EpicsSignalWithRBV
from ophyd.areadetector import AreaDetector, ImagePlugin
from ophyd.areadetector.cam import PilatusDetectorCam
from ophyd.areadetector.base import EpicsSignalWithRBV
from ophyd.areadetector.filestore_mixins import resource_factory, FileStoreHDF5, FileStoreTIFF, FileStoreIterativeWrite, FileStorePluginBase
from ophyd.areadetector.plugins import HDF5Plugin_V33, TIFFPlugin_V33, StatsPlugin_V33, ROIStatPlugin, ROIStatNPlugin, ROIPlugin, StatsPlugin

# from BMM import user_ns as user_ns_module
# user_ns = vars(user_ns_module)
# md = user_ns["RE"].md
import bmm_tools.tools.md       # obtain a profile's value for RE.md
md = bmm_tools.tools.md.common_md

from nslsii.ad33 import SingleTriggerV33
from ophyd import Component as C

#from BMM.user_ns.base import PROPOSALS
PROPOSALS = '/nsls2/data/bmm/proposals'

from bmm_tools.tools.messages  import *  # error_msg et al. + boxedtext
from bmm_tools.devices.pilatus import BMMFileStoreHDF5, BMMHDF5Plugin

class BMMEiger(AreaDetector):
    #image = C(ImagePlugin, "image1:")
    hdf5 = C(
        BMMHDF5Plugin,
        "HDF1:",
        write_path_template=f"{PROPOSALS}/{md['cycle']}/{md['data_session']}/assets/eiger1m-1/%Y/%m/%d/",
        read_path_template=f"{PROPOSALS}/{md['cycle']}/{md['data_session']}/assets/eiger1m-1//%Y/%m/%d/",
        read_attrs=[],
        root=f"{PROPOSALS}/{md['cycle']}/{md['data_session']}/assets/eiger1m-1/",
    )
    #roistat = C(ROIStatPlugin, "roistat",)

    
    roi1 = C(ROIPlugin, "ROI1:", name = 'roi1')
    roi2 = C(ROIPlugin, "ROI2:", name = 'roi2')
    roi3 = C(ROIPlugin, "ROI3:", name = 'roi3')
    roi4 = C(ROIPlugin, "ROI4:", name = 'roi4')
    stats1 = C(StatsPlugin, "Stats1:", name="stats1")
    stats2 = C(StatsPlugin, "Stats2:", name="stats2")
    stats3 = C(StatsPlugin, "Stats3:", name="stats3")
    stats4 = C(StatsPlugin, "Stats4:", name="stats4")


    
    signed_data        = C(EpicsSignalWithRBV, 'cam1:SignedData')
    
    # cam_file_path      = C(EpicsSignalWithRBV, 'cam1:FilePath')
    # cam_file_name      = C(EpicsSignalWithRBV, 'cam1:FileName')
    # cam_file_number    = C(EpicsSignalWithRBV, 'cam1:FileNumber')
    # cam_auto_increment = C(EpicsSignalWithRBV, 'cam1:AutoIncrement')
    # cam_file_template  = C(EpicsSignalWithRBV, 'cam1:FileTemplate')
    # cam_full_file_name = C(EpicsSignalRO,      'cam1:FullFileName_RBV')
    # cam_file_format    = C(EpicsSignalWithRBV, 'cam1:FileFormat')

    threshold_energy   = C(EpicsSignalWithRBV, 'cam1:ThresholdEnergy')
    threshold2_energy  = C(EpicsSignalWithRBV, 'cam1:Threshold2Energy')
    photon_energy      = C(EpicsSignalWithRBV, 'cam1:PhotonEnergy')

    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        #self.stage_sigs.update([(self.cam.trigger_mode, "Internal Server")])

        ## tie Stats1 to ROI1 and so on
        self.stats1.nd_array_port.put('ROI1')
        self.stats2.nd_array_port.put('ROI2')
        self.stats3.nd_array_port.put('ROI3')
        self.stats4.nd_array_port.put('ROI4')

    def make_data_key(self):
        source = "PV:{}".format(self.prefix)
        # This shape is expected to match arr.shape for the array.
        shape = (
            1,
            self.cam.array_size.array_size_y.get(),
            self.cam.array_size.array_size_x.get(),
        )
        
        data_key = dict(
            shape=shape,
            source=source,
            dtype="array",
            dtype_str="<f4",
            external="FILESTORE:",
        )
        #print(data_key)
        return data_key

    def set_signed_data(self, signed=True):
        '''Set the SignedData flag.

        True means to used signed data.  This will make the dynamic
        range 2^31.  It will also make the signal in the inter-pane
        pixels -1.  Noise will likely be in the single-digit scale.

        False means to use unsigned data.  This gives a range of 2^32,
        but means that the inter-pane pixels will have values of 2^32-1.

        '''
        if signed is True:
            self.signed_data.put(1)
        else:
            self.signed_data.put(0)

    def _interpret_roi(self, which):
        '''Return the pointer to the correct Eiger ROI attribute given aa
        string that can be interpreted to indicate one or ROI1 through 4.
        '''
        stwhich = str(which).lower()
        if stwhich in ('roi1', '1'):
            roi = self.roi1
        elif stwhich in ('roi2', '2'):
            roi = self.roi2
        elif stwhich in ('roi3', '3'):
            roi = self.roi3
        elif stwhich in ('roi4', '4'):
            roi = self.roi4
        else:
            print(f"{which} cannot be interpreted as an ROI (acceptable values: roi1, roi2, roi3, roi4)")
            return None
        return roi
            
    def set_rois(self, which, values):
        '''Set an ROI boundary given a list or tuple of min_x, size_x, min_y, size_y

        arguments
        =========
        which: str or integer
          identify the roi, must be one of roi1, roi2, roi3, or roi4 (or just the integer)

        values: list or tuple
          min_x, size_x, min_y, size_y
        '''
        mx, sx, my, sy = values # .split()
        roi = self._interpret_roi(which)
        if roi is None:
            return
        roi.min_xyz.min_x.put(mx)
        roi.size.x.put(sx)
        roi.min_xyz.min_y.put(my)
        roi.size.y.put(sy)
            
    def get_rois(self, which):
        '''Get an ROI boundary tuple.  Also prints a message to the screen
        about the ROI boundaries.

        argument
        ========
        which: str or integer
          identify the roi, must be one of roi1, roi2, roi3, or roi4 (or just the integer)

        returns
        =======
        tuple of (min_x, size_x, min_y, size_y)

        '''
        roi = self._interpret_roi(which)
        if roi is None:
            return
        mx, sx, my, sy = (roi.min_xyz.min_x.get(),
                          roi.size.x.get(),
                          roi.min_xyz.min_y.get(),
                          roi.size.y.get())
        print(f'{roi.name[-4:].upper()}: {mx} {sx} {my} {sy}')
        return (mx, sx, my, sy)

class BMMEigerSingleTrigger(SingleTriggerV33, BMMEiger):
    '''AreaDetector interface to the Eiger, customized for use at BMM.
    '''
    pass


