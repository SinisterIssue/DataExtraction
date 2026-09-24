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
    url = "https://www.swiftbic.com/banks-in-AFGHANISTAN.html"
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized") 
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--log-level=3")
    translator = GoogleTranslator(target='english')
    driver = webdriver.Chrome(options=options)
    driver.get(url)
    list1 = driver.find_elements(By.XPATH, f'/html/body/div[1]/div[2]/div/div[1]/table/tbody/tr')
    for i in range(1, len(list1)+1):
        list2 = driver.find_elements(By.XPATH, f'/html/body/div[1]/div[2]/div/div[1]/table/tbody/tr[{i}]/td')
        data_dict = {}
        branch=""
        city =""
        fullAddress=""
        country =""
        for j in range(1, len(list2)+1):
            if j==1:
                fullName = driver.find_element(By.XPATH, f'/html/body/div[1]/div[2]/div/div[1]/table/tbody/tr[{i}]/td[{j}]').text
                print(fullName)
            if j==2:
                branch = driver.find_element(By.XPATH, f'/html/body/div[1]/div[2]/div/div[1]/table/tbody/tr[{i}]/td[{j}]').text
                print(branch)
            if j==3:
                city = driver.find_element(By.XPATH, f'/html/body/div[1]/div[2]/div/div[1]/table/tbody/tr[{i}]/td[{j}]').text
                print(city)
        link = driver.find_element(By.XPATH, f'/html/body/div[1]/div[2]/div/div[1]/table/tbody/tr[{i}]/td[4]/a').get_attribute("href")
        driver.execute_script("window.open('');")
        driver.switch_to.window(driver.window_handles[1])
        driver.get(link)
        country = "Afghanistan"
        try:
            fullAddress = driver.find_element(By.XPATH, f'/html/body/div[1]/div[2]/div/div[1]/table/tbody/tr[7]/td[2]').text
            print(fullAddress)
        except:
            pass
        driver.close()
        driver.switch_to.window(driver.window_handles[0])
        summary = fullName + " is one of the swiftBIC banks in Afghanistan."
        if fullName:
            data_dict['fullName'] = fullName
        if branch:
            data_dict['branch'] = branch
        if city:
            data_dict['city'] = city
        if country:
            data_dict['country'] = country
        if fullAddress:
            data_dict['fullAddress'] = fullAddress
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




