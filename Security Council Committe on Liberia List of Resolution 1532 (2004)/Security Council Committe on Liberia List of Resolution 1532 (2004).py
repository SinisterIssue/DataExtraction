#!/usr/bin/env python
# coding: utf-8

# In[15]:


from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import json
import re
from deep_translator import GoogleTranslator


# In[16]:


def to_json(data):
    """
    This function takes list of dictionary as Input and 
    then Creates a JSON file in which Input data is stored
    """
    with open("data_dict.json", "w") as outfile:
        json.dump(data, outfile,indent=4)
        outfile.close()


# In[17]:


def get_data(slug_name):
    data_list = []
    url = "https://press.un.org/en/2004/sc8147.doc.htm"
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized") 
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--log-level=3")
    translator = GoogleTranslator(target='english')
    driver = webdriver.Chrome(options=options)
    driver.get(url)
    list1 = driver.find_elements(By.XPATH, f'/html/body/div/div[1]/main/div/div/div[2]/article/div/div[2]/div/div/div[2]/div/div[3]/div/div[2]/div/blockquote/div/table/tbody/tr')
    for i in range(1, len(list1)+1):
        list2 = driver.find_elements(By.XPATH, f'/html/body/div/div[1]/main/div/div/div[2]/article/div/div[2]/div/div/div[2]/div/div[3]/div/div[2]/div/blockquote/div/table/tbody/tr[{i}]/td')
        data_dict = {}
        for j in range(1, len(list2)+1):
            if j==1:
                lastName = driver.find_element(By.XPATH, f'/html/body/div/div[1]/main/div/div/div[2]/article/div/div[2]/div/div/div[2]/div/div[3]/div/div[2]/div/blockquote/div/table/tbody/tr[{i}]/td[{j}]').text
                print(lastName)
            if j==2:
                firstName = driver.find_element(By.XPATH, f'/html/body/div/div[1]/main/div/div/div[2]/article/div/div[2]/div/div/div[2]/div/div[3]/div/div[2]/div/blockquote/div/table/tbody/tr[{i}]/td[{j}]').text
                print(firstName)
            if j==3:
                alias = driver.find_element(By.XPATH, f'/html/body/div/div[1]/main/div/div/div[2]/article/div/div[2]/div/div/div[2]/div/div[3]/div/div[2]/div/blockquote/div/table/tbody/tr[{i}]/td[{j}]').text
                alias = alias.replace("\n", " ").replace("                    ", "").strip()
                print(alias)
            if j==4:
                listOfdob = driver.find_element(By.XPATH, f'/html/body/div/div[1]/main/div/div/div[2]/article/div/div[2]/div/div/div[2]/div/div[3]/div/div[2]/div/blockquote/div/table/tbody/tr[{i}]/td[{j}]').text
                listOfdob = listOfdob.replace("\n", "; ").replace("                             ", " ").replace("   ", " ").strip()
                print(listOfdob)
                dob = listOfdob.split("(")[0].strip()
                print(dob)
            if j==5:
                passport = driver.find_element(By.XPATH, f'/html/body/div/div[1]/main/div/div/div[2]/article/div/div[2]/div/div/div[2]/div/div[3]/div/div[2]/div/blockquote/div/table/tbody/tr[{i}]/td[{j}]').text
                passport = passport.replace("\n", "; ")
            if j==6:
                careerInfo = driver.find_element(By.XPATH, f'/html/body/div/div[1]/main/div/div/div[2]/article/div/div[2]/div/div/div[2]/div/div[3]/div/div[2]/div/blockquote/div/table/tbody/tr[{i}]/td[{j}]').text
        fullName = firstName + " " + lastName
        fullName = fullName.title()
        identifierType = "Passport: " + passport
        if ";" in dob:
            dob = dob.split(";")[0]
        if identifierType.split(":")[1].strip() == "":
            identifierType = ""
        summary = fullName + " is one of the Entities Subject to ASSETS FREEZE LIST OF RESOLUTION 1532 (2004). " + "On 13 July 2004, the Security Council Committee established pursuant to resolution 1521 (2003) concerning Liberia decided to update the information associated with the following two individuals on the list of individuals and entities subject to this measured."
        print("*"*50)
        if fullName:
            data_dict['fullName'] = fullName
        if alias:
            data_dict['alias'] = alias
        if dob:
            data_dict['dob'] = dob.strip()
        if listOfdob:
            data_dict['listOfDob'] = listOfdob.strip()
        if identifierType:
            data_dict['identifierType'] = identifierType
        if careerInfo:
            data_dict['careerInfo'] = careerInfo
        if summary:
            data_dict['summary'] = summary
        data_list.append(data_dict)
    driver.quit()
    return data_list


# In[18]:


if __name__ == '__main__':
    data_list = get_data("add_slug_name")
    to_json(data_list)


# In[ ]:




