mport pandas as pd
import numpy as np
import re
import nltk
import nltk
import string
from nltk.corpus import stopwords
from collections import Counter

def preprocess(text):
  text = text.lower()
  y = []
  for i in text:
    if i not in stopwords.words("english") and i not in string.punctuation:
        y.append(i)
  text = "".join(y)

def get_data(filename):
  words = []
  with open(filename,"r") as f:
    text  = f.read()
    text = text.lower()
  return text

def minDistance(word1, word2):
  W1_LEN = len(word1)
  W2_LEN = len(word2)
  dp = [[0] * (W1_LEN + 1) for _ in range(W2_LEN + 1)]
  for i in range(W1_LEN):
      dp[W2_LEN][i] = W1_LEN - i
  for i in range(W2_LEN):
      dp[i][W1_LEN] = W2_LEN - i
  for i in range(W2_LEN - 1, -1, -1):
      for j in range(W1_LEN - 1, -1, -1):
          if word2[i] == word1[j]:
              dp[i][j] = dp[i + 1][j + 1]
          else:
              dp[i][j] = min(dp[i + 1][j], dp[i + 1][j + 1], dp[i][j + 1]) + 1
  #     print(np.array(dp))
  return dp[0][0]

def my_autocorrect(V,word,k):
  result = []
  ans = []
  word = word.lower()
  if word in V:
    return ["Already exists"]
  for i in V:
    diff = minDistance(word,i)
    result.append((diff,i))
  result.sort()
  return result[:k]


def main(word,k):
    text = get_data("book.txt")
    nltk_tokens = nltk.word_tokenize(text)
    V = set(nltk_tokens)
    print(my_autocorrect(V,word,k))

main("movy",5)
