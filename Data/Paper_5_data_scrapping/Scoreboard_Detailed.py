import csv
from collections import OrderedDict

"""

Script Description:



"""

def transferToCsv(data,fileName):

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
            val = str(line).rstrip('\n')
            #print val
            x = val.split(",")
            #print x
            data.append(x)

    #print data

def convertToCSV(fileName):
    data = []

    # Initializing a blank .csv file
    with open("ScoreBoard_Detailed_2014.csv", "wb") as csv_file:
        writer = csv.writer(csv_file, delimiter=',')
        for line in data:
            writer.writerow(line)

    csv_file.close()

    # Appending the Column data for the .csv file
    data.append("MId,Home Team,Home Team Goals,Away Team Goals,Away Team,Home Poss,Away Poss,Home ShotsT,Away ShotsT,Home Shots,Away Shots,Home Touches,Away Touches,Home Passes,Away Passes,Home Tackles,Away Tackles,Home Clearances,Away Clearances,Home Corners,Away Corners,Home Offsides,Away Offsides".split(","))
    transferToCsv(data,fileName)
    with open("ScoreBoard_Detailed_2014.csv", "ab") as csv_file:  # Opens the .csv file in append binary mode.
        writer = csv.writer(csv_file, delimiter=',')
        for line in data:
            #print line
            writer.writerow(line)

    csv_file.close()


def addStats(val,matchId):
    myList = [item for item in val.split('\n')]
    newString = ''.join(myList)
    #print matchId
    statsList[matchId] = newString

statsList = OrderedDict()

with open("Stats-2014.txt","r") as ins:
    # print "A" + cnt
    cnt = 0
    val = ","
    matchId = ""
    for line in ins:
        # print cnt
        rVal = str(line)
        x = rVal.split(',')
        #print x
        if cnt == 0:
            print x
            cnt += 1
            #val = val + x[1] + ","
            #print x[1].rstrip('\n')
            matchId = x[1].rstrip('\n')
            #print matchId
        else:
            print x
            val = val + x[0] + "," + x[2] + ","
            #print x[0] + "," + x[2] + ",".rstrip('\n')
            cnt += 1
            if cnt == 10:
                #print val
                addStats(val,matchId)
                val = ","
                cnt = 0
                #break


for i in statsList:
    print i, statsList[i]


text_file = open("ScoreBoard_Detailed_2014.txt","w")
with open("ScoreBoard_2014.txt","r") as ins:
    idx = 0
    for line in ins:
        value_at_index = statsList.values()[idx]
        key_at_index = statsList.keys()[idx]
        val = str(line).rstrip('\n')
        val = val.rstrip(',')
        val = key_at_index + "," + val
        val = val + value_at_index
        val = val.rstrip(',')
        text_file.write(val + '\n')
        idx += 1

text_file.close()
convertToCSV("ScoreBoard_Detailed_2014.txt")


