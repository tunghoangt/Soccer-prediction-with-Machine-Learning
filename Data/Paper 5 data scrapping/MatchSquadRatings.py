import string,csv
import pandas as pd

"""



"""

map2013 = {}
map2014 = {}
map2015 = {}
mNameTorName13 = {}
mNameTorName14 = {}
mNameTorName15 = {}

def cleanFile(text_file):
    with open(text_file,"r") as fin, open("MatchSquads-2014_final.txt","w") as fout:
        flag = 0
        temp = ""
        for line in fin:
            var = str(line)
            var = var.rstrip('\n')
            if "Positions" not in var and "END MATCH" not in var and "NEXT TEAM" not in var and "..." not in var and "Substitutes" not in var:
                if flag == 0:
                    temp = ""
                    temp += var
                    flag = 1
                elif flag == 1:
                    if "Goalkeeper" in var or "Defender" in var or "Midfielder" in var or "Forward" in var:
                        temp = temp + " " + var
                        flag = 0
                        fout.write(temp + '\n')
                    else:
                        temp = temp + " " + var
            else:
                fout.write(var + '\n')

    fin.close()
    fout.close()



def removeSquadNumbers():
    # Removing squad numbers
    with open("MatchSquads-2014_final.txt", "r") as fin, open("MatchSquads_2014-final.txt", "w") as fout:
        for line in fin:
            var = str(line)
            var = var.rstrip('\n')
            if "Positions" not in var and "END,MATCH" not in var and "NEXT,TEAM" not in var and "..." not in var and "Substitutes" not in var:
                x = var.split(',')
                x.pop(0)
                new_var = ""
                for y in x:
                    if new_var == "":
                        new_var = y
                    else:
                        new_var = new_var + "," + y
                fout.write(new_var + '\n')
            else:
                fout.write(var + '\n')

    fin.close()
    fout.close()


def identifyPlayerNames():
    with open("MatchSquads_2014-final.txt","r") as fin, open("MatchSquads-2014_final.txt","w") as fout:
        for line in fin:
            var = str(line)
            var = var.rstrip('\n')
            if "Positions" not in var and "END,MATCH" not in var and "NEXT,TEAM" not in var and "..." not in var and "Substitutes" not in var:
                x = var.split(',')
                new_var = ""
                for y in x:
                    if "'" not in y and "Goalkeeper" not in y and "Defender" not in y and "Midfielder" not in y and "Forward" not in y:
                        if new_var == "":
                            new_var = new_var + y
                        else:
                            new_var = new_var + " " + y
                    else:
                        new_var = new_var + "," + y
                fout.write(new_var + '\n')
            else:
                fout.write(var + '\n')



def loadPlayerRatings(text_file):
    """

    :param text_file:
    :return:
    Function description: This function loads all the player ratings of a given year into a map, where the
    key is the team name and the value is the player name and rating.
    """
    global map2013
    global map2014
    global map2015

    with open(text_file,"r") as fin:
        for line in fin:
            x = line.split(',')
            ln = len(x)
            if ln > 4:
                #print "NEBUG:", x[4]
                map2014[x[1]] = [x[0], x[2], x[3],x[4]]
            else:
                map2014[x[1]] = [x[0],x[2],x[3]]


    fin.close()
    cnt = 0
    for i in map2014:
        cnt += 1
        print i,map2014[i]

    print cnt


def digInString(var):
    return any(char.isdigit() for char in var)

def findDig(var):
    ret = ''.join(c for c in var if c.isdigit())
    return ret

def editDistDP(str1, str2, m, n):
    dp = [[0 for x in range(n + 1)] for x in range(m + 1)]

    # Fill d[][] in bottom up manner
    for i in range(m + 1):
        for j in range(n + 1):
            if i == 0:
                dp[i][j] = j  # Min. operations = j
            elif j == 0:
                dp[i][j] = i  # Min. operations = i
            elif str1[i - 1] == str2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1]
            else:
                dp[i][j] = 1 + min(dp[i][j - 1],  # Insert
                                   dp[i - 1][j],  # Remove
                                   dp[i - 1][j - 1])  # Replace

    return dp[m][n]


def getMatch(name,team):
    ret = ""
    if name not in mNameTorName14:
        mn = 10000000
        for i in map2014:
            temp_team = ""
            if len(map2014[i]) > 3:
                #print "NEBUG:" , i , team
                if map2014[i][0] == team:
                    temp = editDistDP(name, i, len(name), len(i))
                    if temp < mn:
                        mn = temp
                        ret = i
                elif map2014[i][3] == team:
                    temp = editDistDP(name, i, len(name), len(i))
                    if temp < mn:
                        mn = temp
                        ret = i

                mNameTorName14[i] = 1
            elif map2014[i][0] == team:
                temp = editDistDP(name, i, len(name),len(i))
                if temp < mn:
                    mn = temp
                    ret = i

                mNameTorName14[i] = 1

    else:
        ret = name

    return ret



