#!/usr/bin/env python
# coding: utf-8

# In[23]:


from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import json
import re
from deep_translator import GoogleTranslator


# In[24]:


def to_json(data):
    """
    This function takes list of dictionary as Input and 
    then Creates a JSON file in which Input data is stored
    """
    with open("data_dict.json", "w") as outfile:
        json.dump(data, outfile,indent=4)
        outfile.close()


# In[25]:


def get_data(slug_name):
    data_list = []
    url = "https://www1.nyc.gov/site/doi/about/executive-staffs.page"
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized") 
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--log-level=3")
    translator = GoogleTranslator(target='english')
    driver = webdriver.Chrome(options=options)
    driver.get(url)
    list1 = driver.find_elements(By.XPATH, f'//div/div[2]/div/div/div/div[2]/div/ul/li')
    # print(len(list1))
    for i in range(1, len(list1)+1):
        data_dict = {}
        careerInfo = ""
        educationInfo = ""
        fullName = driver.find_element(By.XPATH, f'//div/div[2]/div/div/div/div[2]/div/ul/li[{i}]').text
        careerInfoDesignation = fullName.split(",")[1].strip()
        fullName = fullName.split(",")[0]
        print(fullName)
        print(careerInfoDesignation)
        driver.find_element(By.XPATH, f'//div/div[2]/div/div/div/div[2]/div/ul/li[{i}]/a').click()
        time.sleep(2)
        image = driver.find_element(By.XPATH, f'//div/div[1]/div/div[2]/div/div/div/div[2]/div/div[1]/img').get_attribute('src')
        print(image)
        list2 = driver.find_elements(By.XPATH, f'//div/div[1]/div/div[2]/div/div/div/div[2]/div/p')
        for j in range(1, len(list2)+1):
            info = driver.find_element(By.XPATH, f'//div/div[1]/div/div[2]/div/div/div/div[2]/div/p[{j}]').text
            if "graduate" not in info:
                careerInfo = careerInfo + "; "+  info
            if "graduate" in info:
                educationInfo = info
        careerInfo = careerInfo.replace("; ", "", 1)
        print(careerInfo)
        print(educationInfo)
        summary = fullName + " is the "+ careerInfoDesignation + " of the New York City Department Of Investigation."
        driver.back()
        if fullName:
            data_dict['fullName'] = fullName
        if careerInfoDesignation:
            data_dict['careerInfoDesignation'] = careerInfoDesignation
        if image:
            data_dict['image'] = image
        if careerInfo:
            data_dict['careerInfo'] = careerInfo
        if educationInfo:
            data_dict['educationInfo'] = educationInfo
        if summary:
            data_dict['summary'] = summary
        data_list.append(data_dict)
    driver.quit()
    return data_list


# In[26]:


if __name__ == '__main__':
    data_list = get_data("add_slug_name")
    to_json(data_list)


# In[ ]:




