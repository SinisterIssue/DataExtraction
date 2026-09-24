#!/usr/bin/env python
# coding: utf-8

# In[20]:


from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import json
import re
from deep_translator import GoogleTranslator


# In[21]:


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
    url = "https://corporatefinanceinstitute.com/resources/careers/companies/top-banks-in-argentina/"
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized") 
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--log-level=3")
    translator = GoogleTranslator(target='english')
    driver = webdriver.Chrome(options=options)
    driver.get(url)
    info = driver.find_element(By.XPATH, f'/html/body/div[2]/div[2]/div/div/div/section[1]').text
    list1 = driver.find_elements(By.XPATH, f'/html/body/div[2]/div[2]/div/div/div/section[1]/h4')
    for i in range(1, len(list1)+1):
        data_dict = {}
        fullName = driver.find_element(By.XPATH, f'/html/body/div[2]/div[2]/div/div/div/section[1]/h4[{i}]').text
        try:
            nextName = driver.find_element(By.XPATH, f'/html/body/div[2]/div[2]/div/div/div/section[1]/h4[{i+1}]').text
        except:
            nextName = ""
        try:
            ele_info = info.split(fullName, 1)[1].split(nextName, 1)[0]
            netIncome = ele_info.split("Net Income:", 1)[1].split("\n",1)[0].strip()
            print(netIncome)
            totalAssets = ele_info.split("Total assets:", 1)[1].split("\n", 1)[0].strip()
            print(totalAssets)
            description = ele_info.replace("\n", " ").replace("Net Income: "+netIncome, "").replace("Total assets: "+totalAssets, "").strip()
            print(description)
        except:
            ele_info = info.split(fullName, 1)[1].split("Careers in Investment Banking", 1)[0]
            netIncome = ele_info.split("Net Income:", 1)[1].split("\n",1)[0].strip()
            print(netIncome)
            totalAssets = ele_info.split("Total assets:", 1)[1].split("\n", 1)[0].strip()
            print(totalAssets)
            description = ele_info.replace("\n", " ").replace("Net Income: "+netIncome, "").replace("Total assets: "+totalAssets, "").strip()
            print(description)
        summary = fullName + " is one of the top banks in Argentina with Net Income: " + netIncome + "and Total Assests: "+ totalAssets
        if fullName:
            data_dict['fullName'] = fullName
        if  netIncome:
            data_dict['netIncome'] = netIncome
        if totalAssets:
            data_dict['totalAssets'] = totalAssets
        if description:
            data_dict['description'] = description
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




