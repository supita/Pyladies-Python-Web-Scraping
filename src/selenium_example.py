"""

@author Estela Alvarez
"""


from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import selenium.webdriver.support.ui as ui

from beautifulsoup_example import print_messages_info, extract_board_messages_info

import re


def get_webdriver():
    profile = webdriver.FirefoxProfile()
    profile.set_preference("general.useragent.override", "some UA string")
    browser = webdriver.Firefox(profile)

    return browser


def get_groups_name_from_query(browser, query="js montreal"):
    browser.get("http://www.meetup.com/find/?radius=25")

    search_box = browser.find_element_by_id("mainKeywords")
    search_box.send_keys(query)
    search_box.send_keys(Keys.RETURN)

    group_name_re = re.compile(r"http://www.meetup.com/(.*)/")

    groups_name = []
    for link in browser.find_elements_by_xpath(
            '//ul[contains(@class, "search-result")]//a[contains(@class, "display-none") and contains(@href, "http://www.meetup.com/")]'):

        match = group_name_re.search(link.get_attribute("href"))

        if match:
            groups_name.append(match.group(1))

    return groups_name


def print_discussions_info_from_given_groups(browser, groups_name=[]):
    for group in groups_name:
        browser.get("http://www.meetup.com/%s/messages/boards/" % group)
        try:
            ui.WebDriverWait(browser, 10).until(
                EC.presence_of_element_located((By.ID, "threadActionForm")))
            if "Montreal-MUG" in group:
                print """
                =======================================================
                      BOARD INFO EXTRACTION THROUGH BeautifulSoup
                =======================================================

                """
                messages = extract_board_messages_info(browser.page_source)
            else:
                messages = get_messages_from_board(browser)
            print_messages_info(messages)
        except:
            browser.quit()


def get_messages_from_board(browser):
    messages = []

    for row in browser.find_elements_by_xpath('.//form[@id="threadActionForm"]//tbody//tr'):
        tds = row.find_elements_by_tag_name("td")

        thread = {}
        thread["url"] = tds[2].find_element_by_tag_name("a").get_attribute("href")
        thread["subject"] = tds[2].text

        thread["author"] = tds[3].text
        thread["replies"] = int(tds[4].text)
        thread["views"] = int(tds[5].text)
        last_replied = tds[6].text.split("\n")

        thread["last_replied"] = {
            "time": last_replied[0].strip(),
            "date": last_replied[1].strip(),
            "by": last_replied[2].replace("by:", "").strip()
        }

        messages.append(thread)
    return messages


def main():
    browser = get_webdriver()
    groups_name = get_groups_name_from_query(browser)

    print_discussions_info_from_given_groups(browser, groups_name)

    browser.close()

if __name__ == '__main__':
    main()
