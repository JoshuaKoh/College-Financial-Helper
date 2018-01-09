import dataOperations as do
import locationUtil as locU
import testScoreUtil as testU
from dataStore import reduced_df
import numpy as np
import pandas as pd
from schoolCorrelation import schoolsACTSimilarTo, schoolsSATSimilarTo


def selectSchools(zipCode, major, sat_crit, sat_writ, sat_math, act, doGeneralSAT=True, doMinMaxScores=True):
    writDistance = 53.5
    critDistance = 55
    mathDistance = 55
    overallDistance = 55
    actq1q2Distance = 3
    actq2q3Distance = 2.5

    if doMinMaxScores:
        writDistance *= 2
        critDistance *= 2
        mathDistance *= 2
        overallDistance *= 2
        actq1q2Distance *= 2
        actq2q3Distance *= 2

    byMajor = do.getByMajor(reduced_df, [major])

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

    finalDf = finalDf.assign(cost_points=pd.Series(np.zeros(len(finalDf))).values)

    for index, row in finalDf.iterrows():
        print(row["INSTNM"])
        # DROP ROWS OUTSIDE SAT/ACT RANGE
        schoolACTMed = row["ACTCMMID"]
        schoolACT25p = row["ACTCM25"] if row["ACTCM25"] else schoolACTMed - actq1q2Distance
        schoolACT75p = row["ACTCM75"] if row["ACTCM75"] else schoolACTMed + actq2q3Distance
        if act <= schoolACT25p or act >= schoolACT75p:
            finalDf.drop(index, inplace=True)
            # print("ACT")
            # print("Student %f, Lower %f, Upper %f" % (act, schoolACT25p, schoolACT75p))
            continue
        if (
                doGeneralSAT or
                np.isnan(row["SATWRMID"]) or
                np.isnan(row["SATVRMID"]) or
                np.isnan(row["SATMTMID"])
           ):
            studentScore = ((sat_crit + sat_writ)/2) + sat_math
            school25p = row["SAT_AVG"] - overallDistance
            school75p = row["SAT_AVG"] + overallDistance
            if studentScore <= school25p or studentScore >= school75p:
                finalDf.drop(index, inplace=True)
                # print("GENERAL SAT")
                # print("Student %f, Lower %f, Upper %f" % (studentScore, school25p, school75p))
                continue
        else:
            schoolSATwritMed = row["SATWRMID"]
            schoolSATwrit25p = row["SATWR25"] if row["SATWR25"] else schoolSATwritMed - writDistance
            schoolSATwrit75p = row["SATWR75"] if row["SATWR75"] else schoolSATwritMed + writDistance
            schoolSATcritMed = row["SATVRMID"]
            schoolSATcrit25p = row["SATVR25"] if row["SATVR25"] else schoolSATcritMed - critDistance
            schoolSATcrit75p = row["SATVR75"] if row["SATVR75"] else schoolSATcritMed + critDistance
            schoolSATmathMed = row["SATMTMID"]
            schoolSATmath25p = row["SATMT25"] if row["SATMT25"] else schoolSATmathMed - mathDistance
            schoolSATmath75p = row["SATMT75"] if row["SATMT75"] else schoolSATmathMed + mathDistance

            if (
                    sat_writ <= schoolSATwrit25p or sat_writ >= schoolSATwrit75p or
                    sat_crit <= schoolSATcrit25p or sat_crit >= schoolSATcrit75p or
                    sat_math <= schoolSATmath25p or sat_math >= schoolSATmath75p
               ):
                # print("PART SAT")
                # finalDf.drop(index, inplace=True)
                continue

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


selectSchools("30277", "computer", 500, 500, 500, 25)
