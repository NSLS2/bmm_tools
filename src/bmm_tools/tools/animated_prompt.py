
PROMPTNC = "[YES: y then Enter (or just Enter) ● NO: n then Enter] "

PEAKPROMPTNC = '''
 y: pluck motor position from plot 
 n: do nothing
 p: move to peak position
 o: move to center of pass position (com)
 c: move to center of FWHM (cen)
 
 Select y/n/p/o/c then Enter > '''

try:
    from terminaltexteffects.effects.effect_wipe import Wipe
    def animated_prompt(prompt_text: str) -> str:
        #if is_re_worker_active is False:
        effect = Wipe(prompt_text)
        with effect.terminal_output(end_symbol=" ") as terminal:
            for frame in effect:
                terminal.print(frame)
        return input()
        #else:
        #    ans = input(prompt_text).strip()
        #    return ans
except:
    ## fallback if terminaltexteffects is not installed
    def animated_prompt(prompt_text: str) -> str:
        ans = input(prompt_text).strip()
        return ans
    