def calculateMatchRatings(text_file):
    cur_team = ""
    team_cnt = 0
    home_team = 0
    cur_team_def_rating = 0
    cur_team_mid_rating = 0
    cur_team_att_rating = 0
    cur_team_rating = 0
    starting_eleven_cnt = 0
    with open(text_file,"r") as fin,open("MatchSquadRatings2014.txt","w") as fout:
        for line in fin:
            var = str(line)
            var = var.rstrip('\n')
            if "Positions" in var:
                x = var.split(',')
                cur_team = x[0]
                if team_cnt > 0 and home_team%2 == 0:
                    temp_str = str(starting_eleven_cnt)
                    print "HOME_TEAM_RATING:", cur_team_rating
                    temp_str += "," + str(cur_team_rating)
                    print "HOME_ATT_RATING:", cur_team_att_rating
                    temp_str += "," + str(cur_team_att_rating)
                    print "HOME_MID_RATING:", cur_team_mid_rating
                    temp_str += "," + str(cur_team_mid_rating)
                    print "HOME_DEF_RATING:", cur_team_def_rating
                    temp_str += "," + str(cur_team_def_rating)
                    #fout.write(temp_str + "\n")

                    home_team = 1
                elif team_cnt > 0 and home_team%2 == 1:
                    print "AWAY_TEAM_PLAYERS:", starting_eleven_cnt
                    temp_str += "," + str(starting_eleven_cnt)
                    print "AWAY_TEAM_RATING:", cur_team_rating
                    temp_str += "," + str(cur_team_rating)
                    print "AWAY_ATT_RATING:", cur_team_att_rating
                    temp_str += "," + str(cur_team_att_rating)
                    print "AWAY_MID_RATING:", cur_team_mid_rating
                    temp_str += "," + str(cur_team_mid_rating)
                    print "AWAY_DEF_RATING:", cur_team_def_rating
                    temp_str += "," + str(cur_team_def_rating)
                    fout.write(temp_str + "\n")
                    home_team = 2

                starting_eleven_cnt = 0
                cur_team_def_rating = 0
                cur_team_mid_rating = 0
                cur_team_att_rating = 0
                cur_team_rating = 0
                team_cnt += 1
                print cur_team,

            elif "Positions" not in var and "END,MATCH" not in var and "NEXT,TEAM" not in var and "..." not in var and "Substitutes" not in var:
                substitute = digInString(var)
                #print "DEBUG: " , var
                if starting_eleven_cnt < 11:
                    starting_eleven_cnt += 1
                    x = var.split(',')
                    temp_name = x[0]
                    temp_name = temp_name.split(' ')
                    #print temp_name
                    if temp_name[-1] == "90" or temp_name[-1] == "45":
                        temp_name.pop()

                    fin_name = " ".join(temp_name)
                    #print fin_name
                    playerName = getMatch(fin_name,cur_team)
                    #print playerName
                    rating = int(map2014[playerName][1])
                    cat = str(map2014[playerName][2])
                    cat = cat.rstrip('\n')
                    if substitute == True:
                        #print "Subbed off at " , x[1]
                        sub_off_time = findDig(var)
                        sub_off_time = int(sub_off_time)
                        #print sub_off_time
                        #print playerName, "Subbed off", sub_off_time
                        #print sub_off_time
                        weighted_rating = float(sub_off_time)/90.0
                        weighted_rating = round(weighted_rating,3)
                        weighted_rating = rating*weighted_rating
                        #print weighted_rating
                        print playerName,weighted_rating
                        cur_team_rating += weighted_rating
                        if cat == "ATT":
                            cur_team_att_rating += weighted_rating
                        elif cat == "GK":
                            cur_team_def_rating += weighted_rating
                        elif cat == "DEF":
                            cur_team_def_rating += weighted_rating
                        elif cat == "MID":
                            cur_team_mid_rating += weighted_rating
                        else:
                            print "No position found for player", playerName , cat

                    else:
                        # print "TYPE",type(map2013[playerName][2])
                        print playerName, rating
                        cur_team_rating += rating
                        if cat == "ATT":
                            cur_team_att_rating += rating
                        elif cat == "GK":
                            cur_team_def_rating += rating
                        elif cat == "DEF":
                            cur_team_def_rating += rating
                        elif cat == "MID":
                            cur_team_mid_rating += rating
                        else:
                            print "No position found for player", playerName, cat

                            # print map2013[playerName][1], map2013[playerName][2]



                elif substitute == True:
                    #print "Subbed off at " , x[1]
                    sub_on_time = findDig(var)
                    sub_on_time = int(sub_on_time)
                    #print sub_off_time
                    #print sub_off_time

                    starting_eleven_cnt += 1
                    x = var.split(',')
                    temp_name = x[0]
                    temp_name = temp_name.split(' ')
                    # print temp_name
                    if temp_name[-1] == "90" or temp_name[-1] == "45":
                        temp_name.pop()

                    fin_name = " ".join(temp_name)
                    #print fin_name
                    playerName = getMatch(fin_name,cur_team)
                    #print playerName, "Subbed on", sub_on_time
                    rating = int(map2014[playerName][1])
                    weighted_rating = float(90 - sub_on_time) / 90.0
                    weighted_rating = round(weighted_rating,3)
                    if sub_on_time == 90:
                        weighted_rating = float(90-sub_on_time+1) / 90.0
                        weighted_rating = round(weighted_rating,3)
                    print weighted_rating
                    weighted_rating = rating * weighted_rating
                    print playerName,weighted_rating
                    #print "SUB RATING:", playerName, weighted_rating
                    cat = str(map2014[playerName][2])
                    cat = cat.rstrip('\n')
                    cur_team_rating += weighted_rating
                    if cat == "ATT":
                        cur_team_att_rating += weighted_rating
                    elif cat == "GK":
                        cur_team_def_rating += weighted_rating
                    elif cat == "DEF":
                        cur_team_def_rating += weighted_rating
                    elif cat == "MID":
                        cur_team_mid_rating += weighted_rating
                    else:
                        print "No position found for player", playerName, cat

                    #print map2013[playerName][1], map2013[playerName][2]


        print "AWAY_TEAM_PLAYERS:", starting_eleven_cnt
        temp_str += "," + str(starting_eleven_cnt)
        print "AWAY_TOTAL_TEAM_RATING:", cur_team_rating
        temp_str += "," + str(cur_team_rating)
        print "AWAY_ATT_RATING:", cur_team_att_rating
        temp_str += "," + str(cur_team_att_rating)
        print "AWAY_MID_RATING:", cur_team_mid_rating
        temp_str += "," + str(cur_team_mid_rating)
        print "AWAY_DEF_RATING:", cur_team_def_rating
        temp_str += "," + str(cur_team_def_rating)
        fout.write(temp_str + "\n")
        print "DEBUG:",team_cnt

def transferToCsv(data, fileName):

    """
    :param data:string
    :param fileName:string
    :param season:string
    :return:none

    This function takes the listoflists (data) and adds the corresponding matches for a particular seasons
    into the variable data. After that, the data variable is written line by line into the Scoreboard_all.csv file
    """

    with open(fileName, "r") as ins:
        for line in ins:
            val = str(line)
            #val = season + "," + val
            x = val.split(",")
            data.append(x)


#Text file open
#ratings_file = open("PlayerRatings-2013-Final.txt","r")

#cleanFile("MatchSquads-2015.txt")
#removeSquadNumbers()
#identifyPlayerNames()
loadPlayerRatings("PlayerRatings-2014-Final.txt")
calculateMatchRatings("MatchSquads-2014_final.txt")


data = []

# Initializing a blank .csv file
with open("MatchSquadRatings2014.csv", "wb") as csv_file:
    writer = csv.writer(csv_file, delimiter=',')
    for line in data:
        writer.writerow(line)



csv_file.close()

# Appending the Column data for the .csv file
data.append("HTP,HTR,HTAR,HTMR,HTDR,ATP,ATR,ATAR,ATMR,ATDR".split(","))

# Function calls
transferToCsv(data,"MatchSquadRatings2014.txt")

with open("MatchSquadRatings2014.csv", "ab") as csv_file:  # Opens the .csv file in append binary mode.
    writer = csv.writer(csv_file, delimiter=',')
    for line in data:
        writer.writerow(line)


csv_file.close()

csv_input = pd.read_csv('ScoreBoard_Detailed_2014.csv')
csv_input1 = pd.read_csv('MatchSquadRatings2014.csv')
csv_input['HTP'] = csv_input1['HTP']
csv_input['HTR'] = csv_input1['HTR']
csv_input['HTAR'] = csv_input1['HTAR']
csv_input['HTMR'] = csv_input1['HTMR']
csv_input['HTDR'] = csv_input1['HTDR']
csv_input['ATP'] = csv_input1['ATP']
csv_input['ATR'] = csv_input1['ATR']
csv_input['ATAR'] = csv_input1['ATAR']
csv_input['ATMR'] = csv_input1['ATMR']
csv_input['ATDR'] = csv_input1['ATDR']

csv_input.to_csv('ScoreBoardFinal2014.csv',index=False)

