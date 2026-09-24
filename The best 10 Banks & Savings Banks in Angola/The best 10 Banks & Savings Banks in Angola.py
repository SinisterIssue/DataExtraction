#!/usr/bin/env python
# coding: utf-8

# In[7]:


from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import json
import re
from deep_translator import GoogleTranslator


# In[8]:


def to_json(data):
    """
    This function takes list of dictionary as Input and 
    then Creates a JSON file in which Input data is stored
    """
    with open("data_dict.json", "w") as outfile:
        json.dump(data, outfile,indent=4)
        outfile.close()


# In[9]:


def get_data(slug_name):
    data_list = []
    url = "https://www.africanadvice.com/Banks_And_Savings_Banks/Angola/"
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized") 
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--log-level=3")
    translator = GoogleTranslator(target='english')
    driver = webdriver.Chrome(options=options)
    driver.get(url)
    list1 = driver.find_elements(By.XPATH, f'/html/body/form/div[3]/div[1]/div[2]/div[4]/div/div[1]/span/a[2]')
    for i in range(1, len(list1)+1):
        data_dict = {}
        fullName = driver.find_element(By.XPATH, f'/html/body/form/div[3]/div[1]/div[2]/div[4]/div/div[1]/span[{i}]/a[2]').text
        print(fullName)
        info = driver.find_element(By.XPATH, f'/html/body/form/div[3]/div[1]/div[2]/div[4]/div/div[1]/span[{i}]/p').text
        fullAddress = info.split("\n")[0].replace("Address:", "").replace("See full address and map.", "").strip()
        category = info.split("\n")[1].replace("Categories:", "").strip()
        print(fullAddress)
        print(category)
        summary = fullName + " is one of the best Banks and Saving Banks in Angola during the year 2022."
        if fullName:
            data_dict['fullName'] = fullName
        if fullAddress:
            data_dict['fullAddress'] = fullAddress
        if category:
            data_dict['category'] = category
        if summary:
            data_dict['summary'] = summary
        data_list.append(data_dict)
    driver.quit()
    return data_list


# In[10]:


if __name__ == '__main__':
    data_list = get_data("add_slug_name")
    to_json(data_list)


# In[ ]:




