from bluesky.suspenders import SuspendFloor, SuspendBoolHigh, SuspendBoolLow
from bluesky.plan_stubs import null

import uuid
from rich import print as cprint

from bmm_tools.tools.messages import bold_msg, error_msg, warning_msg, whisper
from bmm_tools.tools.animated_prompt import PROMPTNC, animated_prompt

TAB = '\t\t\t\t'

class BMMSuspenders():
    def __init__(self, *args, **kwargs):
        #print(kwargs)
        self.re   = kwargs['re']
        
        #self.idps = kwargs['idps']
        self.bmps  = kwargs['bmps']
        self.sha   = kwargs['sha']
        self.shb   = kwargs['shb']
        self.ring  = kwargs['ring']
        self.kafka = kwargs['kafka']

        self.all_suspenders = list()

        self.suspender_ring_current = None
        self.suspender_bmps = None

        self.suspenders_engaged = False
        self.busy = False
        
        try:
            if self.ring.filltarget.connected is True and self.ring.filltarget.get() > 20:
                self.suspender_ring_current = SuspendFloor(self.ring.current, 10, resume_thresh=0.9 * ring.filltarget.get(),
                                                           sleep=60,
                                                           pre_plan=self.beamdown_message,
                                                           post_plan=self.beamup_message)
                self.all_suspenders.append(self.suspender_ring_current)
        except Exception as e:
            cprint(f'[orange_red1]{TAB}failed to create ring current suspender: {e}[/orange_red1]')
            pass

        
        try:
            self.suspender_bmps = SuspendBoolLow(self.bmps.state, sleep=60)
            self.all_suspenders.append(self.suspender_bmps)
        except Exception as e:
            cprint(f'[orange_red1]{TAB}failed to create bpms suspender:[/orange_red1] {e}')
            pass

        try:
            self.suspender_sha = SuspendBoolLow(self.sha.state, sleep=60)
            self.all_suspenders.append(self.suspender_sha)
        except Exception as e:
            cprint(f'[orange_red1]{TAB}failed to create sha suspender:[/orange_red1] {e}')
            pass
        
        try:
            self.suspender_shb = SuspendBoolHigh(self.shb.state, sleep=5,
                                                 #pre_plan=tell_slack_shb_closed,
                                                 #post_plan=tell_slack_shb_opened,
            )
            self.all_suspenders.append(self.suspender_shb)
        except Exception as e:
            cprint(f'[orange_red1]{TAB}failed to create shb suspender:[/orange_red1] {e}')
            pass

    # def tell_slack_shb_closed(self):
    #     self.kafka.message({'echoslack': True, 'text': 'B shutter closed'})
    #     yield from null()
    # def tell_slack_shb_opened(self):
    #     self.kafka.message({'echoslack': True, 'text': 'B shutter opened'})
    #     yield from null() 

        
    def beamdown_message(self):

        ## ----------------------------------------------------------------------------------
        ## suspend upon beam dump, resume 30 seconds after hitting 90% of fill target
        warning_msg('''
    *************************************************************

      The beam has dumped. :(

      You do not need to do anything.  Bluesky suspenders have
      noticed the loss of beam and have paused your scan.

      Your scan will resume soon after the beam returns.
    ''')
        whisper('''
          You may also terminate your scan by hitting 
          C-c twice then entering RE.stop()
    ''')
        warning_msg('''                                  
    *************************************************************
    ''')
        self.kafka.message({'echoslack': True, 'text': ':skull_and_crossbones: Beam has dumped! :skull_and_crossbones:'})
        yield from null()
    def beamup_message(self):
        self.kafka.message({'echoslack': True, 'text': ':sunrise: Beam has returned! :sunrise:'})
        yield from null()


        

    def set_suspenders(self):
        if self.suspenders_engaged:
            return
        for s in self.all_suspenders:
            self.re.install_suspender(s)
        self.suspenders_engaged = True

    def clear_suspenders(self):
        if self.busy is False:
            self.re.clear_suspenders()
            self.suspenders_engaged = False
        


    def clear_to_start(self):
        ok = True
        text = ''
        # return (ok, text)
        if self.ring.current.get() < 10:
            ok = False
            text += 'There is no current in the storage ring. Solution: wait for beam to come back\n'
        if self.bmps.state.get() == 0:
            ok = False
            text += 'BMPS is closed. Solution: check vacuum levels and gate valves, then call the control room and ask to have it opened\n'
        if self.sha.state.get() == 1:
            ok = False
            text += 'Front end shutter (sha) is closed. Solution: if there is current in the ring, search the FOE then do sha.open()\n'
        if self.shb.state.get() == 1:
            print()
            action = animated_prompt('B shutter is closed.  Open shutter? ' + PROMPTNC).strip()
            openit = False
            if action == '' or action[0].lower() == 'y':
                openit = True
            else:
                openit = False
            if openit == True:
                self.shb.open()
            if self.shb.state.get() == 1:  # B shutter failed to open
                ok = False
                text += 'Photon shutter (shb) is closed. Solution: search the hutch then do shb.open()\n'
            else:                   # B shutter successfully opened
                ok = True
        # if quadem1.I0.get() < 0.1:
        #     ok = 0
        #     text += 'There is no signal on I0\n'
        return (ok, text)
            
