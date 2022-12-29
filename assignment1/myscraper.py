import re
from urllib.request import urlopen, Request

from bs4 import BeautifulSoup as bS

# number of pages to scrap
DATA_LEN = 100
url = "https://maharashtratimes.com/latest-news/articlelist/75401897.cms"  
contents = []
counter = 1
outputFile = "111903117-Assignment-Dataset.txt"

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
        content = soup.find_all('span', {'class': 'text_ellipsis'})
        headline = soup.find_all('a',{'class': 'section_name'})
        for (h,c) in zip(headline,content):
            line = h.text
            con = c.text
            article = con+"\n"

            contents.append(article)
        counter += 1

    print(f"Total headlines collected :: {len(contents)}")
    with open(outputFile, "w") as file:
        for headline in contents:
            file.write(str(headline))
    print("Done......................")
