
from scipy.ndimage import center_of_mass
def com(signal):
    '''Return the center of mass of a 1D array. This is used to find the
    center of a peak-like scan, e.g. rocking curve or slit height.'''
    return int(center_of_mass(signal)[0])


import pandas
def peak(signal):
    '''Return the index of the maximum of a 1D array.  This is used to find the
    center of a peak-like scan, e.g. rocking curve or slit height.'''
    return pandas.Series.idxmax(signal)

