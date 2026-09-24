#!/usr/bin/env python
# coding: utf-8

# In[21]:


from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import json


# In[22]:


def text_sum(text1):
    text = text1

    from nltk.corpus import stopwords
    from nltk.tokenize import word_tokenize, sent_tokenize

    # Tokenizing the text
    stopWords = set(stopwords.words("english"))
    words = word_tokenize(text)

    # Creating a frequency table to keep the
    # score of each word

    freqTable = dict()
    for word in words:
        word = word.lower()
        if word in stopWords:
            continue
        if word in freqTable:
            freqTable[word] += 1
        else:
            freqTable[word] = 1

    # Creating a dictionary to keep the score
    # of each sentence
    sentences = sent_tokenize(text)
    sentenceValue = dict()

    for sentence in sentences:
        for word, freq in freqTable.items():
            if word in sentence.lower():
                if sentence in sentenceValue:
                    sentenceValue[sentence] += freq
                else:
                    sentenceValue[sentence] = freq

    sumValues = 0
    for sentence in sentenceValue:
        sumValues += sentenceValue[sentence]

    # Average value of a sentence from the original text

    average = int(sumValues / len(sentenceValue))

    # Storing sentences into our summary.
    summary = ''
    for sentence in sentences:
        if (sentence in sentenceValue) and (sentenceValue[sentence] > (1.2 * average)):
            summary += " " + sentence
    return summary


# In[23]:


def to_json(data):
    """
    This function takes list of dictionary as Input and 
    then Creates a JSON file in which Input data is stored
    """
    with open("data_dict.json", "w") as outfile:
        json.dump(data, outfile,indent=4)
        outfile.close()


# In[24]:


data_list = []
url = "https://da.lacounty.gov/"
options = webdriver.ChromeOptions()
options.add_argument("--start-maximized") 
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument("--log-level=3")


# In[25]:


def get_data(slug_name):
    driver = webdriver.Chrome(options=options)
    driver.get(url)
    data_dict= {}
    fullName = driver.find_element(By.XPATH, f'//div/div[2]/div[1]/div/div/div[1]/div/p[2]/a/span').text.replace("\u00f3", "o")
    firstName = fullName.split(" ")[0]
    lastName = fullName.split(" ")[1]
    print(firstName)
    print(lastName)
    driver.find_element(By.XPATH, f'/html/body/div[2]/div[1]/div[2]/div/div[2]/div[1]/div/div/div[1]/div/p[2]/a').click()
    careerInfoDesignation = driver.find_element(By.XPATH, f'//div/div/div/div/div/div/p[3]').text.replace("\u00f3", "o")
    careerInfo = driver.find_element(By.XPATH, f'//div/div/div/div/div/div/p[4]').text
    careerInfo +=  driver.find_element(By.XPATH, f'//div/div/div/div/div/div/p[5]').text
    careerInfo = careerInfo.replace("\u00f3", "o")
    # print(careerInfo)
    achievements = driver.find_element(By.XPATH, f'//div[2]/div/div[3]/div/div/div/div/div/div/ul').text.replace("\n", "; ")
    # print(achievements)
    familyInfo = driver.find_element(By.XPATH, f'//div/div[3]/div/div/div/div/div/div/p[7]').text.replace("\u00f3", "o").replace("\u201c", "").replace("\u201d", "")
    educationInfo = driver.find_element(By.XPATH, f'//div/div[3]/div/div/div/div/div/div/p[8]').text.replace("\u00f3", "o")
    listOfCareerInfo = ""
    for i in range(9, 14):
        CareerInfo = driver.find_element(By.XPATH, f'//div/div[3]/div/div/div/div/div/div/p[{i}]').text.replace("\u00f3", "o")
        listOfCareerInfo = listOfCareerInfo + CareerInfo
        listOfCareerInfo = listOfCareerInfo.replace("\u2019", "'").replace("\u2013", ",")
    info = driver.find_element(By.XPATH, f'//div/div[3]/div/div/div/div/div/div/p[14]').text
    educationInfo = educationInfo + " " + info.split(".")[1].replace("\u00f3", "o")
    # print(educationInfo)
    familyInfo = familyInfo + " " + info.split(".")[0].replace("\u00f3", "o")
    # print(familyInfo)
    x = text_sum(str(listOfCareerInfo))
    summary = fullName + ", " + x
    if fullName:
        data_dict['fullName'] = fullName
    if firstName:
        data_dict['firstName'] = firstName
    if lastName:
        data_dict['lastName'] = lastName
    if careerInfoDesignation:
        data_dict['careerInfoDesignation'] = careerInfoDesignation
    if familyInfo:
        data_dict['familyInfo'] = familyInfo
    if educationInfo:
        data_dict['educationInfo'] = educationInfo
    if careerInfo:
        data_dict['careerInfo'] = careerInfo
    if listOfCareerInfo:
        data_dict['listOfCareerInfo'] = listOfCareerInfo
    if achievements:
        data_dict['achievements'] = achievements
    if summary:
        data_dict['summary'] = summary
    data_list.append(data_dict)
    return data_list


# In[26]:


if __name__ == '__main__':
    data_list = get_data("add_slug_name")
    to_json(data_list)


# In[ ]:




