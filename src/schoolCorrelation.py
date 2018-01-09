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
    # 4. Use first y assignment if not analyzing exactly the degrees attribute.
    # y = pd.to_numeric(withNoVarNulls[variable])
    # === FOR DEGREES ONLY ===
    y = []
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


def schoolsACTSimilarTo(school):
    if np.isnan(school["C150_4"]):
        return 0
    if not np.isnan(school["ACTCMMID"]):
        return school["ACTCMMID"]

    targetDropout = school["C150_4"]
    droputDelta = 0.005

    prepped_df = old_df[(old_df["C150_4"].notnull()) & (old_df["ACTCMMID"].notnull())]

    byDropout = prepped_df[
        prepped_df["C150_4"].between((targetDropout - droputDelta), (targetDropout + droputDelta))]

    if np.isnan(byDropout["ACTCMMID"].mean()):
        return 0
    else:
        return byDropout["ACTCMMID"].mean()


def schoolsSATSimilarTo(school):
    if np.isnan(school["C150_4"]):
        return 0
    if not np.isnan(school["SAT_AVG"]):
        return school["SAT_AVG"]

    targetDropout = school["C150_4"]
    droputDelta = 0.005

    prepped_df = old_df[(old_df["C150_4"].notnull()) & (old_df["SAT_AVG"].notnull())]

    byDropout = prepped_df[
        prepped_df["C150_4"].between((targetDropout - droputDelta), (targetDropout + droputDelta))]

    if np.isnan(byDropout["SAT_AVG"].mean()):
        return 0
    else:
        return byDropout["SAT_AVG"].mean()


'''
FINISHED
Used to tune the correct configuration of features and deltas
'''
def schoolsSimilarToAnalyzer(school):
    '''
    Clayton State University,  139311, expected 20, got 19.8
    Liberty University, 232557, expected 23, got 22.7
    '''
    targetDropout = float(school["C150_4"].iloc[0])
    droputDelta = 0.005
    # targetSalary = float(school["AVGFACSAL"].iloc[0])
    # salaryDelta = 750
    # targetEnroll = float(school["ENRL_ORIG_YR2_RT"].iloc[0])
    # enrollDelta = 0.04
    # print(school["INSTNM"].to_string(index=False))
    # print("enrolled after 2 yrs: %s" % school["ENRL_ORIG_YR2_RT"].to_string(index=False))
    # print("dropout rate: %s" % school["C150_4"].to_string(index=False))
    # print("family salary: %s" % school["AVGFACSAL"].to_string(index=False))

    prepped_df = old_df[(old_df["C150_4"].notnull())
                        # & (old_df["ENRL_ORIG_YR2_RT"].notnull())
                        # & (old_df["AVGFACSAL"].notnull())
                        # & ~(old_df["ENRL_ORIG_YR2_RT"].str.strip() == "PrivacySuppressed")
                        & (old_df["ACTCMMID"].notnull())]
    # print("%i to start" % len(prepped_df))
    byDropout = prepped_df[
        prepped_df["C150_4"].between((targetDropout - droputDelta), (targetDropout + droputDelta))]
    # print("%f after dropout, out of %i schools" % (byDropout["ACTCMMID"].mean(), len(byDropout)))
    # bySalary = byDropout[
    #     byDropout["AVGFACSAL"].between((targetSalary - salaryDelta), (targetSalary + salaryDelta))]
    # print("%f after salary, out of %i schools" % (bySalary["ACTCMMID"].mean(), len(bySalary)))
    # byEnrollment = bySalary[
    #     bySalary["ENRL_ORIG_YR2_RT"].astype(float).between((targetEnroll - enrollDelta), (targetEnroll + enrollDelta))]
    # print("%f at end, out of %i schools" % (byDropout["ACTCMMID"].mean(), len(byDropout)))
    # print(byEnrollment[["INSTNM", "ACTCMMID"]])
    school["ACTCMMID"] = byDropout["ACTCMMID"]
    school["SAT_AVG"] = byDropout["SAT_AVG"]
    return school[["ACTCMMID", "SAT_AVG"]]
