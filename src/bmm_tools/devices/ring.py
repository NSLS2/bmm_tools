
from ophyd import Component as Cpt
from ophyd import EpicsSignal, EpicsSignalRO, EpicsSignalWithRBV, Signal, Device

from BMMCommon.tools.messages import *  # error_msg et al. + boxedtext


class Ring(Device):
    current    = Cpt(EpicsSignalRO, ':OPS-BI{DCCT:1}I:Real-I')
    lifetime   = Cpt(EpicsSignalRO, ':OPS-BI{DCCT:1}Lifetime-I')
    energy     = Cpt(EpicsSignalRO, '{}Energy_SRBend')
    mode       = Cpt(EpicsSignalRO, '-OPS{}Mode-Sts', string=True)
    filltarget = Cpt(EpicsSignalRO, '-HLA{}FillPattern:DesireImA')

    def where(self):
        text  = f'current        = {self.current.get():.1f} mA\n'
        text += f'fill target    = {self.filltarget.get():.1f} mA\n'
        text += f'energy         = {self.energy.get():.1f} GeV\n'
        text += f'lifetime       = {self.lifetime.get():.1f} hr\n'
        text += f'operating mode = {self.mode.get()}'
        return '[white]' + text + '[/white]'

    def wh(self):
        boxedtext(self.where(), title='Storage Ring', color='yellow')
    
