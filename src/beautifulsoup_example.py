""" Little scraper to extract the information from the messages listed under
PyLadies Discussion board using BeautifulSoup

@author Estela Alvarez
"""

import requests
from bs4 import BeautifulSoup

import re


def get_pyladies_discussions_page_source():
    response = requests.get('http://www.meetup.com/PyLadiesMTL/messages/boards/')

    return response.text


def extract_board_messages_info(page_source):
    soup = BeautifulSoup(page_source, "html.parser")

    thread_links = soup.find_all("a",
        href=re.compile("http://www.meetup.com/\S+/messages/boards/thread/"))

    messages = []
    for link in thread_links:
        thread = {}
        thread["url"] = link["href"]
        thread["subject"] = link.text.strip()

        other_cells = link.find_parent("td").find_next_siblings("td")

        thread["author"] = other_cells[0].text.strip()
        thread["replies"] = int(other_cells[1].text)
        thread["views"] = int(other_cells[2].text)
        last_replied = other_cells[3].contents

        thread["last_replied"] = {
            "time": last_replied[0].strip(),
            "date": last_replied[2].strip(),
            "by": last_replied[5].text.replace("by:", "").strip()
        }

        messages.append(thread)

    return messages


def print_messages_info(messages):
    print("**********************************************")
    print("         Found %d discusions posted" % len(messages))
    print("**********************************************")

    i = 1

    for message in messages:
        print(""" 
                ==============================
                        Message #%d
                ==============================""" % i)
        print("Author: %s" % message["author"])
        print("Subject: %s" % message["subject"])
        print("Discussion Url: %s" % message["url"])
        print("Times viewed: %d" % message["views"])
        if message["replies"]:
            print("     Number of replies: %d" % message["replies"])
            print("     Last replied on %s by %s" %
                  (message["last_replied"]["date"], message["last_replied"]["by"]))
        else:
            print("     There's no replies for this topic!")


        i += 1


def main():
    page_source = get_pyladies_discussions_page_source()
    messages = extract_board_messages_info(page_source)
    print_messages_info(messages)

if __name__ == '__main__':
    main()
