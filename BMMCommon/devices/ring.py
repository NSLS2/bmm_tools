
from ophyd import Component as Cpt
from ophyd import EpicsSignal, EpicsSignalRO, EpicsSignalWithRBV, Signal, Device

class Ring(Device):
    current    = Cpt(EpicsSignalRO, ':OPS-BI{DCCT:1}I:Real-I')
    lifetime   = Cpt(EpicsSignalRO, ':OPS-BI{DCCT:1}Lifetime-I')
    energy     = Cpt(EpicsSignalRO, '{}Energy_SRBend')
    mode       = Cpt(EpicsSignalRO, '-OPS{}Mode-Sts', string=True)
    filltarget = Cpt(EpicsSignalRO, '-HLA{}FillPattern:DesireImA')
