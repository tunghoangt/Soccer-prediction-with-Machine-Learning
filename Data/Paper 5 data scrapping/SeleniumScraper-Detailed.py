import time

from selenium import webdriver
from selenium.webdriver.common.keys import Keys

browser = webdriver.Chrome()

browser.get("https://www.premierleague.com/results?co=1&se=22&cl=-1")
time.sleep(2)

elem = browser.find_element_by_tag_name("body")

no_of_pagedowns = 50

while no_of_pagedowns:
    elem.send_keys(Keys.PAGE_DOWN)
    time.sleep(0.2)
    no_of_pagedowns-=1

post_elems = browser.find_elements_by_class_name("matchFixtureContainer")
text_file = open("MatchId.txt", "w")
print 'Hello'
for post in post_elems:
    #text_file.write(str(post.get_attribute("data-comp-match-item")) + "\n")
    text_file.write(post.text + "\n")
    text_file.write(str(post.get_attribute("data-comp-match-item")) + "\n")
text_file.close()

out_file = open("Matches.txt","w")

with open("Output.txt", "r") as ins:
    for line in ins:
        if line.startswith("9"):
            out_file.write(line)

out_file.close()

