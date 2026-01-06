from ophyd import Component as Cpt
from ophyd import EpicsSignalRO, Device

class FEBPM(Device):
    x = Cpt(EpicsSignalRO, 'X-I')
    y = Cpt(EpicsSignalRO, 'Y-I')


    
