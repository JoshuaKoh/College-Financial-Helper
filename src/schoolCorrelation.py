from dataStore import reduced_df, old_df, degreeColumns
import numpy as np
import pandas as pd
import scipy
import matplotlib.pyplot as plt
from scipy.stats import linregress
import math

'''
1. Take schools that HAVE SAT/ACT scores and graph test score vs. other variable
2. "other variable" includes:
- tuition,                              NPT4_PUB,           0.328
- students withdrawn after 2 years      WDRAW_ORIG_YR2_RT,  -0.582, use old df!
- students withdrawn after 3 years      WDRAW_ORIG_YR3_RT,  -0.529, use old df!
- students withdrawn after 4 years      WDRAW_ORIG_YR4_RT,  -0.505, use old df!
- students enrolled after 2 years       ENRL_ORIG_YR2_RT,   0.676,  use old df!
- students enrolled after 3 years       ENRL_ORIG_YR3_RT,   -0.058, use old df!
- students enrolled after 4 years       ENRL_ORIG_YR4_RT,   -0.219, use old df!
- locale                                LOCALE,             -0.193
- number of students,                   D_PCTPELL_PCTFLOAN, 0.265
- number of degrees offered,            degree-only         0.128
- dropout rate,                         C150_4,             0.822
- avg family income,                    DEP_INC_AVG,        0.65
- first generation,                     FIRST_GEN,          -0.67
- aided low-income students,            INC_PCT_LO,         -0.538
- family income,                        MD_FAMINC,          0.579
- faculty salary,                       AVGFACSAL,          0.688
- admission rate,                       ADM_RATE,           -0.403
- student federal loan,                 PCTFLOAN,           -0.536
3. Find "other variable"s that are strongly correlated.
4. Use these variables to extrapolate SAT/ACT scores for schools which lack those (i.e. Clayton)'''


def getCoords(m, b, xmin, xmax):
    # y = mx + b
    x = [xmin, xmax]
    y = [(m * xval + b) for xval in x]
    return x, y


# Not implementing ACT because SAT and ACT are almost 1-to-1 correlated.
def satScoresVs():
    # 1. Change which variable to correlate to SAT scores.
    variable = "Degrees"
    # 2. Select whether to use the reduced or old data source.
    # withNoSATNulls = reduced_df[reduced_df["SAT_AVG"].notnull()]
    withNoSATNulls = old_df[old_df["SAT_AVG"].notnull()]
    # 3. Select whether your variable contains "PrivacySurpressed"
    withNoVarNulls = withNoSATNulls[(withNoSATNulls[variable].notnull())
                                    # & ~(withNoSATNulls[variable].str.strip() == "PrivacySuppressed")]
                                    ]
    x = withNoVarNulls["SAT_AVG"]
    # y = pd.to_numeric(withNoVarNulls[variable])
    y = []
    # === FOR DEGREES ONLY ===
    for iter, row in withNoVarNulls.iterrows():
        majorCount = 0
        for degree in degreeColumns:
            majorCount += 1 if row[degree] > 0 else 0
        y.append(majorCount)
    # === END DEGREES ONLY ===

    m, b, r_value, p_value, std_err = linregress(x, y)
    xCoords, yCoords = getCoords(m, b, xmin=x.min(), xmax=x.max())

    fig = plt.figure()
    ax = fig.add_subplot(111)

    plt.ylabel("%s value" % variable)
    plt.xlabel("SAT scores")
    ax.set_title('%i points, %f correlated' % (len(withNoVarNulls), r_value))
    plt.plot(x, y, 'k.', color='b', markersize=3)
    plt.plot(xCoords, yCoords, 'k-')
    plt.show()
