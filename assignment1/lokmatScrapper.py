import re
from urllib.request import urlopen, Request

from bs4 import BeautifulSoup as bS

# number of pages to scrap
DATA_LEN = 250
url = "https://jantaserishta.com/science"
contents = []
counter = 1
outputFile = "news.txt"

while url:
    if counter > DATA_LEN:
        break
    htmlDoc = ''
    print(f"Getting............ {url}")
    req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    with urlopen(req) as response:
        for line in response:
            line = line.decode('utf-8')
            htmlDoc = htmlDoc + line.replace('\n', '')
        soup = bS(htmlDoc, 'html.parser')
        content = soup.find_all('p', {'class': 'jsx-542047719'})
        for c in content:
            con = c.text
            article = con+"\n"

            contents.append(article)
        counter += 1

    print(f"Total headlines collected :: {len(contents)}")
    with open(outputFile, "w") as file:
        for headline in contents:
            file.write(str(headline))
    print("Done......................")
