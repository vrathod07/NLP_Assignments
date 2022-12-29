import re
from urllib.request import urlopen, Request

from bs4 import BeautifulSoup as bS

# number of pages to scrap
DATA_LEN = 10


def getAllHeadlines(category, outputFile):
    """
    will read all the headlines and save in the
    filename specified
    :return: none
    """
    url = ["https://marathi.abplive.com/news/"]  # using this website to scrap
    url[0] += category
    allHeadlines = []
    counter = 2  # this website track pages after 2

    for link in url:
        while link:
            if counter > DATA_LEN:
                break
            htmlDoc = ''
            print(f"Getting............ {link}")
            req = Request(link, headers={'User-Agent': 'Mozilla/5.0'})
            with urlopen(req) as response:
                for line in response:
                    line = line.decode('utf-8')
                    htmlDoc = htmlDoc + line.replace('\n', '')
                soup = bS(htmlDoc, 'html.parser')
                headlineDiv = soup.find_all('div', {'class': 'uk-width-3-5 fz20 p-10 newsList_ht'})
                for headLine in headlineDiv:
                    article = headLine.text

                    article = re.sub(r"\([^)]*\)", r'', article)
                    article = re.sub(r"\[[^\]]*\]", r'', article)
                    article = re.sub(r"<[^>]*>", r'', article)
                    article = re.sub(r"^https?://.*[\r\n]*", r'', article)
                    article = re.sub(r'^http?://.*[\r\n]*', r'', article)
                    article = article.replace(u'\ufeff', '')
                    article = article.replace(u'\xa0', u'')
                    article = article.replace('  ', ' ')
                    article = article.replace(' , ', ', ')
                    article = article.replace('-', '')
                    article += "\n"

                    allHeadlines.append(article)
            link = url[0] + "/page-" + str(counter)
            counter += 1

    print(f"Total headlines collected :: {len(allHeadlines)}")
    with open(outputFile, "w") as file:
        for headline in allHeadlines:
            file.write(str(headline))
    print("Done......................")


# make sure the category name exists
getAllHeadlines("sports", "sports.txt")