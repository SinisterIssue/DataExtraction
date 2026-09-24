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


data_list = []
url = "https://www.gov.uk/government/people"
options = webdriver.ChromeOptions()
options.add_argument("--start-maximized") 
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument("--log-level=3")


# In[28]:


def get_data(slug_name):
    driver = webdriver.Chrome(options=options)
    driver.get(url)
    p=1
    while True:
        try:
            list1 = driver.find_elements(By.XPATH, f'//div[2]/div/div[2]/div[4]/div/ul/li/a')
            for i in range(1, len(list1)+1):
                data_dict= {}
                careerInfo =""
                referenceUrls=""
                additionalInfo = ""
                driver.find_element(By.XPATH, f'//div[2]/div/div[2]/div[4]/div/ul/li[{i}]/a').click()
                time.sleep(1)
                fullName = driver.find_element(By.XPATH, f'/html/body/div[3]/main/header/div[1]/div/h1').text
                print(fullName)
                careerInfoDesignation = driver.find_element(By.XPATH, f'/html/body/div[3]/main/header/div[1]/div/span').text
    #             print(careerInfoDesignation)
                try:
                    list2 = driver.find_elements(By.XPATH, f'/html/body/div[3]/main/div/div[2]/div[1]/div/p')
                    for j in range(1, len(list2)+1):
                        careerInfo =careerInfo + ""+ driver.find_element(By.XPATH, f'/html/body/div[3]/main/div/div[2]/div[1]/div/p[{j}]').text
                        careerInfo = careerInfo.replace("\n", "")
    #                 print(careerInfo)

                except:
                    pass
                try:
                    image = driver.find_element(By.XPATH, f'/html/body/div[3]/main/div/div[1]/div[1]/figure/img').get_attribute('src')
    #                 print(image)
                except:
                    pass
                try:
                    additionalInfo = driver.find_element(By.XPATH, f'/html/body/div[3]/main/div/div[2]/div[2]/div/div').text
                    additionalInfo = additionalInfo.replace("\n", "")
    #                 print(additionalInfo)
                except:
                    pass
                try:
                    info = driver.find_element(By.XPATH, f'/html/body/div[3]/main/div/div[2]/div[2]').text
                    careerInfo = careerInfo + " " + info
                except:
                    pass
                try:
                    list3 = driver.find_elements(By.XPATH, f'/html/body/div[3]/main/div/div[2]/div[2]/div/p/a')
                    for k in range(1, len(list3)+1):
                        referenceUrls = driver.find_element(By.XPATH, f'/html/body/div[3]/main/div/div[2]/div[2]/div/p/a').get_attribute('href') + "; "+ referenceUrls
    #                 print(referenceUrls)
                except:
                    pass
                if len(careerInfoDesignation.strip()) !=0:
                    summary = fullName + " is present on the list of all ministers and senior officials on GOV.UK and holds the position of "+ careerInfoDesignation   
                    print(summary)
                if len(careerInfoDesignation.strip())==0:
                    summary = fullName + " is present on the list of all ministers and senior officials on GOV.UK."
                    print(summary)
                print("*"*50)
                driver.back()
                if fullName:
                    data_dict['fullName'] = fullName
                if careerInfoDesignation:
                    data_dict['careerInfoDesignation'] = careerInfoDesignation
                if image:
                    data_dict['image'] = image
                if careerInfo:
                    data_dict['careerInfo'] = careerInfo
                if additionalInfo:
                    data_dict['additionalInfo'] = additionalInfo
                if referenceUrls:
                    data_dict['referenceUrls'] = referenceUrls
                if summary:
                    data_dict['summary'] = summary
                data_list.append(data_dict)
            if p==1:
                driver.find_element(By.XPATH, f'//div[2]/div/div[2]/div[5]/nav/ul/li[1]/a/span[1]/span').click()
                time.sleep(2)
                p+=1
            if p>1:
                driver.find_element(By.XPATH, f'//div[2]/div/div[2]/div[5]/nav/ul/li[2]/a/span[1]/span').click()
                time.sleep(2)
                p+=1
        except Exception as e:
            print(e)
            break
    return data_list


# In[29]:


if __name__ == '__main__':
    data_list = get_data("add_slug_name")
    to_json(data_list)


# In[ ]:




