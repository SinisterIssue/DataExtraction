#!/usr/bin/env python
# coding: utf-8

# In[1]:


from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import json
import re
from deep_translator import GoogleTranslator


# In[2]:


def to_json(data):
    """
    This function takes list of dictionary as Input and 
    then Creates a JSON file in which Input data is stored
    """
    with open("data_dict.json", "w") as outfile:
        json.dump(data, outfile,indent=4)
        outfile.close()


# In[53]:


def get_data(slug_name):
    data_list = []
    url = "https://www.mylondon.news/news/nostalgia/londons-most-notorious-gangsters-15681776"
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized") 
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--log-level=3")
    translator = GoogleTranslator(target='english')
    driver = webdriver.Chrome(options=options)
    driver.get(url)
    for j in range(1, 3):
        data_dict = {}
        fullName = ""
        fullName = driver.find_element(By.XPATH, f'/html/body/main/article/div[4]/div/div[2]/h3[1]').text
        if fullName =="1. The Kray twins" and j==1:
            fullName = "Ronnie Kray"
    #         print(fullName)
            description = driver.find_element(By.XPATH, f'/html/body/main/article/div[4]/div/div[2]').text
            description = description.split("1. The Kray twins", 1)[1].split("2. Jack", 1)[0].split("\n",2)[2]
            description = description.replace("\n", " ").strip()
    #         print(description)
            dob = description.split("born on")[1].split(",")[0].strip()
    #         print(dob)
            alias= "The Kray twins"
            image = driver.find_element(By.XPATH, f'/html/body/main/article/div[4]/div/div[2]/figure[1]/div/div[2]/img').get_attribute("src")
        if fullName =="1. The Kray twins" and j==2:
            fullName = "Reggie Kray"
    #         print(fullName)
            description = driver.find_element(By.XPATH, f'/html/body/main/article/div[4]/div/div[2]').text
            description = description.split("1. The Kray twins", 1)[1].split("2. Jack", 1)[0].split("\n",2)[2]
            description = description.replace("\n", " ").strip()
    #         print(description)
            dob = description.split("born on")[1].split(",")[0].strip()
    #         print(dob)
            alias= "The Kray twins"
            image = driver.find_element(By.XPATH, f'/html/body/main/article/div[4]/div/div[2]/figure[1]/div/div[2]/img').get_attribute("src")
        summary = fullName + " was one of the London's most notorious gangsters."
        if fullName:
            data_dict['fullName'] = fullName
        if alias:
            data_dict['alias'] = alias
        if image:
            data_dict['image'] = image
        if dob:
            data_dict['dob'] = dob
        if description:
            data_dict['description'] = description
        if summary:
            data_dict['summary']= summary
        data_list.append(data_dict)
    list1 = driver.find_elements(By.XPATH, f'/html/body/main/article/div[4]/div/div[2]/h3')
    for i in range(3, len(list1)+1):
        try:
            image = ""
            description = ""
            fullName = ""
            alias = ""
            data_dict2 ={} 
            fullName = driver.find_element(By.XPATH, f'/html/body/main/article/div[4]/div/div[2]/h3[{i}]').text
            nextName = driver.find_element(By.XPATH, f'/html/body/main/article/div[4]/div/div[2]/h3[{i+1}]').text
            description = driver.find_element(By.XPATH, f'/html/body/main/article/div[4]/div/div[2]').text
            description = description.split(fullName)[1].split(nextName)[0].strip()
            try:
                description = description.split(")", 1)[1].strip()
            except:
                pass
            description = description.replace("RELATED ARTICLES", "").replace("The Crown series 4: Who was Michael Fagan who broke into Buckingham Palace while The Queen was asleep?", "").replace("The abandoned tunnel network under London built in secret by the Post Office, BT and the MoD", "")
            description = description.replace("The brutal story behind the name of the busiest London Underground station", "").replace("London's Titanic: The tragic day 650 Londoners drowned in a river full of poo", "")
            description = description.replace("The spooky ghost story of the monk who died at Buckingham Palace", "").replace("Why are MI5 and MI6 so famous and what happened to the other secret Military Intelligence departments", "")
            description = description.replace("Des on ITV: The chilling letters Dennis Nilsen sent to police and TV producers from prison", "").replace("The man who was the 'real' Robin Hood and the amazing thing that happened to him in London", "")
            description = description.replace("\n", " ")


            if '"' in fullName:
                alias = fullName.split('"', 1)[1].split('"', 1)[0]
                print(alias)
                fullName = fullName.replace('"'+ alias+'"', "").replace("  ", " ")
            fullName = fullName.split(".",1)[1].replace(" and ", " ").strip()


            if fullName == "Jack Comer":
                image = driver.find_element(By.XPATH, f'/html/body/main/article/div[4]/div/div[2]/figure[2]/div/div[2]/img').get_attribute("src")
            if fullName == "Billy Hill":
                image = driver.find_element(By.XPATH, f'/html/body/main/article/div[4]/div/div[2]/figure[3]/div/div[2]/img').get_attribute("src")
            if fullName == "Frankie Fraser":
                image = driver.find_element(By.XPATH, f'/html/body/main/article/div[4]/div/div[2]/figure[4]/div/div[2]/img').get_attribute("src")

        except:
            pass
        if i == len(list1):
            fullName = driver.find_element(By.XPATH, f'/html/body/main/article/div[4]/div/div[2]/h3[10]').text
            lastInfo = driver.find_elements(By.XPATH, f'/html/body/main/article/div[4]/div/div[2]/p')
            for k in range(49, len(lastInfo)+1):
                description = description + driver.find_element(By.XPATH, f'/html/body/main/article/div[4]/div/div[2]/p[{k}]').text 
            alias = fullName.split('"', 1)[1].split('"', 1)[0]
            print(alias)
            fullName = fullName.replace('"'+ alias+'"', "").replace("  ", " ")
            fullName = fullName.split(".",1)[1].replace(" and ", " ").strip()
        summary = fullName + " was one of the London's most notorious gangsters."
        print(fullName)
        print(description)
        print("*"*50)
        if fullName:
            data_dict2['fullName'] = fullName
        if alias:
            data_dict2['alias'] = alias
        if image:
            data_dict2['image'] = image
        if description:
            data_dict2['description'] = description
        if summary:
            data_dict2['summary']= summary
        data_list.append(data_dict2)
    driver.quit()
    return data_list


# In[54]:


if __name__ == '__main__':
    data_list = get_data("add_slug_name")
    to_json(data_list)


# In[ ]:




