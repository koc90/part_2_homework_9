# Wybierz bibliotekę BeautifulSoup lub framework Scrapy. Następnie wykonaj scraping strony http://quotes.toscrape.com. Twoim celem jest uzyskanie dwóch plików: qoutes.json, w którym należy umieścić wszystkie informacje o cytatach ze wszystkich stron witryny oraz authors.json, w którym znajdziesz informacje o autorach tych cytatów. Struktura plików json powinna być dokładnie taka sama jak w poprzednim zadaniu domowym. Wykonaj wcześniej napisane skrypty, aby przesłać pliki json do bazy danych w chmurze dla otrzymanych plików. Poprzednie zadanie domowe powinno działać poprawnie z nowo otrzymaną bazą danych.


import quotes, authors, json
from url import url


def data_load(file) -> list[dict]:
    with open(file, "r", encoding="utf-8") as file:
        data_list = json.load(file)

    return data_list


def data_save(file: str, data: list[dict]):
    with open(file, "w", encoding="utf-8") as file:
        json.dump(data, file)


def save_author_urls_to_file(author_urls):
    with open("authors_url.txt", "w") as file:
        for author_url in author_urls:
            print(author_url, file=file)


def load_author_urls_from_file():
    author_urls = []
    with open("authors_url.txt", "r") as file:
        author_urls_with_nl = file.readlines()
    for author_url in author_urls_with_nl:
        author_urls.append(author_url.replace("\n", ""))

    return author_urls


def main():

    (quotes_2_json, author_url_ends) = quotes.quotes(url)
    data_save("quotes.json", quotes_2_json)

    author_urls = []

    for author_url_end in author_url_ends:
        author_urls.append(url + author_url_end)

    # author_urls = load_author_urls_from_file()
    # print(author_urls)

    authors_2_json = authors.authors(author_urls)
    data_save("authors.json", authors_2_json)

    # authors_2_json = authors.authors_async(author_urls)
    # data_save("authors.json", authors_2_json)
    # NIE DZIAŁA :(


if __name__ == "__main__":
    print("\n\n")
    main()
    # Poprzednie zadanie zadziałało z uzyskanymi plikami *.json
