import asyncio
import http
import logging
import requests


from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime


logging.basicConfig(level=logging.DEBUG)


def scrap_author_from_soup(body: BeautifulSoup):

    div = body.find("div", class_="author-details")

    fullname = div.find("h3", class_="author-title").text
    born_date = div.find("span", class_="author-born-date").text
    born_location = div.find("span", class_="author-born-location").text
    description = div.find("div", class_="author-description").text

    author_dict = {
        "fullname": fullname,
        "born_date": born_date,
        "born_location": born_location,
        "description": description,
    }

    return author_dict


def get_response_make_soup(url):
    logging.debug(url)
    response = requests.get(url)
    if response.status_code == http.HTTPStatus.OK:
        soup = BeautifulSoup(response.text, "lxml")
        body = soup.find("body")
    else:
        logging.error(f"Mission failed. Status code: {response.status_code}")
        body = None

    return body


async def get_response_make_soup_async(urls):
    loop = asyncio.get_running_loop()
    num_urls = len(urls)

    with ThreadPoolExecutor(num_urls) as pool:
        futures = [
            loop.run_in_executor(pool, get_response_make_soup, url) for url in urls
        ]
        bodies = await asyncio.gather(*futures, return_exceptions=True)
        return bodies


def authors(urls):
    authors_json = []

    start = datetime.now()
    for url in urls:
        body = get_response_make_soup(url)
        author_dict = scrap_author_from_soup(body)
        authors_json.append(author_dict)

    end = datetime.now()
    logging.debug(f"\nauthors executed in {end - start}\n\n")
    with open("times.txt", "a") as f:
        print(
            f"\nauthors started at {start}\nauthors ended at {end}\nauthors executed in {end - start}\n\n",
            file=f,
        )

    return authors_json


def authors_async(urls):
    authors_json = []
    start = datetime.now()
    bodies = asyncio.run(get_response_make_soup_async(urls))

    for body in bodies:
        author_dict = scrap_author_from_soup(body)
        authors_json.append(author_dict)

    end = datetime.now()
    logging.debug(f"\nauthors_async executed in {end - start}\n\n")
    with open("times.txt", "a") as f:
        print(
            f"\nauthors_async started at {start}\nauthors_async ended at {end}\nauthors_async executed in {end - start}\n\n",
            file=f,
        )
    return authors_json
