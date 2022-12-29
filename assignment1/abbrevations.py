import re
import  pandas as pd
from urllib.request import urlopen, Request

from bs4 import BeautifulSoup as bS

url  ="https://blog.ongig.com/job-titles/job-title-abbreviations-acronyms/"

def scrape(url):
    counter = 0
    DATA_LEN = 10
    contents = []
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
            #content = soup.find_all('section',{'class': 'post_content clearfix'}).find_all('ul')
            content = soup.find_all('ul')
            for c in content:
                for li in c.find_all('li'):
                    con = li.text
                    con += "\n"
                contents.append(con)
            counter += 1
        with open("abbreviations.txt", "w") as file:
            for c in contents:
                file.write(str(c))
        print("Done......................")

def get_df(inputfile):
    abbr = []
    expanded = []
    with open(inputfile, "r") as f:
        text = f.read()
    sentences = text.split("\n")
    for sentence in sentences:
        print(sentence)
        try:
            abbr.append(sentence.split("—")[0])
        except:
            abbr.append("None")
        try:
            expanded.append(sentence.split("—")[1])
        except:
            expanded.append("None")
    gazatter = ["designation"]* len(abbr)
    data = {'abbr': abbr, 'expanded': expanded, 'gazzatters': gazatter}
    df = pd.DataFrame(data)
    return df


def get_df_institutes(inputfile):
    abbr = []
    expanded = []
    with open(inputfile, "r") as f:
        text = f.read()
    sentences = text.split("\n")
    for sentence in sentences:
        try:
            abbr.append(sentence.split("-")[0])
        except:
            abbr.append("None")
        try:
            expanded.append(sentence.split("-")[1])
        except:
            expanded.append("None")
    gazatter = ["institutes"]* len(abbr)
    data = {'abbr': abbr, 'expanded': expanded, 'gazzatters': gazatter}
    df = pd.DataFrame(data)
    return df

def scrape_institutes(url):
    counter = 0
    DATA_LEN = 10
    contents = []
    #con = ""
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
            #content = soup.find_all('section',{'class': 'post_content clearfix'}).find_all('ul')
            content = soup.find_all('table')
            for c in content:
                for tbody in c.find_all('tbody'):
                    for  tr in tbody.find_all('tr'):
                        for td in tr.find_all('td'):
                            for b in td.find_all('b'):
                                con = b.text
                            # for c in td.find_all('a'):
                            #     con += c.text
                            con += "\n"
                            print(con)
                            contents.append(con)
            counter += 1
        with open("abbreviationsInstitutes.txt", "w") as file:
            for c in contents:
                file.write(str(c))
        print("Done......................")

def main():
    input_file = "assignment1/abbreviations.txt"
    df_desg = get_df(input_file)
    #scrape_institutes("https://grants.nih.gov/grants/acronym_list.htm")
    df_insti = get_df_institutes("abbreviationsInstitutes.txt")
    df = [df_desg,df_insti]
    result = pd.concat(df)
    result.to_csv("abbr.csv")
    

main()