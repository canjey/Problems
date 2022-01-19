from ast import Pass
import json

import requests
from bs4 import BeautifulSoup
from nltk.corpus import wordnet


def get_second_page(url):
    page = requests.get(url).text
    soup = BeautifulSoup(page, 'html.parser')
    all_words = []

    for all_text in soup.find_all('p'):
        content = all_text.text
        p_words = content.lower().split()
        all_words += p_words
        global set_words
        set_words = set(all_words)
    return all_words
   


def get_page_words(page_url):
    page = requests.get(page_url).text
    soup = BeautifulSoup(page, 'html.parser')
    all_words = []
    non_english = []
    word_count = dict()

    for each_text in soup.find_all('p'):
        content = each_text.text
        p_words = content.lower().split()
        p_non_english_words = []
        for index, word in enumerate(p_words):
            symbols = " !@#$%^&*()_-+={[}]|\\;:\"<>?/.,"
            for symbol in symbols:
                if symbol in word:
                    word = word.replace(symbol, '')
            p_words[index] = word

            # update word count
            if word in word_count:
                word_count[word] += 1
            else:
                word_count[word] = 1
            # check if word is an english word
            if not is_english_word(word):
                p_words.remove(word)
                p_non_english_words.append(word)
        all_words += p_words
        non_english += p_non_english_words
        global set_words1
        set_words1 = set(all_words)
    #print(set_words1)
    return {
        'all_words': list(set(all_words)),
        'non_english': list(set(non_english)),
        'word_count': word_count,
        
    }


def is_english_word(name):
    return bool(wordnet.synsets(name))

def compare_the_two():
    #keep only duplicate
    set_words.intersection(set_words1)

    #unique words in page one
    unique_words_in_page_one = set_words1.difference(set_words)
    
    #unique words in page two
    unique_words_in_second_page = set_words.difference(set_words1)
    
    return{
        'duplicate words in both pages':list(set_words),
        'unique words in page one':list(unique_words_in_page_one),
        'unique words in page two' : list(unique_words_in_second_page)
    }



y = input("Enter the URL of the first page")
all_words_ = get_page_words(y)
compare = input('Do you want to compare with another page?')
if compare == 'Yes':
    x = input("Enter the URL of the second page")
    second_page = get_second_page(x)
else:
    Pass

print('all words in first page')
print(json.dumps(all_words_, indent=3))

print('two')
print(json.dumps(second_page, indent=3))

print("compare the two pages")
print(json.dumps(compare_the_two(), indent=3))

print(type(set_words))