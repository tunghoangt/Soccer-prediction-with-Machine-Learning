import pandas as pd
from helpers import *

DATA_SRC = '../Data/PL_site_2006_2018/masterdata.csv'
df = pd.read_csv(DATA_SRC)

# create win/lose label
df['target'] = df[['Score_home', 'Score_away']].apply(score_to_win, axis = 1)

# Form feature #
scores = df[['MatchID', 'Home_team', 'Away_team', 'Score_home', 'Score_away']].values
gd = gd_vectors(scores)

away_form = []
home_form = []
for game in scores:
    id, home_team, away_team, _, _ = game
    away_form.append( exponential_momentum(id, away_team, gd, alpha = .65) )
    home_form.append( exponential_momentum(id, home_team, gd, alpha = .65) )

df['away_form'] = pd.Series(away_form)
df['home_form'] = pd.Series(home_form)
print(df.tail())
