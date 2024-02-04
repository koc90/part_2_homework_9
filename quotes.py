import requests, http, logging
from bs4 import BeautifulSoup


URL = "https://quotes.toscrape.com/"


def scrap_quote_from_soup(body: BeautifulSoup):

    list_of_quotes = []
    author_url_ends = set()
    divs = body.find_all("div", class_="quote")

    for div in divs:
        quote = div.find("span", class_="text").text
        author = div.find("small", class_="author").text
        tags = []
        for tag in div.find_all("a", class_="tag"):
            tags.append(tag.text)
        quote_dict = {"tags": tags, "author": author, "quote": quote}
        list_of_quotes.append(quote_dict)

        author_url_end = div.find("a", class_=None).get_attribute_list(key="href")[0][
            1::
        ]
        author_url_ends.add(author_url_end)

    return list_of_quotes, author_url_ends


def quotes(first_page_url):
    quotes_json = []
    author_url_ends = set()

    new_url = first_page_url
    while True:
        logging.debug(new_url)
        response = requests.get(new_url)
        if response.status_code == http.HTTPStatus.OK:
            soup = BeautifulSoup(response.text, "lxml")
            body = soup.find("body")

            (list_of_quotes, author_url_ends_part) = scrap_quote_from_soup(body)
            quotes_json.extend(list_of_quotes)
            author_url_ends = author_url_ends.union(author_url_ends_part)

            next_li = body.find("li", class_="next")

            if next_li:
                ext_url = next_li.find("a").get_attribute_list(key="href")[0][1::]
                new_url = URL + ext_url

            else:
                break

        else:
            logging.error(f"Mission failed. Status code: {response.status_code}")

    return quotes_json, author_url_ends
