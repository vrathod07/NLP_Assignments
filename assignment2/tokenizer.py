import re
import  os
import datetime

def handle_date(sentence):
    try:
        match = re.search(r'\d{4}-\d{2}-\d{2}', sentence)
        date = datetime.datetime.strptime(match.group(), '%Y-%m-%d').date()
        sentence = re.sub(r'\d{4}-\d{2}-\d{2}',date,sentence)
    except:
        pass
    return sentence

def handle_smile(sentence):
    sentence = sentence.replace(":)",":) ")
    return sentence

def handle_hash(sentence):
    sentence = re.sub(r"#","# ",sentence)
    return sentence

def handle_clitics(sentence):
    # specific
    sentence = re.sub(r"won\'t", "will not", sentence)
    sentence = re.sub(r"can\'t", "can not", sentence)
    # general
    sentence = re.sub(r"n\'t", " not", sentence)
    sentence = re.sub(r"\'re", " are", sentence)
    sentence = re.sub(r"\'s", " is", sentence)
    sentence = re.sub(r"\'d", " would", sentence)
    sentence = re.sub(r"\'ll", " will", sentence)
    sentence = re.sub(r"\'t", " not", sentence)
    sentence = re.sub(r"\'ve", " have", sentence)
    sentence = re.sub(r"\'m", " am", sentence)
    return sentence

def emoji_handler(sentence):
    sentence = sentence.replace(":)", " happy ")
    sentence = sentence.replace(":(", " sad ")
    return sentence

def handle_punctuation(sentence):
    sentence = re.sub(r"""[!"()$^&*+,/?[\]=]""", r" \g<0> ", sentence)
    return sentence

def handle_apostrophe(sentence):
    sentence = re.sub(r"s\'", "s \'s", sentence)
    sentence = re.sub(r"\'s", " \'s", sentence)
    return sentence

def get_text(filepath):
    with open(filepath, 'r') as f:
        text = f.readlines()
    return text

url = re.compile(u'(?:(?:https?|ftp)\:\/\/)?(?:[a-z0-9]{1})(?:(?:\.[a-z0-9-])|(?:[a-z0-9-]))*\.(?:[a-z]{2,6})(?:\/?)') 
def url_handler( token, urls_found ):
    urls = url.findall(token)
    # Replacing url so it won't change
    for u in urls:
        urls_found.append(u)
        token = re.sub(u, "%%%URL%%%", token)
    return token

def tokenize(sentences,output_path):
    result = []
    urls= []
    u = 0
    for sentence in sentences:
       print(sentence)
       sentence = handle_date(sentence)
       sentence = handle_apostrophe(sentence)
       sentence = url_handler(sentence, urls)
       sentence = handle_smile(sentence)
       sentence = handle_hash(sentence)
       sentence = emoji_handler(sentence)
       sentence = handle_punctuation(sentence)
       sentence = handle_clitics(sentence)

       sentence = re.sub('\s{1,}', ' ',sentence)
       s_l = sentence.split(" ")
       print(len(s_l))
       for  i in s_l:   
            if "%%%URL%%%" in i:
                print(urls[u],end="\n")
                result.append(urls[u])
                u += 1
            else:
                print(i,end="\n")
                result.append(i)
       results = "".join(result)
       with open(output_path,"a+") as f:
            f.write(results)

        
             
def main():
    filepath = "data.txt"
    outputPath = os.path.join(filepath.split(".")[0]+"_tokenized.txt")
    text = get_text(filepath)
    tokenize(text,outputPath)

main()
    
