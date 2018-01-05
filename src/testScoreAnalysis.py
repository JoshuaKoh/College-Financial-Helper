from dataStore import reduced_df
import numpy as np

'''
FINISHED!
Results used in SAT/ACT section of schoolSelector to determine score differences

One-off experiment to find the point difference between the following for SAT/ACT scores:
- q1 to q2
- q2 to q3
'''


def testScoreAnalysis():
    writDist25 = []
    critDist25 = []
    mathDist25 = []
    actDist25  = []
    writDist75 = []
    critDist75 = []
    mathDist75 = []
    actDist75  = []
    
    for index, row in reduced_df.iterrows():
        if (not np.isnan(row["SATWRMID"]) and
                not np.isnan(row["SATWR25"]) and
                not np.isnan(row["SATWR75"])):
            lower = row["SATWRMID"] - row["SATWR25"]
            upper = row["SATWR75"] - row["SATWRMID"]
            writDist25.append(lower)
            writDist75.append(upper)

        if (not np.isnan(row["SATVRMID"]) and
                not np.isnan(row["SATVR25"]) and
                not np.isnan(row["SATVR75"])):
            lower = row["SATVRMID"] - row["SATVR25"]
            upper = row["SATVR75"] - row["SATVRMID"]
            critDist25.append(lower)
            critDist75.append(upper)

        if (not np.isnan(row["SATMTMID"]) and
                not np.isnan(row["SATMT25"]) and
                not np.isnan(row["SATMT75"])):
            lower = row["SATMTMID"] - row["SATMT25"]
            upper = row["SATMT75"] - row["SATMTMID"]
            mathDist25.append(lower)
            mathDist75.append(upper)

        if (not np.isnan(row["ACTCMMID"]) and
                not np.isnan(row["ACTCM25"]) and
                not np.isnan(row["ACTCM75"])):
            lower = row["ACTCMMID"] - row["ACTCM25"]
            upper = row["ACTCM75"] - row["ACTCMMID"]
            actDist25.append(lower)
            actDist75.append(upper)

    writ25Avg = np.average(writDist25)
    writ75Avg = np.average(writDist75)
    crit25Avg = np.average(critDist25)
    crit75Avg = np.average(critDist75)
    math25Avg = np.average(mathDist25)
    math75Avg = np.average(mathDist75)
    act25Avg = np.average(actDist25)
    act75Avg = np.average(actDist75)

    print("Writing:\n"
          "Q1-Q2:\t%.1f\n"
          "Q2-Q3:\t%.1f\n\n"
          "Critical Thinking:\n"
          "Q1-Q2:\t%.1f\n"
          "Q2-Q3:\t%.1f\n\n"
          "Math:\n"
          "Q1-Q2:\t%.1f\n"
          "Q2-Q3:\t%.1f\n\n"
          "ACT:\n"
          "Q1-Q2:\t%.1f\n"
          "Q2-Q3:\t%.1f\n\n"
          % (writ25Avg, writ75Avg, crit25Avg, crit75Avg, math25Avg, math75Avg, act25Avg, act75Avg))


testScoreAnalysis()
