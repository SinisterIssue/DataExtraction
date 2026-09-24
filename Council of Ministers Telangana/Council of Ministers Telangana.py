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
    url = "https://www.telangana.gov.in/Government/Council-of-Ministers"
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized") 
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--log-level=3")
    translator = GoogleTranslator(target='english')
    driver = webdriver.Chrome(options=options)
    driver.get(url)
    list1 = driver.find_elements(By.XPATH, f'//div/div[2]/div/div[2]/div/div/div/div/div/div[1]/table/tbody/tr')
    for i in range(1, len(list1)+1):
        list2 = driver.find_elements(By.XPATH, f'//div/div[2]/div/div[2]/div/div/div/div/div/div[1]/table/tbody/tr[{i}]/td')
        data_dict = {}
        fax = ""
        for j in range(1, len(list2)+1):
            if j==1:
                image = driver.find_element(By.XPATH, f'//div/div[2]/div/div[2]/div/div/div/div/div/div[1]/table/tbody/tr[{i}]/td[{j}]/a/img').get_attribute("src")
            if j==2:
                fullName = driver.find_element(By.XPATH, f'//div/div[2]/div/div[2]/div/div/div/div/div/div[1]/table/tbody/tr[{i}]/td[{j}]').text
                prefix = fullName.split(" ", 1)[0]
                fullName = fullName.split(" ", 1)[1].strip()
            if j==3:
                careerInfoDesignation = driver.find_element(By.XPATH, f'//div/div[2]/div/div[2]/div/div/div/div/div/div[1]/table/tbody/tr[{i}]/td[{j}]').text
                careerInfoDesignation = careerInfoDesignation.replace("\n", "").replace(",All the portfolios not allocated to any Minister", "")
                if "Minister" not in careerInfoDesignation:
                    careerInfoDesignation = careerInfoDesignation + " Minister"
            if j==4:
                constituency = driver.find_element(By.XPATH, f'//div/div[2]/div/div[2]/div/div/div/div/div/div[1]/table/tbody/tr[{i}]/td[{j}]').text
            if j==6:
                telephoneNos = driver.find_element(By.XPATH, f'//div/div[2]/div/div[2]/div/div/div/div/div/div[1]/table/tbody/tr[{i}]/td[{j}]').text.replace("\n", "")
                try:
                    fax = telephoneNos.split("Fax:")[1].strip()
                    telephoneNos = telephoneNos.split("Fax:")[0]
                except:
                    pass
        summary = fullName + " is the " + careerInfoDesignation + " of Telangana." 
        if fullName:
            data_dict['fullName'] = fullName
        if prefix:
            data_dict['prefix'] = prefix
        if image:
            data_dict['image'] = image
        if careerInfoDesignation:
            data_dict['careerInfoDesignation'] = careerInfoDesignation
        if constituency:
            data_dict['constituency'] = constituency
        if telephoneNos:
            data_dict['telephoneNos'] = telephoneNos
        if fax:
            data_dict['fax'] = fax
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




