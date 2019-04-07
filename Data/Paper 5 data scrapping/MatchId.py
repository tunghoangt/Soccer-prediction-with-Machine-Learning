import time

from selenium import webdriver
from selenium.webdriver.common.keys import Keys

browser = webdriver.Chrome()

browser.get("https://www.premierleague.com/results?co=1&se=42&cl=-1")
time.sleep(2)

elem = browser.find_element_by_tag_name("body")

no_of_pagedowns = 50

while no_of_pagedowns:
    elem.send_keys(Keys.PAGE_DOWN)
    time.sleep(0.5)
    no_of_pagedowns-=1

uls = browser.find_elements_by_class_name("matchList")
text_file = open("Matches-2015.txt", "w")
for ul in uls:
    post_elems = ul.find_elements_by_class_name("matchFixtureContainer")
    for post in post_elems:
        matchId = post.get_attribute("data-comp-match-item")
        text_file.write(matchId + "\n")


text_file.close()