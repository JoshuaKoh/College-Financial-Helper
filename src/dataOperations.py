from dataStore import (majors_mapping, raw_df, importantColumns)
import logging

log = logging.getLogger(__name__)


def getMajorsForDropdown():
    columns = ["FormattedName", "ShortName", "Description"]
    majors = majors_mapping[majors_mapping.FormattedName.notnull()][columns]
    majors.sort_values("FormattedName", inplace=True)

    return majors


majorsMap = getMajorsForDropdown()


def importAndPrep(df):
    # Remove sufficiently null columns
    nullCols = df.columns[df.isnull().sum() > (len(df)/2)].tolist()
    df.drop(nullCols, axis=1, inplace=True)

    log.info("Prepared %i rows!" % len(df))

    return df


def getByState(state, major=None):
    if major is not None:
        return raw_df[raw_df.STABBR == state][importantColumns]


def getByMajor(majors):
    # TODO extend this to accept multiple majors
    major = majors[0]
    if major == "resources":
        return majorsMap[(majorsMap["ShortName"] == "agriculture") |
                         (majorsMap["ShortName"] == "resources")]
    elif major == "engineering_technology":
        return majorsMap[(majorsMap["ShortName"] == "engineering") |
                         (majorsMap["ShortName"] == "engineering_technology")]
    elif major == "precision_production":
        return majorsMap[(majorsMap["ShortName"] == "mechanic_repair_technology") |
                         (majorsMap["ShortName"] == "precision_production")]
    return majorsMap[majorsMap["ShortName"] == major]


def dfToTuple(df):
    return [tuple(x) for x in df.values]
