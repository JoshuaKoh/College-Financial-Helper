from app import df

importantColumns = ['INSTNM',           # Institution Name
                    'CITY',             # City
                    'STABBR',           # State Abbreviation
                    'ZIP',              # Zip Code
                    'INSTURL',          # Institution Homepage URL
                    'NPCURL',           # Institution Price Calculator
                    'ADM_RATE_ALL',     # Admission Rate
                    'SAT_AVG_ALL'       # SAT Average
                    ]


# Read and clean data
def importAndPrep(app):
    # Remove sufficiently null columns
    nullCols = df.columns[df.isnull().sum() > (len(df)/2)].tolist()
    df.drop(nullCols, axis=1, inplace=True)

    app.logger.debug("Prepared %i rows!" % len(df))

    return df


def getByState(state, major=None):
    if major is not None:
        return df[df.STABBR == state][importantColumns]


