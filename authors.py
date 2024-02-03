from bs4 import BeautifulSoup
import asyncio, aiohttp, http, logging, requests


logging.basicConfig(level=logging.DEBUG)


def scrap_author_from_soup(body: BeautifulSoup):

    list_of_authors = []
    divs = body.find_all("div", class_="author-details")

    for div in divs:
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
        list_of_authors.append(author_dict)

    return list_of_authors


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


async def get_response_make_soup_async(url):
    logging.debug(url)

    body = None

    async with aiohttp.ClientSession() as session:
        logging.debug(f"{url} session opened")
        print(type(session))
        print(dir(session))
        try:
            print(session.get(url))
            async with session.get(url) as response:
                logging.debug(f"{url} response received")
                if response.status == http.HTTPStatus.OK:
                    logging.debug(f"{url} response status: 200")
                    soup = await BeautifulSoup(response.text, "lxml")
                    body = soup.find("body")

                else:
                    logging.error(f"Mission failed. Status code: {response.status}")
                    body = None
        except Exception as e:
            print(e)

            # Cannot connect to host quotes.toscrape.com:443 ssl:True [SSLCertVerificationError: (1, '[SSL: CERTIFICATE_VERIFY_FAILED] certificate verify
            # failed: certificate has expired (_ssl.c:1006)')]

    return body


async def prepare_ingredients_for_soups(urls):
    make_soups = []
    for url in urls:
        make_soups.append(get_response_make_soup_async(url))

    result = asyncio.gather(*make_soups)
    logging.debug("Soup tasks gathered")
    return await result


def authors(urls):
    authors_json = []
    for url in urls:
        body = get_response_make_soup(url)
        list_of_authors = scrap_author_from_soup(body)
        authors_json.extend(list_of_authors)

    return authors_json


def authors_async(urls):
    authors_json = []
    ingredients_for_soups = prepare_ingredients_for_soups(urls)
    logging.debug(f"ingredients_for_soups: {ingredients_for_soups}")
    soups = asyncio.run(ingredients_for_soups)
    is_soups_list = isinstance(soups, list)
    logging.debug(
        f"Tasks done, results should be a list. Is results a list: {is_soups_list}"
    )
    for soup in soups:
        list_of_authors = scrap_author_from_soup(soup)
        authors_json.extend(list_of_authors)

    return authors_json


if __name__ == "__main__":
    # próby
    new_url = "https://quotes.toscrape.com/author/J-K-Rowling/"
    response = requests.get(new_url)
    soup = BeautifulSoup(response.text, "lxml")
    body = soup.find("body")

    list_2_json = scrap_author_from_soup(body)
    print(list_2_json)
