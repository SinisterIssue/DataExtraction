#!/usr/bin/env python
# coding: utf-8

# In[102]:


from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import json
import re


# In[103]:


def to_json(data):
    """
    This function takes list of dictionary as Input and 
    then Creates a JSON file in which Input data is stored
    """
    with open("data_dict.json", "w") as outfile:
        json.dump(data, outfile,indent=4)
        outfile.close()


# In[104]:


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


# In[105]:


data_list = []
url = "https://en.wikipedia.org/wiki/Category:South_Korean_women_in_politics"
options = webdriver.ChromeOptions()
options.add_argument("--start-maximized") 
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument("--log-level=3")


# In[106]:


def get_data(slug_name):
    driver = webdriver.Chrome(options=options)
    driver.get(url)
    list1 = driver.find_elements(By.XPATH, f'//div[1]/div/div/div[1]/ul/li/div/div[1]/a')
    for i in range(1, len(list1)+1):
        driver.find_element(By.XPATH, f'//div[1]/div/div/div[1]/ul/li[{i}]/div/div[1]/a').click()
        time.sleep(2)
        list2 = driver.find_elements(By.XPATH, f'/html/body/div[3]/div[3]/div[5]/div[2]/div[2]/div/div/div/h3')
        for j in range(1, len(list2)+1):
            list3 = driver.find_elements(By.XPATH, f'/html/body/div[3]/div[3]/div[5]/div[2]/div[2]/div/div/div[{j}]/ul/li/a')
            for k in range(1, len(list3)+1):
                data_dict={}
                fullName = driver.find_element(By.XPATH, f'/html/body/div[3]/div[3]/div[5]/div[2]/div[2]/div/div/div[{j}]/ul/li[{k}]/a').text
                fullName = fullName.replace("(politician)", "").replace("(lawyer)", "")
                print(fullName)
                driver.find_element(By.XPATH, f'/html/body/div[3]/div[3]/div[5]/div[2]/div[2]/div/div/div[{j}]/ul/li[{k}]/a').click()
                time.sleep(2)
                try:
                    list4 = driver.find_elements(By.XPATH, f'/html/body/div[3]/div[3]/div[5]/div[1]/table[1]/tbody/tr')
                    familyInfo = ""
                    educationInfo = ""
                    importantDates = ""
                    religion = ""
                    age = ""
                    dob =""
                    placeOfBirthCity = ""
                    constituency = ""
                    politicalCareerInfo = ""
                    politicalParty = ""
                    rawName = ""
                    for l in range(1, len(list4)+1):
                        headings = driver.find_element(By.XPATH, f'/html/body/div[3]/div[3]/div[5]/div[1]/table[1]/tbody/tr[{l}]').text
                        if "Born" in headings:
                            dob = driver.find_element(By.XPATH, f'/html/body/div[3]/div[3]/div[5]/div[1]/table[1]/tbody/tr[{l}]/td').text.replace("[1]", "")
                            try:
                                age = dob.split("(")[1]
                                age = age.split(")")[0].replace("age", "").strip()
                                placeOfBirthCity = dob.split(")")[1].replace("\n", "").strip()
                                dob = dob.split("(")[0]
    #                             print(placeOfBirthCity)
    #                             print(age)
                            except:
                                try:
                                    placeOfBirthCity = dob.split("\n")[1]
                                    dob = dob.split("\n")[0]
                                except:
                                    pass
                            print(dob)
                        if "Constituency"in headings:
                            constituency = driver.find_element(By.XPATH, f'/html/body/div[3]/div[3]/div[5]/div[1]/table[1]/tbody/tr[{l}]/td').text
    #                         print(constituency)
                        if "Political party" in headings:
                            politicalParty = driver.find_element(By.XPATH, f'/html/body/div[3]/div[3]/div[5]/div[1]/table[1]/tbody/tr[{l}]/td').text
                            politicalParty = politicalParty.replace("[1]", "")
    #                         print(politicalParty)
                        if "Alma mater" in headings:
                            educationInfo = driver.find_element(By.XPATH, f'/html/body/div[3]/div[3]/div[5]/div[1]/table[1]/tbody/tr[{l}]/td').text
                            educationInfo = educationInfo.replace("\n", "; ")
    #                         print(educationInfo)
                        if "Died" in headings:
                            died = driver.find_element(By.XPATH, f'/html/body/div[3]/div[3]/div[5]/div[1]/table[1]/tbody/tr[{l}]/td').text.replace("[1]", "")
                            importantDates = "Died: " + died
                            if "aged" in died:
                                age = died.split("aged")[1].replace(")","")
                                age = age.split("\n")[0]
                        if "Spouse(s)" in headings:
                            spouse = driver.find_element(By.XPATH, f'/html/body/div[3]/div[3]/div[5]/div[1]/table[1]/tbody/tr[{l}]/td').text
                            familyInfo = familyInfo + " Spouse: " + spouse
                        if "Children" in headings:
                            children = driver.find_element(By.XPATH, f'/html/body/div[3]/div[3]/div[5]/div[1]/table[1]/tbody/tr[{l}]/td').text
                            familyInfo = familyInfo + " Children: " + children
                        if "Education" in headings:
                            try:
                                education = driver.find_element(By.XPATH, f'/html/body/div[3]/div[3]/div[5]/div[1]/table[1]/tbody/tr[{l}]/td').text
                                educationInfo = educationInfo + " Education: " + education
                                educationInfo = educationInfo.replace("\n", ";").replace("[1]", "")
                            except:
                                pass
                        if "Religion" in headings:
                            religion = driver.find_element(By.XPATH, f'/html/body/div[3]/div[3]/div[5]/div[1]/table[1]/tbody/tr[{l}]/td').text
                            religion = religion.replace("\n", " ")
                except:
                    pass
                image=""
                try:
                    image = driver.find_element(By.XPATH, f'/html/body/div[3]/div[3]/div[5]/div[1]/table/tbody/tr[3]/td/a/img').get_attribute("src")
                    print(image)
                except:
                    try:
                        image = driver.find_element(By.XPATH, f'/html/body/div[3]/div[3]/div[5]/div[1]/table/tbody/tr[2]/td/a/img').get_attribute("src")
                        print(image)
                    except:
                        pass
                try:
                    
                    list5 = driver.find_elements(By.XPATH, f'/html/body/div[3]/div[3]/div[5]/div[1]/table[2]/tbody/tr')
                    head = driver.find_element(By.XPATH, f'/html/body/div[3]/div[3]/div[5]/div[1]/table[2]/tbody/tr[1]').text
#                     print(head)
                    if "Election" in head:
                        for m in range(2, len(list5)+1):
#                             print("here")
                            list6 = driver.find_elements(By.XPATH, f'/html/body/div[3]/div[3]/div[5]/div[1]/table[2]/tbody/tr[{m}]/td')
                            for n in range(1, len(list6)+1):
                                if n==1:
                                    election = driver.find_element(By.XPATH, f'/html/body/div[3]/div[3]/div[5]/div[1]/table[2]/tbody/tr[{m}]/td[{n}]').text
                                elif n==2:
                                    year = driver.find_element(By.XPATH, f'/html/body/div[3]/div[3]/div[5]/div[1]/table[2]/tbody/tr[{m}]/td[{n}]').text
                                elif n==3:
                                    district = driver.find_element(By.XPATH, f'/html/body/div[3]/div[3]/div[5]/div[1]/table[2]/tbody/tr[{m}]/td[{n}]').text
                                elif n==4:
                                    PartyAffliation = driver.find_element(By.XPATH, f'/html/body/div[3]/div[3]/div[5]/div[1]/table[2]/tbody/tr[{m}]/td[{n}]').text
                                elif n==5:
                                    votes = driver.find_element(By.XPATH, f'/html/body/div[3]/div[3]/div[5]/div[1]/table[2]/tbody/tr[{m}]/td[{n}]').text
                                elif n==6:
                                    percentageOfVotes = driver.find_element(By.XPATH, f'/html/body/div[3]/div[3]/div[5]/div[1]/table[2]/tbody/tr[{m}]/td[{n}]').text
                                elif n==7:
                                    results = driver.find_element(By.XPATH, f'/html/body/div[3]/div[3]/div[5]/div[1]/table[2]/tbody/tr[{m}]/td[{n}]').text
                            politicalInfo = "Election: " + election+ ", Year: "+ year+ ", District: "+ district+ ", PartyAffliation: "+ PartyAffliation+ ", votes: "+ votes+ ", Percentage Of Votes: "+ percentageOfVotes+", Results: "+results
                            politicalCareerInfo = politicalCareerInfo + "; "+ politicalInfo
                        print(politicalCareerInfo)
                    if fullName in head:
                        rawNameKorean = driver.find_element(By.XPATH, f'/html/body/div[3]/div[3]/div[5]/div[1]/table[2]/tbody/tr[2]').text
                        rawNameChinese = driver.find_element(By.XPATH, f'/html/body/div[3]/div[3]/div[5]/div[1]/table[2]/tbody/tr[3]').text
                        rawName = rawNameKorean + "; " + rawNameChinese
                        print(rawName)
                    
                except:
                    pass
                try:
                    list5 = driver.find_elements(By.XPATH, f'/html/body/div[3]/div[3]/div[5]/div[1]/table[3]/tbody/tr')
                    head = driver.find_element(By.XPATH, f'/html/body/div[3]/div[3]/div[5]/div[1]/table[3]/tbody/tr[1]').text
                    if "Election" in head:
                        for m in range(2, len(list5)+1):
                            list6 = driver.find_elements(By.XPATH, f'/html/body/div[3]/div[3]/div[5]/div[1]/table[3]/tbody/tr[{m}]/td')
                            for n in range(1, len(list6)+1):
                                if n==1:
                                    election = driver.find_element(By.XPATH, f'/html/body/div[3]/div[3]/div[5]/div[1]/table[3]/tbody/tr[{m}]/td[{n}]').text
                                elif n==2:
                                    year = driver.find_element(By.XPATH, f'/html/body/div[3]/div[3]/div[5]/div[1]/table[3]/tbody/tr[{m}]/td[{n}]').text
                                elif n==3:
                                    district = driver.find_element(By.XPATH, f'/html/body/div[3]/div[3]/div[5]/div[1]/table[3]/tbody/tr[{m}]/td[{n}]').text
                                elif n==4:
                                    PartyAffliation = driver.find_element(By.XPATH, f'/html/body/div[3]/div[3]/div[5]/div[1]/table[3]/tbody/tr[{m}]/td[{n}]').text
                                elif n==5:
                                    votes = driver.find_element(By.XPATH, f'/html/body/div[3]/div[3]/div[5]/div[1]/table[3]/tbody/tr[{m}]/td[{n}]').text
                                elif n==6:
                                    percentageOfVotes = driver.find_element(By.XPATH, f'/html/body/div[3]/div[3]/div[5]/div[1]/table[3]/tbody/tr[{m}]/td[{n}]').text
                                elif n==7:
                                    results = driver.find_element(By.XPATH, f'/html/body/div[3]/div[3]/div[5]/div[1]/table[3]/tbody/tr[{m}]/td[{n}]').text
                            politicalInfo = "Election: " + election+ ", Year: "+ year+ ", District: "+ district+ ", PartyAffliation: "+ PartyAffliation+ ", votes: "+ votes+ ", Percentage Of Votes: "+ percentageOfVotes+", Results: "+results
                            politicalCareerInfo = politicalCareerInfo + "; "+ politicalInfo
                        print(politicalCareerInfo)
                    if fullName in head:
                        rawNameKorean = driver.find_element(By.XPATH, f'/html/body/div[3]/div[3]/div[5]/div[1]/table[3]/tbody/tr[2]').text
                        rawNameChinese = driver.find_element(By.XPATH, f'/html/body/div[3]/div[3]/div[5]/div[1]/table[3]/tbody/tr[3]').text
                        rawName = rawNameKorean + "; " + rawNameChinese
                        print(rawName)
                except:
                    pass
                list7 = driver.find_elements(By.XPATH, f'/html/body/div[3]/div[3]/div[5]/div[1]/p')
                additionalInfo = ""
                for o in range (1, len(list7)+1):
                    info = driver.find_element(By.XPATH, f'/html/body/div[3]/div[3]/div[5]/div[1]/p[{o}]').text
                    additionalInfo = additionalInfo + info
                    additionalInfo = re.sub(r'\[[0-9]*\]','',additionalInfo)
