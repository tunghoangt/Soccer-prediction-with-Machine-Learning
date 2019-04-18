import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import StaleElementReferenceException


"""

    Script description:

    This python script uses the output file Matches-2103.txt obtained from SeleniumScraper-Detailed.py
    to  fetch the stats for every match in a particular season (2013 onwards). The Matches-2013.txt file
    contains the match ids for every match in a season. Using the id, the url for the match is constructed.
    Then, a request to open the url is sent. Inside the page, a click on the Stats tab is automated and then
    from the Stats tab, all the Stats for the current match is fetched and stored in a text file called
    Stats-2013.txt along with the Match ID in a formatted way for further use.

"""

browser = webdriver.Chrome()
text_file = open("Stats-2015.txt","w")

with open("Matches-2015.txt", "r") as ins:
    for line in ins:
        try:
            browser.get("https://www.premierleague.com/match/" + line)
            elem = browser.find_element_by_tag_name("body")
            elem.send_keys(Keys.PAGE_DOWN)
            time.sleep(1)
            tab = browser.find_element_by_class_name("tablist")
            stats = tab.find_element_by_xpath(".//li[not(@class)]")
            stats.click()
            #print stats.text
            #for tab in tabs:
            #    print tab.text
            #    if tab.text == "Stats":
            #        print "Hello"
            #        tab.click()

            time.sleep(1)
            stats = browser.find_element_by_class_name("matchCentreStatsContainer")
            text_file.write("Match: " + line)
            text_file.write(stats.text + "\n\n")
        except StaleElementReferenceException:
            text_file.write("Match: " + line)
            for x in range(0, 10):
                text_file.write("XX-XX-,XX-XX-,XX-XX\n")
            text_file.write("Match: " + line)
            text_file.write(stats.text + "\n\n")

            text_file.write("\n\n")
        except:
            print line

