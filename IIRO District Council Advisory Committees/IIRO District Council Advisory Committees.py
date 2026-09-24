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


# In[8]:


def get_data(slug_name):    
    data_list = []
    url = "https://www.iiroc.ca/about-iiroc"
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized") 
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--log-level=3")
    translator = GoogleTranslator(target='english')
    driver = webdriver.Chrome(options=options)
    driver.get(url)
    list1 = driver.find_elements(By.XPATH, f'/html/body/div[2]/div[1]/div[1]/div[2]/div/article/div/div[2]/div/nav/ul/li[8]/ul/li/a')
    for i in range(1, len(list1)+1):
        council = driver.find_element(By.XPATH, f'/html/body/div[2]/div[1]/div[1]/div[2]/div/article/div/div[2]/div/nav/ul/li[8]/ul/li[{i}]/a').text
        print(council)
        driver.find_element(By.XPATH, f'/html/body/div[2]/div[1]/div[1]/div[2]/div/article/div/div[2]/div/nav/ul/li[8]/ul/li[{i}]/a').click()
        time.sleep(2)
        list2 = driver.find_elements(By.XPATH, f'/html/body/div[2]/div[1]/div[1]/div[2]/div[3]/div/div[1]/div[2]/div/div/article/div[1]/div/div/div/table/tbody/tr')
        for j in range(1, len(list2)+1):
            careerInfoDesignation = ""
            data_dict = {}
            list3 = driver.find_elements(By.XPATH, f'/html/body/div[2]/div[1]/div[1]/div[2]/div[3]/div/div[1]/div[2]/div/div/article/div[1]/div/div/div/table/tbody/tr[{j}]/td')
            for k in range(1, len(list3)+1):
                if k==1:
                    fullName = driver.find_element(By.XPATH, f'/html/body/div[2]/div[1]/div[1]/div[2]/div[3]/div/div[1]/div[2]/div/div/article/div[1]/div/div/div/table/tbody/tr[{j}]/td[{k}]').text
                    if "," in fullName:
                        careerInfoDesignation = fullName.split(",")[1].strip()
                        fullName = fullName.split(",")[0]
                    print(fullName)
                    print(careerInfoDesignation)
                if k==2:
                    organizaion = driver.find_element(By.XPATH, f'/html/body/div[2]/div[1]/div[1]/div[2]/div[3]/div/div[1]/div[2]/div/div/article/div[1]/div/div/div/table/tbody/tr[{j}]/td[{k}]').text
                    print(organizaion)
            additionalInfo = "Council: " + council+  "; Organization: " + organizaion
            if careerInfoDesignation == "":
                summary = fullName + " is a part of " + council + " and the "+  organizaion + " organization."
            else:
                summary = fullName + " is the chair for " + council + " and the " + organizaion + " organization."
            print("*"*50)
            if fullName:
                data_dict['fullName'] = fullName
            if careerInfoDesignation:
                data_dict['careerInfoDesignation'] = careerInfoDesignation
            if additionalInfo:
                data_dict['additionalInfo'] = additionalInfo
            if summary:
                data_dict['summary'] = summary
            data_list.append(data_dict)
        driver.back()
    driver.quit()
    return data_list


# In[9]:


if __name__ == '__main__':
    data_list = get_data("add_slug_name")
    to_json(data_list)


# In[ ]:




