from nltk.corpus import wordnet
import os
import sys
import re
import string

def clitics_handler( token ):
    token = token.replace("\'d", "%would")
    token = token.replace("\'ll", "%will")
    token = token.replace("\'ve", "%have")
    token = token.replace("\'re", "%are")
    token = token.replace("\'m", "%am")

    token = token.replace("can\'t", "can not")
    token = token.replace("shan\'t", "shall not")
    token = token.replace("won\'t", "will not")
    token = token.replace("ain\'t", "is not")
    token = token.replace("n\'t", "%not")

    token = token.replace("it\'s", "it is")
    token = token.replace("It\'s", "It is")

    token = token.replace("that\'s", "that is")
    token = token.replace("That\'s", "That is")

    token = token.replace("there\'s", "there is")
    token = token.replace("There\'s", "There is")

    token = token.replace("where\'s", "where is")
    token = token.replace("Where\'s", "Where is")

    token = token.replace("let\'s", "let us")
    token = token.replace("Let\'s", "Let us")

    return token

def emoji_handler( token ):
    token = token.replace(":)", " happy ")
    token = token.replace(":(", " sad ")
    return token


def punctuation_handler( token ):
    token = re.sub(r"""[!"()$^&*+,/?[\]=]""", r" \g<0> ", token)
    return token
def combine_word_handler( token ):
    words = token.split(' ')
    new_token = ""

    combine1 = ""
    combine2 = ""
    # combine word with single character
    for word in words:
        if( len(word) == 1 ):
            combine1 += word
            if( combine2 ):
                new_token += combine2 + ' '
                combine2 = ""

        elif( len(word) == 2 and word[1] == '.' ):
            combine2 += word
            if( combine1 ):
                new_token += combine1 + ' '
                combine1 = ""

        else:
            if( combine1 ):
                new_token += combine1 + ' '
                combine1 = ""

            if( combine2 ):
                new_token += combine2 + ' '
                combine2 = ""

            new_token += word + ' '

    if( combine1 ):
        new_token += combine1 + ' '

    if( combine2 ):
        new_token += combine2 + ' '
    
    return new_token[:-1]


url = re.compile(u'(?:(?:https?|ftp)\:\/\/)?(?:[a-z0-9]{1})(?:(?:\.[a-z0-9-])|(?:[a-z0-9-]))*\.(?:[a-z]{2,6})(?:\/?)') 
def url_handler( token, urls_found ):
    urls = url.findall(token)
    # Replacing url so it won't change
    for u in urls:
        urls_found.append(u)
        token = re.sub( u, "%%%URL%%%", token)
    return token

def date_handler( token, dates_found ):
    res1 = re.findall(r'\d{1,4}[/-]\d{1,2}[/-]\d{2,4}', token)
    for r in res1:
        if( '-' in r):
            date = r.split('-')
        else:
            date = r.split('/')

        if( len(date) == 2 ):
            token = re.sub( r, "%%%DATE%%%", token)
            if( len(date[0]) == 4 ):
                d = "CF:D:" + str(date[0]) + '-' + str(date[1])
                dates_found.append(d)
            else:
                d = "CF:D:" + str(date[1]) + '-' + str(date[0])
                dates_found.append(d)

        elif( len(date) == 3 ):
            token = re.sub( r, "%%%DATE%%%", token)
            if( len(date[0]) == 4 ):
                d = "CF:D:" + str(date[0]) + '-' + str(date[1]) + '-' + str(date[2])
                dates_found.append(d)
            else:
                d = "CF:D:" + str(date[2]) + '-' + str(date[2]) + '-' + str(date[0])
                dates_found.append(d)

    res2 = re.findall(r'(?:\d{1,2}t?h? )?(?:Jan|Feb|Mar|Apr|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]* (?:\d{1,2}, )?\d{2,4}', token)
    for r in res2:
        dates_found.append(r)
        token = re.sub( r, "%%%DATE%%%", token)

    return token

def time_handler( token, time_found ):
    res1 = re.findall(r'\d{1,2} [AP]M', token)

    for r in res1:
        token = re.sub( r, "%%%TIME1%%%", token)
        time = r.split(' ')
        t = 'CF:T:'
        hr = int(time[0])
        if( r[-2] == 'P' ):
            hr += 12
        if( hr < 10 ):
            t += '0' + str(hr) + '00'
        else:
            t += str(hr) + '00'
        time_found.append(t)

    res2 = re.findall(r'\d{1,2} o\'clock', token)
    for r in res2:
        token = re.sub( r, "%%%TIME2%%%", token)
        time = r.split(' ')
        t = 'CF:T:'
        hr1 = int(time[0])
        hr2 = hr1 + 12

        if( hr1 < 10 ):
            t += '0' + str(hr1)
        else:
            t += str(hr1)
        
        t += '|' + str(hr2)
        time_found.append(t)

    return token


with open("data.txt", "r") as file:
    tweets = file.readlines()

for tweet in tweets:
    original = tweet

    urls_found = []
    dates_found = []
    time_found = []

    u = 0
    d = 0
    t = 0

    tweet = url_handler( tweet, urls_found )
    tweet = date_handler( tweet, dates_found )
    tweet = time_handler( tweet, time_found )
    tweet = emoji_handler( tweet )
    tweet = clitics_handler( tweet )
    tweet = combine_word_handler( tweet )
    tweet = punctuation_handler( tweet )
    tweet = punctuation_handler_for_single_quote( tweet )
    tweet = punctuation_handler_for_dot( tweet )

    tweet = re.sub('\s{1,}', ' ', tweet)    # removes multiple whitespaces

    tokens = tweet.split(' ')
    print(original)
    print(len(tokens))

    for token in tokens:
        if "%%%URL%%%" in token:
            print(urls_found[u])
            u += 1
        elif "%%%DATE%%%" in token:
            print( dates_found[d] )
            d += 1
        elif "%%%TIME%%%" in token:
            print( time_found[t] )
            t += 1
        else:
            token = token.replace("%", ".")
            n = len(token)
            if( n == 2 ):
                print(token[0])
                if( token[1][0] == '-' ):
                    print(token[1])
                else:
                    print('-')
                    print(token[1])

            elif( n > 0 ):
                print(token[0])
                for i in range(1, n):
                    print('-')
                    print(token[i])
            else:
                print('-')
    print()