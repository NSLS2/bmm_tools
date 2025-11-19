
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
        self.dspacing_111 = 3.1355248  # 13 November, 2025
        self.dspacing_311 = 1.6376262  # 8 September, 2025

        self.offset_111 = 16.0800639   # 13 November, 2025
        self.offset_311 = 15.9881364   # 8 September, 2025
        
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
    8 September 2025

    '''
    if xtal == '111':
        m = -4.1409e-06
        b = 4.47946925
        return(m*energy + b)
    else:
        m = -3.3122e-06
        b = 2.38902936
        return(m*energy + b)
