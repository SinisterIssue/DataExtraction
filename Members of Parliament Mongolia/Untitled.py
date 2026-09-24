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


# In[22]:


def get_data(slug_name):
    data_list = []
    url = "http://www.parliament.mn/en/cv"
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized") 
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--log-level=3")
    translator = GoogleTranslator(target='english')
    driver = webdriver.Chrome(options=options)
    driver.get(url)
    list1 = driver.find_elements(By.XPATH, f'/html/body/div[5]/div[3]/div/div/div[2]/div')
    # print(len(list1))
    for i in range(2, len(list1)+1):
        list2 = driver.find_elements(By.XPATH, f'/html/body/div[5]/div[3]/div/div/div[2]/div[{i}]/div')
        for j in range(1, len(list2)+1):
            data_dict = {}
            languagesKnown = ""
            emails = ""
            driver.find_element(By.XPATH, f'/html/body/div[5]/div[3]/div/div/div[2]/div[{i}]/div[{j}]/a/div/div/div[1]/img').click()
            time.sleep(2)
            image = driver.find_element(By.XPATH, f'/html/body/div[5]/div[3]/div[2]/div/div[1]/div/div[1]/div/center/img').get_attribute("src")
            print(image)
            fullName = driver.find_element(By.XPATH, f'/html/body/div[5]/div[3]/div[2]/div/div[1]/div/div[2]/div[1]').text.title()
            print(fullName)
            careerInfoDesignation = driver.find_element(By.XPATH, f'/html/body/div[5]/div[3]/div[2]/div/div[1]/div/div[2]/div[2]').text
            print(careerInfoDesignation)
            info = driver.find_element(By.XPATH, f'/html/body/div[5]/div[3]/div[2]/div/div[1]/div/div[2]').text
            educationInfo = info.split("EDUCATIONAL BACKGROUND")[1].split("WORKING EXPERIENCE")[0].replace("\n", " ").strip()
            print(educationInfo)
            try:
                careerInfo = info.split("WORKING EXPERIENCE")[1].split("FOREIGN LANGUAGE KNOWLEDGE")[0].replace("\n", " ").strip()
                print(careerInfo)
            except:
                pass
            try:
                careerInfo = info.split("WORKING EXPERIENCE")[1].split("AWARDS")[0].replace("\n", " ").strip()
                print(careerInfo)
                achievements = info.split("AWARDS")[1].split("FOREIGN LANGUAGE KNOWLEDGE")[0].replace("\n", " ").replace('”', '”;').strip()
                print(achievements)
            except:
                pass
            try:
                languagesKnown = info.split("FOREIGN LANGUAGE KNOWLEDGE")[1].split("E-MAIL")[0].replace("\n", " ").strip()
                print(languagesKnown)
            except:
                pass
            try:
                emails = info.split("E-MAIL")[1].replace("\n", " ").strip()
            except:
                pass
            summary = fullName + " is the " + careerInfoDesignation
            driver.back()
            if fullName:
                data_dict['fullName'] = fullName
            if image:
                data_dict['image'] = image
            if careerInfoDesignation:
                data_dict['careerInfoDesignation'] = careerInfoDesignation
            if educationInfo:
                data_dict['educationInfo'] = educationInfo
            if careerInfo:
                data_dict['careerInfo'] = careerInfo
            if achievements:
                data_dict['achievements'] = achievements
            if languagesKnown:
                data_dict['languagesKnown'] = languagesKnown
            if emails:
                data_dict['emails'] = emails
            if summary:
                data_dict['summary'] = summary
            data_list.append(data_dict)
            print("*"*50)
    driver.quit()
    return data_list


# In[23]:


if __name__ == '__main__':
    data_list = get_data("add_slug_name")
    to_json(data_list)


# In[ ]:




