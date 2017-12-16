import pandas as pd
import numpy as np

df = pd.read_csv('../data/college-scorecard.csv', sep=',',
                 dtype={'ZIP': str,
                        'NPCURL': str,
                        'C150_L4_POOLED_SUPP': str,
                        'C150_4_POOLED_SUPP': str,
                        'C200_L4_POOLED_SUPP': str,
                        'C200_4_POOLED_SUPP': str,
                        'ALIAS': str,
                        'T4APPROVALDATE': str
                        })

RETENTION = "RET_FT4"
df = df[(df[RETENTION].notnull()) & (df[RETENTION] != 0)]
df = df.dropna(axis=1, how='any')

# TODO NORMALIZE DATA WITHIN NUMERICAL SCALE

# TODO DIMENSIONALITY REDUCTION

# TODO UNSUPERVISED: K-MEANS

# TODO CLUSTER ANALYSIS

# TODO GROUP RETENTION INTO DISCRETE BUCKETS

# TODO DECISION TREE PREDICTOR

# TODO NEURAL NET PREDICTOR

# TODO SVM PREDICTOR
