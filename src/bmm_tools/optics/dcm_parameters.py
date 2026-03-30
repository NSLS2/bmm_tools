
class dcm_parameters():
    '''A simple class for maintaining calibration parameters for the
    Si(111) and Si(311) monochromators.

    Parameters
    ----------
    BMM_dcm.dspacing_111 : float
        d-spacing for the Si(111) mono
    BMM_offset_111 : float
        angular offset for the Si(111) mono
    BMM_dcm.dspacing_311 : float
        d-spacing for the Si(311) mono
    BMM_offset_311 : float
        angular offset for the Si(311) mono

    '''

    def __init__(self):
        self.dspacing_111 = 3.1351937  # 3 March, 2026
        self.dspacing_311 = 1.6375686  # 30 March, 2026

        self.offset_111 = 16.9261335   # 4 March, 2026
        self.offset_311 = 17.0996517   # 30 March, 2026
        
## see calibrate_pitch in BMM/mono_calibration.py
def approximate_pitch(energy, xtal='111'):
    '''Make a guess for the correct 2nd crystal pitch for a given energy.

    This is regressed from the values found during mono calibration.

    Arguments
    =========
    energy: (float)
      energy at which to estimate pitch
    xtal: (string) ['111']
      mono crystals to use for the approximation, default is '111'
      usually called in code as
         pitch = approximate_pitch(energy, xtal=dcm._crystal)

    Updated
    =======
    19-22 February 2026

    '''
    if xtal == '111':
        #return(1.309)
        m = -4.2553e-06
        b = 1.34835398
        return(m*energy + b)
    else:
        #return(3.9195)
        m = -3.1384e-06
        b = 4.03062239
        return(m*energy + b)
