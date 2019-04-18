import time
import sys
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from itertools import islice

"""
    _author_ = "Shriya Mishra"

    Script Description

"""
"""
def fetchSquadList(col_name,text_file):
    time.sleep(3)
    columns = browser.find_elements_by_class_name(col_name)
    for column in columns:
        players = column.find_element_by_class_name("player")
        col_header = players.find_element_by_class_name("position")
        print "TEAM"
        text_file.write("*************** " + col_header.text + "*****************\n")
        col_list = column.find_elements_by_class_name("info")
        time.sleep(3)
        cnt = 0
        for line in col_list:
            text_file.write(line.find_element_by_class_name("name").text + "  -  " + line.find_element_by_class_name(
                "position").text + '\n')
            """
"""
            if cnt < 12:
                try:
                    sub_out = line.find_element_by_css_selector(".icn.sub-off")
                    text_file.write(line.find_element_by_class_name("name").text + "  -  " + line.find_element_by_class_name(
                            "position").text + " so" + '\n')

                    cnt += 1
                except:
                    text_file.write(line.find_element_by_class_name("name").text + "  -  " + line.find_element_by_class_name(
                        "position").text + '\n')
                    cnt += 1

            else:
                try:
                    sub_in = line.find_element_by_css_selector(".icn.sub-on")
                    if sub_in is not None:
                        text_file.write(line.find_element_by_class_name("name").text + "  -  " + line.find_element_by_class_name(
                            "position").text+" si " + '\n')
                except:
                    print "Fetch failed Sub-on"
            """
"""
        text_file.write("--------------END MATCH-----------------------\n\n")

"""

browser = webdriver.Chrome()
#orig_stdout = sys.stdout
#sys.stdout = f
#text_file = open("MatchSquads-2013.txt",'w')
#getSquadUrl("Matches-2013.txt")
with open("Matches-2015.txt", 'r') as ins, open('MatchSquads-2015.txt', 'w') as f:
    # ins = list(islice(ins, 2))
    team1 = ""
    team2 = ""
    for line in ins:
        try:

            browser.get("https://www.premierleague.com/match/" + line)

            time.sleep(3)
            tab = browser.find_element_by_class_name("matchCentreSquadLabelContainer")
            # elem = browser.find_elements_by_tag_name("body")
            # time.sleep(2)
            tab.click()
            time.sleep(10)
            cnt = 10
            while cnt:
                tab.send_keys(Keys.PAGE_DOWN)
                time.sleep(0.2)
                cnt -= 1
            # tab.send_keys(Keys.PAGE_DOWN)
            # tab.send_keys(Keys.PAGE_DOWN)
            # fetchSquadList("matchLineupTeamContainer",text_file)
            team = browser.find_element_by_css_selector(".col-4-m.right")
            # text_file.write(str(team.text)  + '\n')
            team2 = team.text
            # print team2
            # text_file.write(var + '\n')
            time.sleep(2)
            team = browser.find_element_by_css_selector(".col-4-m ")
            time.sleep(2)
            # text_file.write(team.text + '\n')
            team1 = team.text
            # print team1
            f.write(team1.encode('utf-8') + '\n')
            f.write('..........\n')
            f.write("NEXT TEAM \n")
            f.write('..........\n')
            f.write(team2.encode('utf-8') + '\n')
            # text_file.close()
            # text_file.write(str(temp) + '\n')
            f.write("-----------------------END MATCH--------------------------------------\n")
            """

            players = team.find_elements_by_class_name("player")
            for player in players:
                #players = squad.find_elements_by_tag_name("li")
                info = player.find_element_by_class_name("info")
                text_file.write(info.text + '\n')
            #fetchSquadList(".col-4-m.right",text_file)

            text_file.write("Next team \n")
            """
        except:
            time.sleep(240)
            pass
            print "failed : " + line


#sys.stdout = orig_stdout
f.close()