#                 print(additionalInfo)
                try:
                    x = text_sum(str(additionalInfo))
                    summary = x
                except:
                    summary = fullName+ " is a South Korean Women in politics."

                print("*"*50)
                driver.back()
                if fullName:
                    data_dict['fullName'] = fullName
                if rawName:
                    data_dict['rawName'] = rawName
                if image:
                    data_dict['image'] = image
                if dob:
                    data_dict['dob'] = dob
                if age:
                    data_dict['age'] = age
                if placeOfBirthCity:
                    data_dict['placeOfBirthCity'] = placeOfBirthCity
                if constituency:
                    data_dict['constituency'] = constituency
                if politicalParty:
                    data_dict['politicalParty'] = politicalParty
                if educationInfo:
                    data_dict['educationInfo'] = educationInfo
                if familyInfo:
                    data_dict['familyInfo'] = familyInfo
                if importantDates:
                    data_dict['importantDates'] = importantDates
                if religion:
                    data_dict['religion'] = religion
                if politicalCareerInfo:
                    data_dict['politicalCareerInfo'] = politicalCareerInfo
                if additionalInfo:
                    data_dict['description'] = summary
                if summary:
                    data_dict['summary'] = additionalInfo
                data_list.append(data_dict)
        driver.back()
    return data_list
    


# In[107]:


if __name__ == '__main__':
    data_list = get_data("add_slug_name")
    to_json(data_list)


# In[ ]:




