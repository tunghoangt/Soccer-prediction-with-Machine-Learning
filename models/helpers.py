import math, random, csv
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
from sklearn.preprocessing import StandardScaler

def score_to_win(scores):
    """
    Converts individual game scores into a multi-class label where:
    home_win = 1; draw = 0; home_loss = -1
    """
    if scores[0] > scores[1]:
        return 1
    elif scores[0] == scores[1]:
        return 0
    else:
        return -1

def gd_vectors(scores):
    """
    Calculate the goal difference of the each game from the perspective of the
    home team, for use in form calcluations.
    """
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
    """
    Pull out the window length previous results for the input team. If boolean,
    then simply the win/loss values are added, otherwise goal difference is used.
    """
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
    """
    Calcluated a linear momentum measure for a team given a history of goal
    difference. Simply, the linear sum of their previous results.
    """
    previous_results = get_window(matchID, team, gd_vectors, window, boolean)
    if not previous_results:
        return 0
    return sum(previous_results)

def exponential_momentum(matchID, team, gd_vectors, alpha, boolean = True):
    """
    Calculate an exponentially-decaying weight of a team's recent performance
    which places more emphasis on recent result.
    """
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

def run_model_diagnostics(X, y, clfs, size = .2, state = 42, is_classification = True, get_metrics = True):
    """
    Automated model fitting & testing on input X & y. Can be used for both classification
    and regression problems, as controlled by is_classification.
    """
    # TODO: add standardization
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = size, random_state = state)
    if get_metrics:
        metric_map = { str(type(clf)).split('.')[-1][:-2]: [] for clf in clfs }

    for clf in clfs:
        clf_name = str(type(clf)).split('.')[-1][:-2]
        clf.fit(X_train, y_train)
        y_pred = clf.predict(X_test)

        if is_classification:
            # accuracy score, confusion matrix, ROC curve
            # TODO: maybe these should be dictionaries too
            metric_map[clf_name].append( ("score", clf.score(X_test, y_test)) )
        #else:
            # rmse, full
    if get_metrics:
        return metric_map
    else:
        return (y_test, y_pred, clfs)

def build_exp_goals_model(df, clf, test_year = 2018, features_to_drop = ['MatchID', 'Team', 'year', 'Score']):
    """
    Using an input sklearn classifier, clf, for a given test_year fit a goal model
    to predict expected goals in a given game for a given team.
    """
    X = df[df.year != test_year].drop(columns = features_to_drop).values
    y = df[df.year != test_year].values
    clf.fit(X, y)
    return clf

def build_game_stats_model(df, clf, feature, window = 10, test_year = 2018, features_to_drop = ['MatchID', 'Team', 'year']):
    """
    Using an input sklearn classifier, clf, for a given test_year fit a game stat model
    (e.g. Clearances) for use in predicting the value in a given game for a given team.
    """
    prem_teams = df[df.year != test_year].Team.unique()
    X_as_list, y_as_list = [], []
    for team in prem_teams:
        team_df = df[df.Team == team]  # TODO: what if this is empty (promoted)
        fit_df = team_df[team_df.year != test_year].drop(columns = features_to_drop + [feature])
        for i in range(team_df.shape[0] - window - 1):
            X_vec = fit_df.iloc[i:i + window].values.flatten()
            if X_vec.shape[0] == 8 * window:
                X_as_list.append(X_vec)
                y_as_list.append(team_df[feature].values[i + window + 1]) # target is next game's value

    # convert to vectors
    X = np.vstack(X_as_list)
    y = np.array(y_as_list)
    clf.fit(X, y)
    return clf

def fit_game(game, df, clf_map, goal_model, noise_map, window = 10,
             relegated = ['Hull', 'Middlesbrough', 'Sunderland'], features_to_drop = ['MatchID', 'Team', 'year']):
    """
    Given a set of sklearn game-stat models, clf_map, and an expected goals model
    predict the result of a given game for a given team. The prediction is done using
    the previous window games. A noise_map will overlay noise for each game-stat
    feature for use in simulation (where this is run many times). Teams that were
    relegated the previous year are used as proxies for the newly promoted teams.
    """
    team_df = df[df.Team == game.Team]
    if team_df.shape[0] < window:  # newly promoted teams at the beginning of simulation
        relegated_df = df[(df.Team == relegated[0]) | (df.Team == relegated[1]) | (df.Team == relegated[2])]
        team_df = pd.concat([relegated_df, team_df])

    # include already known variables
    new_row = {'MatchID': game.MatchID, 'Team': game.Team, 'year': game.year, 'Score': None, 'Shots': None,
               'Passes': None, 'Clearances': None, 'Offsides': None, 'Fouls': None,
               'Expenditures': game.Expenditures, 'Income': game.Income, 'IsHome': game.IsHome}

    for feature in clf_map.keys():
        X = team_df.tail(window).drop(columns = features_to_drop + [feature]).values.flatten().reshape(1,-1)
        noise = noise_map[feature] * np.random.normal()
        new_row[feature] = max(int(clf_map[feature].predict(X)[0]) + noise, 0)

    goal_features = ['Shots', 'Passes', 'Clearances', 'Offsides', 'Fouls', 'Expenditures', 'Income', 'IsHome']
    X_score_as_list = [ new_row[feature] for feature in goal_features ]

    X_score = np.array(X_score_as_list).reshape(1,-1)
    new_row['Score'] = int(goal_model.predict(X_score)[0])
    return new_row

def get_team_points(df, test_year = 2018):
    """
    Given a simulated dataframe, with results for test_year, determine each
    team's final point totals over 38 games.
    """
    year_df = df[df.year == test_year]
    point_dict = { team: [] for team in year_df.Team.unique() }
    match_ids = year_df.MatchID.unique() # need to match games on MatchID
    for match_id in match_ids:
        game = year_df[year_df.MatchID == match_id]
        result = game[['Team', 'Score']].values
        if result[0][1] == result[1][1]:  # draw
            point_dict[result[0][0]].append(1)
            point_dict[result[1][0]].append(1)
        elif result[0][1] > result[1][1]:
            point_dict[result[0][0]].append(3)
            point_dict[result[1][0]].append(0)
        else:
            point_dict[result[0][0]].append(0)
            point_dict[result[1][0]].append(3)

    table = []
    for team, point_list in point_dict.items():
        table.append( (team, sum(point_list)) )
    return table

def run_simulation(df, runs, model_map, goal_model, test_year = 2018, stat = 'avg'):
    """
    Given a dataframe of game-stats and scores, a set of sklearn models for game-stats
    and expected goals along with a year being simulated, run a simulation runs times
    and generated the summary statistics denoted by stat.
    """
    season_df = df[df.year == test_year].drop(columns = list(model_map.keys()) + ['Score'])
    base_df = df[df.year == test_year - 1]
    season_point_totals = { team: [] for team in season_df.Team.unique() } # list of simulation results

    for run in range(runs):

        run_df = base_df.copy()
        for row in season_df.iterrows():
            game = row[1]
            simulated_result = fit_game(game, run_df, model_map, goal_model)
            run_df = run_df.append(simulated_result, ignore_index = True)

        simulated_table = get_team_points(run_df)
        for points in simulated_table:
            season_point_totals[points[0]].append(points[1])

    # TODO: add more aggregators (i.e. stdev & probabilites of position finish)
    return [ (team, sum(point_totals)/len(point_totals)) for team, point_totals in season_point_totals.items() ]
