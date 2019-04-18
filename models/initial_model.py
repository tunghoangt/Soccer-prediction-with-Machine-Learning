import pandas as pd
from sklearn.linear_model import LogisticRegression
from helpers import *

DATA_SRC = '../Data/PL_site_2006_2018/masterdata.csv'

df = pd.read_csv(DATA_SRC)

# create win/lose label
df['target'] = df[['Score_home', 'Score_away']].apply(score_to_win, axis = 1)
print(df.head())
