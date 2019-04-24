import csv
import numpy as np
import math

def score_to_win(scores):
    # turn the scores into a label (w/r/t home team)
    # win = 1; draw = 0; loss = -1
    if scores[0] > scores[1]:
        return 1
    elif scores[0] == scores[1]:
        return 0
    else:
        return -1

# has to be changed given that some teams aren't in the Prem continuously
def gd_vectors(scores):
    gd_dict = {}
    for game in scores:
        # goal difference from the perspective of the home team
        id, home_team, away_team, home_goals, away_goals = game
        score = home_goals - away_goals
        gd_dict[home_team] = gd_dict.get(home_team, []) + [(id, score)]
        gd_dict[away_team] = gd_dict.get(away_team, []) + [(id,-1 * score)]
    return gd_dict

# TODO: add strength of opponent weighting
def get_window(matchID, team, gd_vectors, window = 5, boolean = False):
    team_results = gd_vectors[team]
    idx = -1
    for i, result in enumerate(team_results):
        if result[0] == matchID:
            idx = i
            break
    if idx < window - 1:
        return None
    return [ team_results[i][1] for i in range(idx - window, idx) ]

def linear_momentum(matchID, team, gd_vectors, window = 5, boolean = False):
    previous_results = get_window(matchID, team, gd_vectors, window, boolean)
    if not previous_results:
        return 0
    return sum(previous_results)

def exponential_momentum(matchID, team, gd_vectors, alpha, boolean = True):
    if alpha > .69:
        raise ValueError
    avg_vec, i = [], 1
    while sum(avg_vec) < 1:
        avg_vec.append( math.e ** (-1 * (alpha * i)) )
        i += 1
    avg_vec = sorted(avg_vec)
    previous_results = get_window(matchID, team, gd_vectors, len(avg_vec), boolean)
    if not previous_results:
        return 0
    return np.dot( np.array(avg_vec), np.array(previous_results) )
