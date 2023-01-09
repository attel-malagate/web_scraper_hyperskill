import requests
from bs4 import BeautifulSoup
import logging
import string
import os


def update_file_name(_s):
    new_name = ""
    for char in _s:
        if char in string.punctuation:
            new_name += ""
        elif char == " ":
            new_name += "_"
        else:
            new_name += char
    return new_name + ".txt"


def make_dirs(_n):
    for i in range(0, _n):
        os.mkdir(f"Page_{i+1}")


n_pages = int(input())
user_type = input()


def scrape_page(_type, _n):
    logging.basicConfig(level="INFO")
    seed_page = "https://www.nature.com/nature/articles?sort=PubDate&year=2020"
    for page in range(0, _n):
        r = requests.get(seed_page + f"&page={page+1}", headers={'Accept-Language': 'en-US,en;q=0.5'})
        logging.debug("Request Status_code: ", r.status_code)
    # if r.status_code == 200 and "title" in user_input:
        if r.status_code == 200:
            soup = BeautifulSoup(r.content, 'html.parser')
            logging.debug(type(soup))

            articles_a_tags = soup.find_all("a", {"data-track-action": "view article"})
            types = soup.find_all("span", {"class": "c-meta__type"})
            types_text = [item.get_text() for item in types]
            user_article_type = [articles_a_tags[i].get("href") for i, item in enumerate(types_text) if item == _type]
            articles_request_dict = {f"soup{i}": BeautifulSoup(requests.get(f"https://www.nature.com{item}", headers={'Accept-Language': 'en-US,en;q=0.5'}).content, "html.parser") for i, item in enumerate(user_article_type)}
            titles_dict = {f"title{i}": item.find("h1", "c-article-magazine-title").text for i, item in
                       enumerate(articles_request_dict.values())}
            file_names = [update_file_name(item) for item in titles_dict.values()]
            content_dict = {file_names[i]: item.find("div", {"class": "c-article-body"}).text.strip("\n") for i, item in
                        enumerate(articles_request_dict.values())}

        else:
            print(f"The URL returned {r.status_code}!")

        for item in content_dict:
            for k in range(_n):
                with open(f"Page_{k+1}/{item}", "wb") as file:
                    file.write(bytes(content_dict[item], encoding="utf-8"))
        print("Saved all articles")


make_dirs(n_pages)
scrape_page(user_type, n_pages)
