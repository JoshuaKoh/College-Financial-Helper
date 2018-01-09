import dataOperations as do
import locationUtil as locU
import testScoreUtil as testU
from dataStore import reduced_df
import numpy as np
import pandas as pd
from schoolCorrelation import schoolsACTSimilarTo, schoolsSATSimilarTo


def selectSchools(zipCode, major, sat_crit, sat_writ, sat_math, act):
    withCP = reduced_df.assign(cp=0)
    byMajor = do.getByMajor(withCP, [major])

    # TODO ALLOW ALL STATES TO BE SEARCHABLE
    userState, userLat, userLong = locU.extractDataFromZip(zipCode)
    byState = do.getByState(byMajor, userState)

    # EXTRAPOLATE NULL SAT/ACT DATA
    for index, row in byState.iterrows():
        byState.loc[byState['UNITID'] == row["UNITID"], 'ACTCMMID'] = schoolsACTSimilarTo(row)
        byState.loc[byState['UNITID'] == row["UNITID"], 'SAT_AVG'] = schoolsSATSimilarTo(row)

    # FILTER (STILL) NULL SAT/ACT ROWS
    withNoSATNulls = byState[byState["SAT_AVG"].notnull()]
    withNoACTNulls = withNoSATNulls[withNoSATNulls["ACTCMMID"].notnull()]
    withNoSAT0s = withNoACTNulls[withNoACTNulls["SAT_AVG"] != 0]
    finalDf = withNoSAT0s[withNoSAT0s["ACTCMMID"] != 0]

    # DROP ROWS OUTSIDE SAT/ACT 25%/75% RANGE


    userSATwritNorm = testU.normalizeSAT(sat_writ)
    userSATcritNorm = testU.normalizeSAT(sat_crit)
    userSATmathNorm = testU.normalizeSAT(sat_math)
    userACTNorm = testU.normalizeACT(act)

    finalDf = finalDf.assign(cost_points=pd.Series(np.zeros(len(finalDf))).values)

    for index, row in finalDf.iterrows():
        cost_points = 0.0

        schoolState = row["STABBR"]
        schoolLat = row["LATITUDE"]
        schoolLng = row["LONGITUDE"]
        distance = locU.getDistanceBetweenCoords(userLat, userLong, schoolLat, schoolLng)

        # TODO VERIFY DISTANCE CP
        '''
        Use an exponential function that takes distance as input and outputs CP. 
        Decays and gives less CP as distance increases. 
        '''
        if distance < 70:               # in-state and close
            cost_points += 0
        elif schoolState != userState:  # out of state
            cost_points += 2
        else:                           # in-state and far
            cost_points += .6

        # TODO VERIFY SAT/ACT CP.
        writDistance = 53.5
        critDistance = 55
        mathDistance = 55
        overallDistance = 55
        actq1q2Distance = 3
        actq2q3Distance = 2.5
        if (np.isnan(row["SATWRMID"]) or
                np.isnan(row["SATVRMID"]) or
                np.isnan(row["SATMTMID"])):
            studentScore = ((sat_crit + sat_writ)/2) + sat_math
            schoolScore = row["SAT_AVG"]
            school25p = schoolScore - (overallDistance * 2)
            school75p = schoolScore + (overallDistance * 2)

            normStudentSAT = testU.normalizeCMSAT(studentScore)
            normSchoolSAT = testU.normalizeCMSAT(schoolScore)
            squaredSAT = testScoreLossFunc(normStudentSAT, normSchoolSAT)

            # RULE 1: If between 25th and 75 percentile, give 0 CP.
            if school25p < studentScore < school75p:
                cost_points += 0
            # RULE 2: If beyond min or max, give 1 CP for SAT.
            elif studentScore < (2 * school25p) or studentScore > (2 * school75p):
                cost_points += 1
            # RULE 3: If in the outer bands, give CP scaling with loss function.
            else:
                cost_points += 2 * squaredSAT
        else:
            schoolSATwritMed = row["SATWRMID"]
            schoolSATwrit25p = row["SATWR25"] if row["SATWR25"] else schoolSATwritMed - writDistance
            schoolSATwritMedNorm = testU.normalizeSAT(schoolSATwritMed)
            schoolSATwrit75p = row["SATWR75"] if row["SATWR75"] else schoolSATwritMed + writDistance
            schoolSATwritMin = (schoolSATwritMed * -1) + (schoolSATwrit25p * 2)
            schoolSATwritMax = (schoolSATwritMed * -1) + (schoolSATwrit75p * 2)
            schoolSATcritMed = row["SATVRMID"]
            schoolSATcrit25p = row["SATVR25"] if row["SATVR25"] else schoolSATcritMed - critDistance
            schoolSATcritMedNorm = testU.normalizeSAT(schoolSATcritMed)
            schoolSATcrit75p = row["SATVR75"] if row["SATVR75"] else schoolSATcritMed + critDistance
            schoolSATcritMin = (schoolSATcritMed * -1) + (schoolSATcrit25p * 2)
            schoolSATcritMax = (schoolSATcritMed * -1) + (schoolSATcrit75p * 2)
            schoolSATmathMed = row["SATMTMID"]
            schoolSATmath25p = row["SATMT25"] if row["SATMT25"] else schoolSATmathMed - mathDistance
            schoolSATmathMedNorm = testU.normalizeSAT(schoolSATmathMed)
            schoolSATmath75p = row["SATMT75"] if row["SATMT75"] else schoolSATmathMed + mathDistance
            schoolSATmathMin = (schoolSATmathMed * -1) + (schoolSATmath25p * 2)
            schoolSATmathMax = (schoolSATmathMed * -1) + (schoolSATmath75p * 2)

            squaredSATwrit = testScoreLossFunc(userSATwritNorm, schoolSATwritMedNorm)
            squaredSATcrit = testScoreLossFunc(userSATcritNorm, schoolSATcritMedNorm)
            squaredSATmath = testScoreLossFunc(userSATmathNorm, schoolSATmathMedNorm)

            # RULE 1: If between 25th and 75 percentile, give 0 CP.
            if schoolSATwrit25p < sat_writ < schoolSATwrit75p:
                cost_points += 0
            # RULE 2: If beyond min or max, give 1 CP for SAT.
            elif sat_writ < schoolSATwritMin or sat_writ > schoolSATwritMax:
                cost_points += 1
            # RULE 3: If in the outer bands, give CP scaling with loss function.
            else:
                cost_points += 2 * squaredSATwrit

            # RULE 1: If between 25th and 75 percentile, give 0 CP.
            if schoolSATcrit25p < sat_crit < schoolSATcrit75p:
                cost_points += 0
            # RULE 2: If beyond min or max, give 1 CP for SAT.
            elif sat_crit < schoolSATcritMin or sat_crit > schoolSATcritMax:
                cost_points += 1
            # RULE 3: If in the outer bands, give CP scaling with loss function.
            else:
                cost_points += 2 * squaredSATcrit

            # RULE 1: If between 25th and 75 percentile, give 0 CP.
            if schoolSATmath25p < sat_math < schoolSATmath75p:
                cost_points += 0
            # RULE 2: If beyond min or max, give 3 CP.
            elif sat_math < schoolSATmathMin or sat_math > schoolSATmathMax:
                cost_points += 1
            # RULE 3: If in the outer bands, give CP scaling with loss function.
            else:
                cost_points += 2 * squaredSATmath

        schoolACTMed = row["ACTCMMID"]
        schoolACT25p = row["ACTCM25"] if row["ACTCM25"] else schoolACTMed - actq1q2Distance
        schoolACTMedNorm = testU.normalizeACT(schoolACTMed)
        schoolACT75p = row["ACTCM75"] if row["ACTCM75"] else schoolACTMed + actq2q3Distance
        schoolACTMin = (schoolACTMed * -1) + (schoolACT25p * 2)
        schoolACTMax = (schoolACTMed * -1) + (schoolACT75p * 2)
        squaredACT = testScoreLossFunc(userACTNorm, schoolACTMedNorm)

        # RULE 1: If between 25th and 75 percentile, give 0 CP.
        if schoolACT25p < act < schoolACT75p:
            cost_points += 0
        # RULE 2: If beyond min or max, give 3 CP.
        elif act < schoolACTMin or act > schoolACTMax:
            cost_points += 3
        # RULE 3: If in the outer bands, give CP scaling with loss function.
        else:
            cost_points += 6 * squaredACT

        # TODO WEIGHTING FOR LOCATION

        # TODO WEIGHTING FOR STARTING SALARY

        # TODO WEIGHTING FOR DROPOUT RATE
        # Based on http://www.slate.com/blogs/moneybox/2014/11/19/u_s_college_dropouts_rates_explained_in_4_charts.html
        if row["C150_4"] < 0.55:
            cost_points += 6 * (1 - row["C150_4"])
        else:
            cost_points += 3 * (1 - row["C150_4"])

        # TODO SOME KIND OF ANALYSIS FOR COST...?

        finalDf.loc[finalDf['UNITID'] == row["UNITID"], 'cost_points'] = cost_points

    # TODO SORT BY CP COLUMN AND RETURN
    sortedDf = finalDf.sort_values("cost_points")
    print(sortedDf[["INSTNM", "cost_points"]])
    return None


# larger negative value -> score1 is significantly less than score2
# larger positive value -> score2 is significantly more than score1
# changes in close values are small, changes in disparate values are large
def testScoreLossFunc(score1, score2):
    return ((score1**2) - (score2**2))**2


selectSchools("30277", "business_marketing", 690, 700, 700, 29)
