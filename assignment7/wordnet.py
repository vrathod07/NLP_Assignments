from nltk.corpus import wordnet as wn
import nltk
from nltk.corpus import wordnet_ic
from nltk.wsd import lesk
from nltk.tokenize import word_tokenize

nltk.download('wordnet')
nltk.download('omw-1.4')
nltk.download('wordnet_ic')
nltk.download('punkt')

def get_common_hypernym(word1,word2):
  syn_1 = wn.synset(word1+".n.01")
  syn_2 = wn.synset(word2+".n.01")
  lch = wn.synset(word1+".n.01").lowest_common_hypernyms(wn.synset(word2+".n.01"))
  return lch

def get_lin_similarity(word1,word2):
  syn_1 = wn.synset(word1+".n.01")
  syn_2 = wn.synset(word2+".n.01")
  brown_ic = wordnet_ic.ic('ic-brown.dat')
  return syn_1.lin_similarity(syn_2, brown_ic)

def get_res_similarity(word1,word2):
  syn_1 = wn.synset(word1+".n.01")
  syn_2 = wn.synset(word2+".n.01")
  brown_ic = wordnet_ic.ic('ic-brown.dat')
  return syn_1.res_similarity(syn_2, brown_ic)

def get_jcn_similarity(word1,word2):
  syn_1 = wn.synset(word1+".n.01")
  syn_2 = wn.synset(word2+".n.01")
  brown_ic = wordnet_ic.ic('ic-brown.dat')
  return syn_1.jcn_similarity(syn_2, brown_ic)

def get_lch_similarity(word1,word2):
  syn_1 = wn.synset(word1+".n.01")
  syn_2 = wn.synset(word2+".n.01")
  brown_ic = wordnet_ic.ic('ic-brown.dat')
  return syn_1.lch_similarity(syn_2, brown_ic)

def get_lesk_wsd(sentence,word):
    a1= lesk(word_tokenize(sentence),word)
    return (a1,a1.definition())

def print_menu():
    print("-----------------------------------")
    print("1. Get common hypernyms of two words")
    print("2. Find Lin similarity between any two words as per WordNet. Use Brown information content.")
    print("3. Find Resnik similarity between any two words as per WorNet. Use Brown information content.")
    print("4. Find Jiang-Conrath distance between any two concepts as per WordNet.")
    print("5. Find Leacock-Chodorow similarity between any two concepts as per WordNet.")
    print("6. Using senses from WordNet, find the appropriate sense for an ambigous word in the sentence as per lesk algorithm.")
    print("-----------------------------------")
def main():
    while(1):
        print_menu()
        print("\n Enter the choice")
        n = int(input())
        if(n == 1):
            print("Enter any two words")
            w1 = input()
            w2 = input()
            print(get_common_hypernym(w1,w2))
            break
        if(n == 2):
            print("Enter any two words")
            w1 = input()
            w2 = input()
            print(get_lin_similarity(w1,w2))
            break
        if(n == 3):
            print("Enter any two words")
            w1 = input()
            w2 = input()
            print(get_res_similarity(w1,w2))
            break
        if(n == 4):
            print("Enter any two words")
            w1 = input()
            w2 = input()
            print(get_jcn_similarity(w1,w2))
            break
        if(n == 5):
            print("Enter any two words")
            w1 = input()
            w2 = input()
            print(get_lch_similarity(w1,w2))
            break
        if(n == 6):
            print("Enter a sentence")
            sentence = input()
            print("\nEnter the word that to disambiguate")
            word = input()
            print(get_lesk_wsd(sentence,word))
            break

main()