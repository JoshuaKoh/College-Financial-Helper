import pandas as pd
import numpy as np

# Read and clean data
df = pd.read_csv('data/college-scorecard.csv', sep=',')

# Remove sufficiently null columns
nullCols = df.columns[df.isnull().sum() > (len(df)/2)].tolist()
df.drop(nullCols, axis=1, inplace=True)

