
'''Attenuation factors for the Cu foils in the attenuator block at
the entrance to the goniometer.

This extremely simple model is used both for live plotting of the XRR
data and for reducing the XRR data for export or analysis

'''


## From Jean


# binary             0  1        2                  3                                         4
# level              0  1        2        3         4         5         6         7*          8
#KNOWN_ATTENUATION = [1, 6.85865, 47.0088, 318.6107, 2225.346, 15046.19, 97500.05, 668718.718, ]

## From Jean, processing numbers

KNOWN_ATTENUATION = [1, 6.67114, 44.16972, 273.1222, 1800.653, 11568.12, 92113, 468725, 1442273]


## From Donald

# KNOWN_ATTENUATION = [1, 6.85865,  # 0 1
#                      6.85865*6.858,  # 2
#                      6.85865*6.858*6.858,  # 3
#                      6.85865*6.858*6.858*6.964,  # 4
#                      6.85865*6.858*6.858*6.964*6.964,  # 5
#                      6.85865*6.858*6.858*6.964*6.964*6.981,  # 6
# ]

                     
                     

