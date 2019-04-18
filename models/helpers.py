import csv

def score_to_win(scores):
    # turn the scores into a label (w/r/t home team)
    # win = 1; draw = 0; loss = -1
    if scores[0] > scores[1]:
        return 1
    elif scores[0] == scores[1]:
        return 0
    else:
        return -1
