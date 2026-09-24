#!/usr/bin/env python
# coding: utf-8

# In[11]:


from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import json
import re
from deep_translator import GoogleTranslator


# In[12]:


def to_json(data):
    """
    This function takes list of dictionary as Input and 
    then Creates a JSON file in which Input data is stored
    """
    with open("data_dict.json", "w") as outfile:
        json.dump(data, outfile,indent=4)
        outfile.close()


# In[13]:


def get_data(slug_name):    
    data_list = []
    url = "https://parliament.gov.gy/about-parliament/parliamentarian/"
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized") 
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--log-level=3")
    translator = GoogleTranslator(target='english')
    driver = webdriver.Chrome(options=options)
    driver.get(url)

    list1 = driver.find_elements(By.XPATH, f'/html/body/section/div[2]/div/div/div/div[2]/div/div/div[2]/ul/li/span[1]/a')
    for i in range(1, len(list1)+1):
        data_dict = {}
        politicalParty =""
        importantDates =""
        additionalInfo = ""
        careerInfo = ""

        link = driver.find_element(By.XPATH, f'/html/body/section/div[2]/div/div/div/div[2]/div/div/div[2]/ul/li[{i}]/span[1]/a').get_attribute("href")
        driver.execute_script("window.open('');")
        driver.switch_to.window(driver.window_handles[1])
        driver.get(link)
        time.sleep(1)
        fullName = driver.find_element(By.XPATH, f'/html/body/section/div[1]/div[2]/div/div/div/div[2]/ul[1]/li[1]/span').text
        print(fullName)
        careerInfoDesignation = driver.find_element(By.XPATH, f'/html/body/section/div[1]/div[2]/div/div/div/div[2]/ul[1]/li[2]/span').text
        print(careerInfoDesignation)
        if careerInfoDesignation == "":
            careerInfoDesignation = "Member of Parliament"
        politicalParty = driver.find_element(By.XPATH, f'/html/body/section/div[1]/div[2]/div/div/div/div[2]/ul[1]/li[3]/span').text
    #     if politicalParty.split(":")[1] =="":
    #         politicalParty = ""
        print(politicalParty)
        importantDates = driver.find_element(By.XPATH, f'/html/body/section/div[1]/div[2]/div/div/div/div[2]/ul[1]/li[4]').text
        if importantDates.split(":")[1] =="":
            importantDates = ""
        print(importantDates)
        additionalInfo = driver.find_element(By.XPATH, f'/html/body/section/div[1]/div[2]/div/div/div/div[2]/ul[1]/li[6]').text
        if additionalInfo.split(":")[1] =="":
            additionalInfo = ""
        additionalInfo = additionalInfo.replace(" |", ";")
        print(additionalInfo)
        try:
            careerInfo = driver.find_element(By.XPATH, f'/html/body/section/div[2]/div/div/div/p[2]').text
            print(careerInfo)
        
        except:
            pass
        image = driver.find_element(By.XPATH, f'/html/body/section/div[1]/div[2]/div/div/div/div[1]/img').get_attribute("src")
        if careerInfo != "":
            summary = careerInfo
        else:
            summary = fullName + " is the " + careerInfoDesignation+  " of Republic of Guyana."
        print("*"*50)
        driver.close()
        driver.switch_to.window(driver.window_handles[0])
        if fullName:
            data_dict['fullName'] = fullName
        if careerInfoDesignation:
            data_dict['careerInfoDesignation'] = careerInfoDesignation
        if image:
            data_dict['image'] = image
        if politicalParty:
            data_dict['politicalParty'] = politicalParty
        if importantDates:
            data_dict['importantDates'] = importantDates
        if additionalInfo:
            data_dict['additionalInfo'] = additionalInfo
        if careerInfo:
            data_dict['careerInfo'] = careerInfo
        if summary:
            data_dict['summary'] = summary
        data_list.append(data_dict)
    driver.quit()
    return data_list


# In[14]:


if __name__ == '__main__':
    data_list = get_data("add_slug_name")
    to_json(data_list)


# In[ ]:




