import time
import csv
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

"""
    _author_ = "Sourabh Swain"
    Script Description:
    This python script fetches each premier league player's EA Sports FIFA ratings for all seasons
    from 2013 onwards. The script scrapes data from the site www.fifaindex.com. The task is achieved by
    performing two tasks - fetching each club's url from the season page & then fetching player ratings
    for each player in the club page.


"""


def getClubLinks(url):
    """

    :param url: string
    :return: none

    This function parses the url, fetches the club url links from the page and stores
    them in a text file. First, we find elements using an id.

    """
    text_file = open("FIFA_Club_Links-2015.txt","w")
    browser.get(url)
    time.sleep(0.5)
    table = browser.find_element_by_id("no-more-tables")
    names = table.find_elements_by_tag_name("a")
    items = set()
    for x in names:
        str = x.get_attribute("href")
        if "https://www.fifaindex.com/team/" in str:
            if str not in items:
                items.add(str)
                text_file.write(x.get_attribute("title") + "," + str + "\n")
                #print str
                #print x.get_attribute("title")



def getPlayerRatings(fileName):
    """

    :param fileName: String
    :return: none

    File Description:
    This function reads the club urls from the text file obtained from getClubLinks function and then fetches
    the ratings of each player for each club by going to the respective url of the club. The output is written
    onto a text file called PlayerRatings-XXXX.txt.

    """
    text_file = open("PlayerRatings-2015.txt","w")
    with open(fileName,"r") as ins:
        for line in ins:
            str1 = line.split(',')
            browser.get(str1[1])
            time.sleep(0.1)
            table = browser.find_element_by_id("no-more-tables")
            body = table.find_element_by_tag_name("tbody")
            rows = body.find_elements_by_tag_name("tr")
            for x in rows:
                data = x.find_elements_by_tag_name("td")
                name = ''.encode('utf-8')
                name = name.encode('utf-8')
                position = ''.encode('utf-8')
                rating = ''.encode('utf-8')
                for y in data:
                    str2 = y.get_attribute("data-title")
                    if str2 == "Name":
                        name = y.text.encode('utf-8')
                        #text_file.write(y.text.encode('utf-8') + " ")
                    elif str2 == "OVR / POT":
                        #text_file.write(y.text.encode('utf-8') + " ")
                        position = y.text.encode('utf-8')
                    elif str2 == "Preferred Positions":
                        rating = y.text.encode('utf-8')
                        #rating = rating[:2]
                        #text_file.write(y.text.encode('utf-8') + "\n")

                text_file.write(str1[0] + ',' + name + ',' + position + ',' + rating[:2] + '\n')

    text_file.close()


def cleanRating(fileName):
    """

    :param fileName: String
    :return: none

    Function description:
    This function arranges the scraped data (Team, Name, Position, Rating) in an arranged way and writes
    them into a text file.

    """
    text_file = open("PlayerRatings-2015-Final.txt","w")
    with open(fileName,"r+") as ins:
        for line in ins:
            str1 = line.split(',')
            rating = str1[2]
            temp = rating
            rating = rating[:2]
            text_file.write(line.replace(temp,rating))


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
            x = val.split(",")
            #print x
            data.append(x)



def convertToCSV(fileName):
    data = []

    # Initializing a blank .csv file
    with open("PlayerRatings-2015.csv", "wb") as csv_file:
        writer = csv.writer(csv_file, delimiter=',')
        for line in data:
            writer.writerow(line)

    csv_file.close()

    # Appending the Column data for the .csv file
    data.append("Team,Name,Rating,Position".split(","))
    transferToCsv(data,fileName)
    with open("PlayerRatings-2015.csv", "ab") as csv_file:  # Opens the .csv file in append binary mode.
        writer = csv.writer(csv_file, delimiter=',')
        for line in data:
            #print line
            writer.writerow(line)

    csv_file.close()



browser = webdriver.Chrome()
#getClubLinks("https://www.fifaindex.com/teams/fifa16_73/?league=13")
#getPlayerRatings("FIFA_Club_Links-2015.txt")
#cleanRating("PlayerRatings-2015.txt")
convertToCSV("PlayerRatings-2015-Final.txt")
