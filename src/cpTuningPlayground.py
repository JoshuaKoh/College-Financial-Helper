from dataStore import reduced_df
import numpy as np


def schoolsWithNoTestScores():
    withNoScores = reduced_df[reduced_df["SAT_AVG"].isnull()]
    print(withNoScores["TUITIONFEE_IN"].head())


schoolsWithNoTestScores()