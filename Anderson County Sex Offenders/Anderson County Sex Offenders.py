#!/usr/bin/env python
# coding: utf-8

# In[9]:


from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import json
import re
from deep_translator import GoogleTranslator


# In[10]:


def to_json(data):
    """
    This function takes list of dictionary as Input and 
    then Creates a JSON file in which Input data is stored
    """
    with open("data_dict.json", "w") as outfile:
        json.dump(data, outfile,indent=4)
        outfile.close()


# In[11]:


def get_data(slug_name):
    data_list = []
    url = "http://stopyouchildmolester.blogspot.com/2012/09/anderson-county-sex-offenders.html"
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized") 
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--log-level=3")
    translator = GoogleTranslator(target='english')
    driver = webdriver.Chrome(options=options)
    driver.get(url)
    list1 = driver.find_elements(By.XPATH, f'//table[2]/tbody/tr/td[2]/table/tbody/tr[1]/td[2]/div/div/table/tbody/tr')
    for i in range(2, len(list1)+1):
        list2 = driver.find_elements(By.XPATH, f'//table[2]/tbody/tr/td[2]/table/tbody/tr[1]/td[2]/div/div/table/tbody/tr[{i}]/td')
        data_dict ={}
        lastUpdatedAt = driver.find_element(By.XPATH, f'/html/body/div[3]/div[2]/div[2]/div[2]/div[2]/div[2]/div[2]/div/div[4]/div[1]/div/div/div/div[1]/div/h2').text
        offence = "Public Sex Offender"
        for j in range(1, len(list2)+1):
            if j==1:
                fullName = driver.find_element(By.XPATH, f'//table[2]/tbody/tr/td[2]/table/tbody/tr[1]/td[2]/div/div/table/tbody/tr[{i}]/td[{j}]').text
                firstName = fullName.split(",")[1].strip()
                lastName = fullName.split(",")[0].strip()
                fullName = firstName + " " + lastName
            if j==2:
                dob = driver.find_element(By.XPATH, f'//table[2]/tbody/tr/td[2]/table/tbody/tr[1]/td[2]/div/div/table/tbody/tr[{i}]/td[{j}]').text
                dob_dmy = dob.split("/")
                d = dob_dmy[1]
                m = dob_dmy[0]
                y = dob_dmy[2]
                dob_dmy = d + "/" + m + "/" + y
            if j==3:
                gender = driver.find_element(By.XPATH, f'//table[2]/tbody/tr/td[2]/table/tbody/tr[1]/td[2]/div/div/table/tbody/tr[{i}]/td[{j}]').text
                if gender == "M":
                    gender = "Male"
                elif gender == "":
                    gender = "Female"
            if j==4:
                race = driver.find_element(By.XPATH, f'//table[2]/tbody/tr/td[2]/table/tbody/tr[1]/td[2]/div/div/table/tbody/tr[{i}]/td[{j}]').text
                if race == "B":
                    race = "Black"
                if race == "W":
                    race = "White"
            if j==5:
                fullAddress = driver.find_element(By.XPATH, f'//table[2]/tbody/tr/td[2]/table/tbody/tr[1]/td[2]/div/div/table/tbody/tr[{i}]/td[{j}]').text
                fullAddress = fullAddress.replace("\n", ", ")
        summary = fullName + " is a registered public sex offender in Anderson County."
        if fullName:
            data_dict['fullName'] = fullName
        if dob:
            data_dict['dob'] = dob_dmy
        if gender:
            data_dict['gender'] = gender
        if race:
            data_dict['race'] = race
        if offence:
            data_dict['offence'] = offence
        if fullAddress:
            data_dict['fullAddress'] = fullAddress
        if lastUpdatedAt:
            data_dict['lastUpdatedAt'] = lastUpdatedAt
        if summary:
            data_dict['summary'] = summary
        data_list.append(data_dict)
    driver.quit()
    return data_list


# In[12]:


if __name__ == '__main__':
    data_list = get_data("add_slug_name")
    to_json(data_list)


# In[ ]:




