import os, re
import numpy
import matplotlib.pyplot as plt
from rich import print as cprint

bmm_catalog = None

def file_resource(record):
    '''Return the fully resolved path to the data resource associated with
    the record, e.g.

    - the filestore image collected by a BMMSnapshot device 
    - the HDF5 file associated with an XRF measurement or a 
      fluorescence XAFS scan

    Argument is either a uid string or Tiled catalog.

    Anything that cannot be interpreted to return a path will return None.
    global bmm_catalog

    This intends to work with "BlueskyRun v2.0" (Mongo backed) and
    "BlueskyRun v3.0 streams" (SQL backed)

    '''
    
    if bmm_catalog is None:
        cprint('[red1]You have not set bmm_tools.tools.db.bmm_catalog[/red1]')
        return(None)
    if type(record) is str:
        try:
            record = bmm_catalog[record]
        except:
            return(None)

    docs = record.documents()
    found = []
    for d in docs:
        if d[0] == 'resource':
            rp = d[1]['resource_path']
            if not rp.startswith('/nsls2'):
                rp = d[1]['root'] + d[1]['resource_path']
            if '_%d' in rp or re.search(r'%\d\.\dd', rp) is not None:
                this = rp % 0
                found.append(this)
            else:
                found.append(rp)
    return(found)



def file_resource_old_version(record):
    '''Return the fully resolved path to the data resource associated with
    the record, e.g.

    - the filestore image collected by a BMMSnapshot device 
    - the HDF5 file associated with an XRF measurement or a 
      fluorescence XAFS scan

    Argument is either a uid string or Tiled catalog.

    Anything that cannot be interpreted to return a path will return None.

    This is trying to resolve things for multiple generations of file storage.

    configuration
    =============
    Need to push the symbol for the Tiled catalog to this module

      import bmm_tools.tools.db
      bmm_tools.tools.db.bmm_catalog = bmm_catalog
      file_resource = bmm_tools.tools.db.file_resource


    '''
    global bmm_catalog
    if bmm_catalog is None:
        cprint('[red1]You have not set bmm_tools.tools.db.bmm_catalog[/red1]')
        return(None)
    if type(record) is str:
        try:
            record = bmm_catalog[record]
        except:
            return(None)
    if 'databroker.core.BlueskyRunFromGenerator' in str(type(record)) :
        #template = os.path.join(record.describe()['args']['get_resources']()[0]['root'],
        #                        record.describe()['args']['get_resources']()[0]['resource_path'])
        #return(template % 0)
        return(None)
    elif 'databroker.core.BlueskyRun' in str(type(record)) :
        template = os.path.join(record.describe()['args']['get_resources']()[0]['root'],
                                record.describe()['args']['get_resources']()[0]['resource_path'])
        try:
            return(template % 0)
        except:
            return(template)
    elif 'databroker.client.BlueskyRun' in str(type(record)):
        docs = record.documents()
        found = []
        for d in docs:
            if d[0] == 'resource':
                this = os.path.join(d[1]['root'], d[1]['resource_path'])
                if '_%d' in this or re.search(r'%\d\.\dd', this) is not None:
                    this = this % 0
                found.append(this)
        return(found)
    elif 'bluesky_tiled_plugins.bluesky_run.BlueskyRun' in str(type(record)):
        docs = record.documents()
        found = []
        for d in docs:
            if d[0] == 'resource':
                rp = d[1]['resource_path']
                if '_%d' in rp or re.search(r'%\d\.\dd', rp) is not None:
                    this = rp % 0
                found.append(rp)
        return(found)
        
    else:
        return(None)

def show_snapshot(record):
    '''Quickly plot a snapshot image from DataBroker given its UID.
    '''
    global bmm_catalog    
    if bmm_catalog is None:
        cprint('[red1]You have not set bmm_tools.tools.db.bmm_catalog[/red1]')
        return(None)
    if type(record) is str:
        try:
            record = bmm_catalog[record]
        except:
            return(None)

    if 'BlueskyRunV2Mongo' in str(type(record)):
        d = 'data/'
    else:                       # V3, SQL
        d = ''
        
    thing = ''
    for x in ('cam-8_image', 'cam-9_image', 'cam-7_image',
              'usbcam-1_image', 'usbcam-5_image', 'usbcam-6_image', 'usbcam-2_image',
              'webcam-1_image', 'webcam-2_image'):
        if f'primary/{d}{x}' in record:
            thing = f'primary/{d}{x}'

    if 'webcam' in thing:
        cprint('[grey42]Cannot show webcam images in this way at this time.[/grey42]')
        cprint('[grey42]Here is the file location:[/grey42]')
        cprint(f'[grey42]\t{file_resource(record)}[/grey42]')
        return
    if thing == '':
        print('No image found...')
        return
    
    print(f'Showing {file_resource(record)}')
    plt.imshow(record[thing][0,:])
    plt.grid(False)
        
    
    # if 'usbcam-1_image' in bmm_catalog[uid]['primary']['data']:
    #     plt.imshow(bmm_catalog[uid]['primary']['data']['usbcam-1_image'][0,:])
    # elif 'usbcam-2_image' in bmm_catalog[uid]['primary']['data']:
    #     plt.imshow(bmm_catalog[uid]['primary']['data']['usbcam-2_image'][0,:])        
    # elif 'usbcam-5_image' in bmm_catalog[uid]['primary']['data']:
    #     plt.imshow(bmm_catalog[uid]['primary']['data']['usbcam-2_image'][0,:])        
    # elif 'usbcam-6_image' in bmm_catalog[uid]['primary']['data']:
    #     plt.imshow(bmm_catalog[uid]['primary']['data']['usbcam-2_image'][0,:])        
    # elif 'webcam-1_image' in bmm_catalog[uid]['primary']['data']:
    #     plt.imshow(bmm_catalog[uid]['primary']['data']['webcam-1_image'][0,:])        
    # elif 'webcam-2_image' in bmm_catalog[uid]['primary']['data']:
    #     plt.imshow(bmm_catalog[uid]['primary']['data']['webcam-2_image'][0,:])        
    # else:                       # pre-data-security
    #     this = bmm_catalog[uid].primary.read()
    #     if 'usbcam1_image' in this:
    #         key = 'usbcam1_image'
    #     elif 'usbcam2_image' in this:
    #         key = 'usbcam2_image'
    #     elif 'usbcam5_image' in this:
    #         key = 'usbcam5_image'
    #     elif 'usbcam6_image' in this:
    #         key = 'usbcam6_image'
    #     elif 'xascam_image' in this:
    #         key = 'xascam_image'
    #     elif 'anacam_image' in this:
    #         key = 'anacam_image'
    #     plt.imshow(numpy.array(this[key])[0])


def full_path(uid):
    global bmm_catalog
    if bmm_catalog is None:
        cprint('[red1]You have not set bmm_tools.tools.db.bmm_catalog[/red1]')
        return(None)
    if type(uid) is str:
        try:
            record = bmm_catalog[uid]
        except:
            return(None)

    fp = os.path.join('/nsls2/data/bmm/proposals',
                      record.metadata['start']['cycle'],
                      f"pass-{record.metadata['start']['proposal']['proposal_id']}",
                      'assets',
                      file_resource(uid)[0]
    )
    return fp
