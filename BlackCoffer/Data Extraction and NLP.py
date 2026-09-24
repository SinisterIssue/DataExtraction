
import numpy as np
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import json
import re
from deep_translator import GoogleTranslator
from collections import Counter
import nltk
from nltk.corpus import stopwords


nltk.download('stopwords')


excel_data = pd.read_excel('Input.xlsx')


excel_data.head()



len(excel_data['URL_ID'])


# ## Extraction


excel_data['content'] = ""
for i in range(0, len(excel_data['URL_ID'])):
    urlID = excel_data["URL_ID"][i]
    print(urlID)
    url = excel_data["URL"][i]
    print(url)
    
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized") 
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--log-level=3")
    translator = GoogleTranslator(target='english')
    driver = webdriver.Chrome(options=options)
    driver.get(url)
    try:
        text = driver.find_element(By.XPATH, f'/html/body/div[6]/div[2]/article/div[2]').text
    except:
        try:
            text = driver.find_element(By.XPATH, f'/html/body/div[6]/article/div[2]/div/div[1]/div/div[1]').text
        except:
            print("no text")
            text = ""
            pass
    excel_data["content"][i] = text 
    print(text)
    file1 = open(f"{urlID}.txt","w", encoding="utf-8")
    file1.write(text)
    file1.close()
    print("*"*50)
    
    driver.close()


excel_data.head()


# ## AVERAGE SENTENCE LENGTH


def avg_sentence_length(text):
    sents = text.split('.')
    avg_sen_len = sum(len(x.split()) for x in sents) / len(sents)
    return avg_sen_len


excel_data["AVG SENTENCE LENGTH"] = excel_data["content"].apply(avg_sentence_length)


excel_data.head()


# ## AVERAGE WORD LENGTH


def avg_word_length(text):
    words = text.split()
    if len(words)==0:
        return 0
    average = sum(len(word) for word in words) / len(words)
    return average


excel_data["AVG WORD LENGTH"] = excel_data["content"].apply(avg_word_length)


excel_data.head()


# ## WORD COUNT


def word_count(text):
    s = text.split()
    words = [word for word in s if not word in stopwords.words("english")]
    return len(words)



excel_data["WORD COUNT"] = excel_data["content"].apply(word_count)


excel_data.head()


# ## PERSONAL PRONOUNS

def personal_pronouns(text):
    pronounRegex = re.compile(r'\b(I|we|my|ours|(?-i:us))\b',re.I)
    pronouns = pronounRegex.findall(text)
    return len(pronouns)



excel_data["PERSONAL PRONOUN"] = excel_data["content"].apply(personal_pronouns)


excel_data.head()


# ## AVERAGE WORDS PER SENTENCE


def average_words_per_sentence(text):
    parts = [len(l.split()) for l in re.split(r'[.]', text) if l.strip()]
    if len(parts)==0:
        return 0
    return (sum(parts)/len(parts))



excel_data["AVG NUMBER OF WORDS PER SENTENCE"] = excel_data["content"].apply(average_words_per_sentence)


excel_data.head()


# ## COMPLEX WORD


def word_syllable_count(word):
    return sum(list(map(lambda x: 1 if x in ["a","i","e","o","u","y","A","E","I","O","U","y"] else 0,word)))


def complex_word(text):
    s = text.split()
    count=0
    for word in s:
        if word_syllable_count(word)>=2:
            count+=1
    return count



excel_data["COMPLEX WORD COUNT"] = excel_data["content"].apply(complex_word)



excel_data.head()


# ## PERCENTAGE OF COMPLEX WORD

def percentage_of_complex_words(text):
    s = text.split()
    count=0
    if len(s) == 0:
        return 0
    for word in s:
        if word_syllable_count(word)>=2:
            count+=1
    return (count/len(s))*100


excel_data["PERCENTAGE OF COMPLEX WORDS"] = excel_data["content"].apply(percentage_of_complex_words)


excel_data.head()


# ## FOG INDEX


def fog_index(text):
    sents = text.split('.')
    avg_sen_len = sum(len(x.split()) for x in sents) / len(sents)
    s = text.split()
    count=0
    if len(s) == 0:
        return 0
    for word in s:
        if word_syllable_count(word)>=2:
            count+=1
    percentage = (count/len(s))*100
    return 0.4*(avg_sen_len+percentage)


excel_data["FOG INDEX"] = excel_data["content"].apply(fog_index)


excel_data.head()


# ## POSITIVE WORDS

def readwords(filename):
    f = open(filename)
    words = [line.rstrip() for line in f.readlines()]
    return words



def positive_words(text):
    positive = readwords('positive-words.txt')
    count = Counter(text.split())
    pos = 0
    for key, val in count.items():
        key = key.rstrip('.,?!\n') # removing possible punctuation signs
        if key in positive:
            pos += val
    return pos
    


excel_data["POSITIVE SCORE"] = excel_data["content"].apply(positive_words)



excel_data.head()


# ## NEGATIVE WORDS


def negative_words(text):
    negative = readwords('negative-words.txt')
    count = Counter(text.split())
    neg = 0
    for key, val in count.items():
        key = key.rstrip('.,?!\n') # removing possible punctuation signs
        if key in negative:
            neg += val
    return neg


excel_data["NEGATIVE SCORE"] = excel_data["content"].apply(negative_words)



excel_data.head()


# ## POLARITY SCORE


def polarity_score(text):
    positive_score = positive_words(text)
    negative_score = negative_words(text)
    pol_score = (positive_score - negative_score)/(positive_score+negative_score+0.000001)
    return pol_score 


excel_data["POLARITY SCORE"] = excel_data["content"].apply(polarity_score)


excel_data.head()


# ## SYLLABLE COUNT PER WORD


def syllable_count(text):
    word = text.lower()
    word = text.split()
    count = 0
    vowels = "aeiou"
    if word[0] in vowels:
        count += 1
    for index in range(1, len(word)):
        if word[index] in vowels and word[index - 1] not in vowels:
            count += 1
    if word.endswith("es"):
        count -= 1
    if word.endswith("ed"):
        count -= 1
    if count == 0:
        count += 1
    return count 


# ## SUBJECTIVE SCORE


def stopwords_removal(text):
    stopword = readwords('StopWords_Auditor.txt')
    stopword.extend(readwords("StopWords_Currencies.txt"))
    stopword.extend(readwords("StopWords_DatesandNumbers.txt"))
    stopword.extend(readwords("StopWords_Generic.txt"))
    stopword.extend(readwords("StopWords_GenericLong.txt"))
    stopword.extend(readwords("StopWords_Geographic.txt"))
    stopword.extend(readwords("StopWords_Names.txt"))
    filtered = []
    s = text.split()
    words = [word for word in s if not word in stopword]
    return words



def subjective_score(text):
    positive_score = positive_words(text)
    negative_score = negative_words(text)
    clean = stopwords_removal(text)
    sub_score = (positive_score + negative_score)/(len(clean) + 0.000001)
    return sub_score



excel_data["SUBJECTIVE SCORE"] = excel_data["content"].apply(subjective_score)


excel_data.head()


# ## Saving final CSV


excel_data.drop("content", axis=1, inplace=True)


excel_data.head()


excel_data.to_csv("Output Data Structure.csv")





