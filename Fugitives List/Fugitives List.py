#!/usr/bin/env python
# coding: utf-8

# In[22]:


from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import json
import re
from deep_translator import GoogleTranslator


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


def get_data(slug_name):
    data_list = []
    url = "http://genealogytrails.com/tex/panhandle2/archer/county_1900fug.html"
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized") 
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--log-level=3")
    translator = GoogleTranslator(target='english')
    driver = webdriver.Chrome(options=options)
    driver.get(url)
    list1 = driver.find_elements(By.XPATH, f'/html/body/center/table/tbody/tr/td/table[2]/tbody/tr/td/div[6]/p')
    for i in range(3, len(list1)+1):
        data_dict = {}
        complexion  =""
        race = ""
        info = driver.find_element(By.XPATH, f'/html/body/center/table/tbody/tr/td/table[2]/tbody/tr/td/div[6]/p[{i}]').text
        fullName = info.split("\n")[0]
        firstName = fullName.split(",")[1]
        lastName = fullName.split(",")[0]
        fullName = firstName+" "+lastName
        info = info.split("\n")[1]
        crime = info.split(".")[0]
        print(crime)
        print(info.split("."))
        additionalInfo = info.split(".")[2]
        try:
            additionalInfo = info.split(".")[3] + info.split(".")[4] + additionalInfo
        except:
            pass
        info = info.split(".")[1]
        info = info.split(",")
        for j in range(0, len(info)):
            if "Age" in info[j]:
                age = info[j].split("Age")[1].strip()
                print(age)
            if "height" in info[j]:
                height = info[j].split("height")[1].strip()
                height = height.replace(" feet", "'").replace(' inches', '"').strip()
                print(height)
            if "weight" in info[j]:
                weight = info[j].split("weight")[1].strip()
            if "color" in info[j]:
                race = info[j].split("color")[1].strip()
            if "complexion" in info[j]:
                complexion = info[j].split("complexion")[1].strip()
            if "eyes" in info[j]:
                eyes = info[j].split("eyes")[1].strip()
            if "hair" in info[j]:
                hair = info[j].split("hair")[1].strip()
            if "occupation" in info[j]:
                careerInfoDesignation = info[j].split("occupation")[1].strip()
        fullName = fullName.strip()
        additionalInfo = additionalInfo.strip()
        summary = fullName + " is present in the 1900 List of Fugitives from Justice in Archer County, Texas."
        if fullName:
            data_dict['fullName'] = fullName
        if crime:
            data_dict['crime'] = crime
        if careerInfoDesignation:
            data_dict['careerInfoDesignation'] = careerInfoDesignation
        if age:
            data_dict['age'] = age
        if height:
            data_dict['height'] = height
        if weight:
            data_dict['weight'] = weight
        if race:
            data_dict['race'] = race
        if complexion:
            data_dict['complexion'] = complexion
        if eyes:
            data_dict['eyes'] = eyes
        if hair:
            data_dict['hair'] = hair
        if additionalInfo:
            data_dict['additionalInfo'] = additionalInfo
        if summary:
            data_dict['summary'] = summary
        data_list.append(data_dict)
    driver.quit()
    return data_list


# In[25]:


if __name__ == '__main__':
    data_list = get_data("add_slug_name")
    to_json(data_list)


# In[ ]:




