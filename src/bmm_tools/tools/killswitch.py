from ophyd import (EpicsMotor, PseudoPositioner, PseudoSingle, Component as Cpt, EpicsSignal, EpicsSignalRO, Device)
from bluesky.plan_stubs import sleep, mv, null

import time

from bmm_tools.tools.messages import *  # error_msg et al. + boxedtext


class KillSwitch(Device):
    '''A simple interface to the DIODE kill switches for the Phytron
    amplifiers on the FMBO Delta Tau motor controllers.

    In BMM's DIODE box, these are implemented on channels 0 to 4 of
    slot 4.

    attributes
    ----------
    dcm 
       kill switch for MC02, monochromator
    slits2
       kill switch for MC03, DM2 slits
    m2
       kill switch for MC04, focusing mirror
    m3
       kill switch for MC05, harmonic rejection mirror
    dm3
       kill switch for MC06, hutch slits and diagnostics

    dcm_device
       set to the instance of bmm_tools.devices.dcm.DCM
    slits2_device
       set to the instance of bmm_tools.devices.slits.StandardSlits for the post mono slits
    slits3_device
       set to the instance of bmm_tools.devices.slits.StandardSlits for the hutch slits
    m2_device
       set to the instance of bmm_tools.devices.motors.Mirrors for the focusing mirror
    m3_device
       set to the instance of bmm_tools.devices.motors.Mirrors for the harmonic rejection mirror
    dm3_axes : list of XAFSEpicsMotor
       set to the XAFSEpicsMotor instances of dm3_bct (and, if defined, dm3_bpm, dm3_foils, dm3_fs)

    The device attributes must be set immediately upon instantiation
    of the killswitch instance.


    methods
    -------
    kill(mc)
       disable Phytron
    enable(mc)
       activate Phytron
    cycle(mc)
       disable, wait 5 seconds, reactivate, then re-enable all motors

    Specify the motor controller as a string, i.e. 'dcm', 'slits2',
    'm2', 'm3', 'dm3'

    Here's a common problem which is resolved using a kill switch.

      BMM E.111 [36] ▶ RE(mvr(m2.pitch, 0.05))
      INFO:BMM_logger:    Moving m2_pitch to 2.550

      Moving m2_pitch to 2.550
      ERROR:ophyd.objects:Motion failed: m2_yu is in an alarm state status=AlarmStatus.STATE severity=AlarmSeverity.MAJOR
      ERROR:ophyd.objects:Motion failed: m2_yu is in an alarm state status=AlarmStatus.STATE severity=AlarmSeverity.MAJOR
      ERROR:ophyd.objects:Motion failed: m2_ydi is in an alarm state status=AlarmStatus.STATE severity=AlarmSeverity.MAJOR
      ERROR:ophyd.objects:Motion failed: m2_ydi is in an alarm state status=AlarmStatus.STATE severity=AlarmSeverity.MAJOR
      Out[36]: ()

    This is telling you that the amplifiers for two of the M2 jacks
    went into an alarm state. In the vast majority of cases, this
    simply requires killing and reactivating those amplifiers.

    The solution to this one is:

      BMM E.111 [1] ▶ ks.cycle('m2')
      Cycling amplifiers on m2 motor controller
      killing amplifiers
      reactivating amplifiers
      enabling motors

    '''
    dcm    = Cpt(EpicsSignal, 'OutPt00:Data-Sel')
    slits2 = Cpt(EpicsSignal, 'OutPt01:Data-Sel')
    m2     = Cpt(EpicsSignal, 'OutPt02:Data-Sel')
    m3     = Cpt(EpicsSignal, 'OutPt03:Data-Sel')
    dm3    = Cpt(EpicsSignal, 'OutPt04:Data-Sel')

    dcm_device    = None
    slits2_device = None
    slits3_device = None
    m2_device     = None
    m3_device     = None
    dm3_axes      = ()

    def check(self, mc):
        '''Verify the string identifying the motor controller.

        Identify the motor controller by these strings:
           'dcm', 'slits2', 'm2', 'm3', 'dm3'
        '''
        if mc is None:
            error_msg("Specify a device: ks.kill(device), device is dcm/slits2/m2/m3/dm3")
            return False
        if mc.lower() not in ('dcm', 'slits2', 'm2', 'm3', 'dm3'):
            error_msg("Specify a device: ks.kill(device), device is dcm/slits2/m2/m3/dm3")
            return False
        return True
        

    def kill(self, mc=None):
        '''Kill the amplifiers on a motor controller.

        Identify the motor controller by these strings:
           'dcm', 'slits2', 'm2', 'm3', 'dm3'
        '''
        if self.check(mc) is False:
            return
        switch = getattr(self, mc)
        switch.put(1)

    def enable(self, mc=None):
        '''Reactivate the amplifiers on a motor controller.

        Identify the motor controller by these strings:
           'dcm', 'slits2', 'm2', 'm3', 'dm3'
        '''
        if self.check(mc) is False:
            return
        switch = getattr(self, mc)
        switch.put(0)

    def allon(self):
        for mc in ('dcm', 'slits2', 'm2', 'm3', 'dm3'):
            self.enable(mc)
        
    def alloff(self):
        for mc in ('dcm', 'slits2', 'm2', 'm3', 'dm3'):
            self.kill(mc)

    def checkall(self):
        ok = True
        for mc in ('dcm', 'slits2', 'm2', 'm3', 'dm3'):
            switch = getattr(self, mc)
            if switch.get() == 1:
                disconnected_msg(f'{mc} controller is disabled')
                ok = False
        return(ok)

    def cycle(self, mc=None):
        '''Cycle power to the amplifiers on a motor controller, then reenable
        the motors on that controller.

        Identify the motor controller by these strings:
           'dcm', 'slits2', 'm2', 'm3', 'dm3'

        '''
        if self.check(mc) is False:
            return
        bold_msg(f'Cycling amplifiers on {mc} motor controller')
        whisper('killing amplifiers')
        self.kill(mc)
        countdown(5)
        whisper('reactivating amplifiers')
        self.enable(mc)
        whisper('enabling motors')
        if mc == 'm2':
            self.m2_device.ena()
        elif mc == 'm3':
            self.m3_device.ena()
        elif mc == 'slits2':
            self.slits2_device.enable()
        elif mc == 'dm3':
            self.slits3_device.enable()
            for axis in self.dm3_axes:
                try:
                    axis.enable()
                    time.sleep(0.5)
                    axis.kill()
                except:
                    pass
        elif mc == dcm:
            self.dcm_device.ena()
            time.sleep(0.5)
            self.dcm_device.kill()
            
