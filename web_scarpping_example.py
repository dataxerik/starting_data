from bs4 import BeautifulSoup
import requests
import re
from time import sleep
from collections import Counter
import matplotlib.pyplot as plt


def play():
    html = requests.get("http://www.example.com").text
    soup = BeautifulSoup(html, 'html5lib')

    first_paragraph = soup.find('p')  # or just soup.p

    first_paragraph_text = soup.p.text
    first_paragraph_words = soup.p.text.split()

    first_paragraph_id = soup.p['id']  # raises KeyError if no 'id'
    first_paragraph_id2 = soup.p.get('id')  # returns None if no 'id'

    all_paragraphs = soup.find_all('p')  # or just soup('p')
    paragraphs_with_ids = [p for p in soup('p') if p.get('id')]

    important_paragraphs = soup('p', {'class': 'important'})
    important_paragraphs2 = soup('p', 'important')
    important_paragraphs3 = [p for p in soup('p')
                             if 'important' in p.get('class', [])]


def oreilly_example():
    url = "http:// shop.oreilly.com/ category/ browse-subjects/" + \
          "data.do? sortby = publicationDate& page = 1"

    soup = BeautifulSoup(requests.get(url).text, 'html5lib')

    tds = soup('td', 'thumbtext')
    print(len(tds))

    print(len([td for td in tds if not is_video(td)]))

    #title = td.find("div", "thumbheader").a.text


def is_video(td):
    """it's a video if ti has exactly one pricelabel, and if the stripped
    text insde that pricelabel starts with 'Video'"""
    pricelabels = td('span', 'pricelabel')
    return (len(pricelabels) == 1 and
            pricelabels[0].text.strip().startswith("Video"))


def book_info(td):
    """given a BeautifulSoup <td> Tag representing a book,
    extract the book's details and return a dict"""

    title = td.find("div", "thumbheader").a.text
    by_author = td.find("div", "AuthorName").text
    authors = [x.strip() for x in re.sub("^By ", "", by_author).split(",")]
    isbn_link = td.find("div", "thumbheader").a.get("href")
    isbn = re.match("/product/(.*)\.do", isbn_link).groups()[0]
    date = td.find("span", "directorydate").text.strip()

    return {
        "title": title,
        "authors": authors,
        "isbn": isbn,
        "date": date
    }


def get_year(book):
    """book["data"] looks like 'November 2014' so we need to
    split on the space and then take the second place"""
    return int(book["date"].split()[1])


def main():
    base_url = "http://shop.oreilly.com/category/browse-subjects/" + \
               "data.do?sortby=publicationDate&page="

    books = []

    NUM_PAGES = 31

    for page_num in range(1, NUM_PAGES + 1):
        print("souping page {} , {} found so far".format(page_num, len(books)))
        url = base_url + str(page_num)
        soup = BeautifulSoup(requests.get(url).text, 'html5lib')

        for td in soup('td', 'thumbtext'):
            if not is_video(td):
                books.append(book_info(td))

        # respecting the robots.txt
        sleep(30)

    year_counts = Counter(get_year(book) for book in books
                          if get_year(book) <= 2014)

    years = sorted(year_counts)
    book_counts = [year_counts[year] for year in years]
    plt.plot(years, book_counts)
    plt.ylabel("# of data books")
    plt.title("# of data books")
    plt.show()


if __name__ == "__main__": main()
