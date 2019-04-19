#! usr/bin/env python3
import praw
from config import REDDIT_API_AUTH_PARAMS
import pandas as pd
import datetime as dt
import json
from PIL import Image
import re
import requests
from bs4 import BeautifulSoup, NavigableString, Tag
from bs4.element import Comment

##
## HELPERS
##
def tag_visible(element):
    if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]']:
        return False
    if isinstance(element, Comment):
        return False
    return True


##
## VANILLA SCRAPER
##
data = []

## IBSPATIENTS.ORG
page = requests.get(url="https://www.aboutibs.org/living-with-ibs-main/personal-stories.html")
soup = BeautifulSoup(page.text)
quotes = soup.find_all("blockquote")
for quote in quotes:
    data.append({
        "source": "www.aboutibs.org",
        "body": " ".join([item.text for item in quote.find_all("p")]),
        "condition": "IBS",
        "geolocation": None,
        "date": None
    })

## IFFGD.ORG
root_url = "https://www.iffgd.org"
# page = requests.get(url="https://www.iffgd.org/stay-connected/personal-stories-list.html")
stories_file = open(
    file="./forum_data/ifffgd_personal_stories_list.htm",
    mode="r"
)
soup = BeautifulSoup(stories_file)
quotes = soup.find_all("a", text="more")

for quote in quotes:
    story_page = requests.get(root_url + quote.get("href"))
    story_soup = BeautifulSoup(story_page.text)

    story_date_text = story_soup.find_all("span", {"class": "stry-date"})[0].text
    condition_text = story_soup.find_all("span", {"class": "stry-author"})[0].text
    body = story_soup.find_all("div", {"class": "article-content"})[0]
    visible_texts = filter(tag_visible, body.find_all(text=True))
    body_text = u" ".join(t.strip() for t in visible_texts).strip()

    data.append({
        "source": "www.iffgd.org",
        "body": body_text,
        "condition": condition_text,
        "geolocation": None,
        "date": story_date_text
    })

## IBSTALES.COM
root_url = "https://www.ibstales.com/"
page = requests.get(url="https://www.ibstales.com/read-tales.htm")
soup = BeautifulSoup(page.text)
sub_links = [anchor.get("href") for anchor in soup.find_all("a", text=re.compile(r"Page\s"))]

for sub_link in sub_links:
    subpage = requests.get(url=root_url+sub_link)
    subsoup = BeautifulSoup(subpage.text)

    condition_text = subsoup.find("h1", {"cwidth":"758"}).text

    for header in subsoup.find_all('h2'):
        nextNode = header
        body_text = ""
        while True:
            nextNode = nextNode.nextSibling
            if nextNode is None:
                break
            if isinstance(nextNode, NavigableString): pass
                # print (nextNode.strip())
            if isinstance(nextNode, Tag):
                if nextNode.name == "h2":
                    data.append({
                        "source": "www.ibstales.com",
                        "body": body_text,
                        "condition": condition_text,
                        "geolocation": None,
                        "date": None
                    })
                    body_text = ""
                    break
                body_text += nextNode.get_text(strip=True).strip()



df = pd.DataFrame(data)
df.to_csv(index=False, path_or_buf="data/scraped_data.csv")
