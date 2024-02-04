import quotes
import authors
import json


URL = "https://quotes.toscrape.com/"


def data_load(file) -> list[dict]:
    with open(file, "r", encoding="utf-8") as file:
        data_list = json.load(file)

    return data_list


def data_save(file: str, data: list[dict]):
    with open(file, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)


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

    quotes_2_json, author_url_ends = quotes.quotes(URL)
    data_save("quotes.json", quotes_2_json)

    author_urls = []

    for author_url_end in author_url_ends:
        author_urls.append(URL + author_url_end)

    authors_2_json = authors.authors_async(author_urls)
    data_save("authors.json", authors_2_json)


if __name__ == "__main__":
    print("\n\n")
    main()
    # Poprzednie zadanie zadziałało z uzyskanymi plikami *.json
