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


# In[3]:


def get_data(slug_name):
    data_list = []
    url = "http://www.barrington.ag/list-commercial-banks-antigua-barbuda/"
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized") 
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--log-level=3")
    translator = GoogleTranslator(target='english')
    driver = webdriver.Chrome(options=options)
    driver.get(url)
    list1 = driver.find_elements(By.XPATH, f'/html/body/div/div/div/main/article/div[2]/div/div/h4')
    for i in range(1, len(list1)+1):
        data_dict = {}
        fullName = driver.find_element(By.XPATH, f'/html/body/div/div/div/main/article/div[2]/div/div[{i}]/h4').text
        print(fullName)
        description = driver.find_element(By.XPATH, f'/html/body/div/div/div/main/article/div[2]/div/div[{i}]/p[1]').text
        print(description)
        summary = fullName + " is one of the Commercial Banks in Antigua and Barbuda."
        if fullName:
            data_dict['fullName'] = fullName
        if description:
            data_dict['description'] = description
        if summary:
            data_dict['summary'] = summary
        data_list.append(data_dict)
    driver.quit()
    return data_list


# In[4]:


if __name__ == '__main__':
    data_list = get_data("add_slug_name")
    to_json(data_list)


# In[ ]:




