import requests
from bs4 import BeautifulSoup
# from PyDictionary import PyDictionary
from nltk.corpus import wordnet
import json

words = []
d = dict()
non_english = []

# dictionary = PyDictionary('hotel')
# print(dictionary.printMeanings())


def is_english_word(name):
    return bool(wordnet.synsets(name))

def take_two():
   y = requests.get('https://www.w3schools.com/python/').text
   soup = BeautifulSoup(y, 'html.parser')
   words = []
   for e_text in soup.find_all('p'):
        content1 = e_text.text
        p_words = content1.lower().split()
        words += p_words

   return set(words)

def take_one():
    x = requests.get('https://java2blog.com/python-list-to-set/').text
    soup = BeautifulSoup(x, 'html.parser')
    words = []
   
    for each_text in soup.find_all('p'):
        content = each_text.text
        sum = each_text.get_text()
        all_words = content.lower().split()
        words += all_words
        print(json.dumps(words))
        
        for index, wordsss in enumerate(all_words) :
            symbols = " !@#$%^&*()_-+={[}]|\;:\"<>?/., "
            for symbol in symbols:
                # print(symbol)
                if symbol in wordsss:
                    wordsss = wordsss.replace(symbol, '')
            all_words[index]= wordsss
            

        for word in all_words:
            if word in d:
                d[word] += 1
            else:
                d[word] = 1
        # for key in list(d.keys()):
        #     print(key, ":", d[key])

        for word in all_words: 
            if not is_english_word(word):
                all_words.remove(word)
                non_english.append(word)
            else:
                pass
    
    

# print(take_two())
take_one()

# print(all_words)
# print("non-english")
# print(non_english)
   

    

