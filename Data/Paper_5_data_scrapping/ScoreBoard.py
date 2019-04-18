import csv

"""
    Script description:

    This piece of code formats the results for the seasons(2013 - 2015) from the files Output-XXXX(XXXX = 2013 - 2015).
    The result is in ScoreBoard_XXXX.txt which is then converted to .csv file. The csv file will be used for further
    data analysis.

"""


def transferToCsv(data,fileName,season):

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
            val = season + "," + val
            x = val.split(",")
            data.append(x)


with open("Output-2015.txt", "r") as ins:
    ctr = 0
    s_line = ""
    text_file = open("ScoreBoard_2015.txt", "w")
    for line in ins:
        val = str(line)
        val = val.replace("-", ",")
        val = val.rstrip("\n")
        s_line += val + ","
        ctr += 1
        #print s_line
        if ctr == 3:
            text_file.write(s_line + "\n")
            ctr = 0.
            s_line = ""


text_file.close()
data = []

# Initializing a blank .csv file
with open("Scoreboard_all.csv", "wb") as csv_file:
    writer = csv.writer(csv_file, delimiter=',')
    for line in data:
        writer.writerow(line)


csv_file.close()

# Appending the Column data for the .csv file
data.append("Season,Home Team,Home Team Goals, Away Team Goals, Away Team".split(","))

# Function calls
transferToCsv(data,"Scoreboard_2013.txt","2013")
transferToCsv(data,"Scoreboard_2014.txt","2014")
transferToCsv(data,"Scoreboard_2015.txt","2015")

with open("Scoreboard_all.csv", "ab") as csv_file:  # Opens the .csv file in append binary mode.
    writer = csv.writer(csv_file, delimiter=',')
    for line in data:
        writer.writerow(line)


csv_file.close()