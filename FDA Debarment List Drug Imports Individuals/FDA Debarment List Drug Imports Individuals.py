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


# In[14]:


def get_data(slug_name):
    data_list = []
    url = "https://www.fda.gov/inspections-compliance-enforcement-and-criminal-investigations/fda-debarment-list-drug-product-applications/fda-debarment-list-drug-imports/"
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized") 
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--log-level=3")
    translator = GoogleTranslator(target='english')
    driver = webdriver.Chrome(options=options)
    driver.get(url)
    list1 = driver.find_elements(By.XPATH, f'/html/body/div[2]/div[1]/div/main/article/div/div/div[2]/table/tbody/tr')
    lastUpdated = driver.find_element(By.XPATH, f'/html/body/div[2]/div[1]/div/main/article/aside[1]/section/div/aside/ul/div/li/div/p').text
    d = lastUpdated.split("/")[1]
    m = lastUpdated.split("/")[0]
    y = lastUpdated.split("/")[2]
    lastUpdated = d + "/" + m + "/" + y
    for i in range(1, len(list1)+1):
        list2 = driver.find_elements(By.XPATH, f'/html/body/div[2]/div[1]/div/main/article/div/div/div[2]/table/tbody/tr[{i}]/td')
        data_dict ={}
        for j in range(1, len(list2)+1):
            if j==1:
                lastName = driver.find_element(By.XPATH, f'/html/body/div[2]/div[1]/div/main/article/div/div/div[2]/table/tbody/tr[{i}]/td[{j}]').text
                print(lastName)
            if j==2:
                firstName = driver.find_element(By.XPATH, f'/html/body/div[2]/div[1]/div/main/article/div/div/div[2]/table/tbody/tr[{i}]/td[{j}]').text
                print(firstName)
            if j==3:
                effectiveDate = driver.find_element(By.XPATH, f'/html/body/div[2]/div[1]/div/main/article/div/div/div[2]/table/tbody/tr[{i}]/td[{j}]').text
                d = effectiveDate.split("/")[1]
                m = effectiveDate.split("/")[0]
                y = effectiveDate.split("/")[2]
                effectiveDate = d + "/" + m + "/" + y
            if j==4:
                endTerm = driver.find_element(By.XPATH, f'/html/body/div[2]/div[1]/div/main/article/div/div/div[2]/table/tbody/tr[{i}]/td[{j}]').text
            if j==5:
                FrDate = driver.find_element(By.XPATH, f'/html/body/div[2]/div[1]/div/main/article/div/div/div[2]/table/tbody/tr[{i}]/td[{j}]').text
                d = FrDate.split("/")[1]
                m = FrDate.split("/")[0]
                y = FrDate.split("/")[2]
                FrDate = d + "/" + m + "/" + y
            if j==6:
                page = driver.find_element(By.XPATH, f'/html/body/div[2]/div[1]/div/main/article/div/div/div[2]/table/tbody/tr[{i}]/td[{j}]').text
                try:
                    referenceUrls = driver.find_element(By.XPATH, f'/html/body/div[2]/div[1]/div/main/article/div/div/div[2]/table/tbody/tr[{i}]/td[{j}]/p/a').get_attribute('href')
                except:
                    referenceUrls = driver.find_element(By.XPATH, f'/html/body/div[2]/div[1]/div/main/article/div/div/div[2]/table/tbody/tr[{i}]/td[{j}]/a').get_attribute('href')
        importantDates = "Effective Date: " + effectiveDate + "; FR Date: "+  FrDate
        additionalInfo = "End/Term of Debarment: " + endTerm + "; Volume Page: "+  page
        fullName = firstName + " " + lastName  
        summary = fullName + " is one of the persons currently debarred pursuant to sections 306(b)(3)(C) or (D) of the Federal Food, Drug, and Cosmetic Act (21 U.S.C. 335(b)(3)(C) or (D)) as published in the FEDERAL REGISTER"
        print("*"*50)
        if fullName:
            data_dict['fullName'] = fullName
        if importantDates:
            data_dict['importantDates'] = importantDates
        if additionalInfo:
            data_dict['additionalInfo'] = additionalInfo
        if lastUpdated:
            data_dict['lastUpdated'] = lastUpdated
        if referenceUrls:
            data_dict['referenceUrls'] = referenceUrls
        if summary:
            data_dict['summary'] = summary
        data_list.append(data_dict)
    driver.quit()
    return data_list


# In[15]:


if __name__ == '__main__':
    data_list = get_data("add_slug_name")
    to_json(data_list)


# In[ ]:




