import logging
import pandas as pd
from dataStore import majors_mapping

log = logging.getLogger(__name__)


def getByState(df, state):
    return df[df.STABBR == state]


def getByMajor(df, majors):
    # TODO extend this to accept multiple majors
    major = majors[0]
    if major == "resources":
        majorsToQuery = majors_mapping[(majors_mapping["ShortName"] == "agriculture") |
                                       (majors_mapping["ShortName"] == "resources")]
    elif major == "engineering_technology":
        majorsToQuery = majors_mapping[(majors_mapping["ShortName"] == "engineering") |
                                       (majors_mapping["ShortName"] == "engineering_technology")]
    elif major == "precision_production":
        majorsToQuery = majors_mapping[(majors_mapping["ShortName"] == "mechanic_repair_technology") |
                                       (majors_mapping["ShortName"] == "precision_production")]
    else:
        majorsToQuery = majors_mapping[majors_mapping["ShortName"] == major]

    byMajor = pd.DataFrame()
    for index, row in majorsToQuery.iterrows():
        byMajor = pd.concat([df[df[row["Code"]] > 0], byMajor])

    return byMajor


def dfToTuple(df):
    return [tuple(x) for x in df.values]
