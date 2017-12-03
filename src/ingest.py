import pandas as pd
import numpy as np
from app import df


# Read and clean data
def importAndPrep(app):
    # Remove sufficiently null columns
    nullCols = df.columns[df.isnull().sum() > (len(df)/2)].tolist()
    df.drop(nullCols, axis=1, inplace=True)

    debug = "Prepared %i rows!" % len(df)
    app.logger.debug(debug)

    return df


def getByState(state):
    print(df.head())
    return len(df[df.STABBR == state])
