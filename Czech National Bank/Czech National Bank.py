#!/usr/bin/env python
# coding: utf-8

# In[6]:


from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import json
import re
from deep_translator import GoogleTranslator


# In[7]:


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
    url = "https://www.cnb.cz/en/about_cnb/bank-board/current-members-of-the-cnb-bank-board"
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized") 
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--log-level=3")
    translator = GoogleTranslator(target='english')
    driver = webdriver.Chrome(options=options)
    driver.get(url)
    list1 = driver.find_elements(By.XPATH, f'/html/body/div[1]/section/div[2]/div/div/main/div[2]/div/div/div/div/ul/li')
    for i in range(1, len(list1)+1):
        data_dict ={}
        placeOfBirthCity = ""
        fullName = driver.find_element(By.XPATH, f'/html/body/div[1]/section/div[2]/div/div/main/div[2]/div/div/div/div/ul/li[{i}]').text
        careerInfoDesignation = fullName.split(":")[0]
        fullName = fullName.split(":")[1].strip()
        print(fullName)
        print(careerInfoDesignation)
        driver.find_element(By.XPATH, f'/html/body/div[1]/section/div[2]/div/div/main/div[2]/div/div/div/div/ul/li[{i}]/a').click()
        time.sleep(2)
        image = driver.find_element(By.XPATH, f'/html/body/div[1]/section/div[2]/div/div/main/div[2]/div/div[1]/div/div/p[1]/img').get_attribute("src")
        print(image)
        info = driver.find_element(By.XPATH, f'/html/body/div[1]/section/div[2]/div/div/main/div[2]/div/div[1]/div/div').text
    #     info = info.split(".")
        if "born in" in info:
            dobInfo = info.split(".", 1)[0]
            placeOfBirthCity = dobInfo.split("born in")[1].split("on")[0].strip()
            dob = dobInfo.split(" on", 1)[1].strip()

        if "born on" in info:
            dobInfo = info.split(".", 1)[0]
            dob = dobInfo.split("born on")[1].strip()
            try:
                placeOfBirthCity = dob.split("in",1)[1].strip()
                dob = dob.split("in", 1)[0]
            except:
                pass

        if "Born on" in info:
            dobInfo = info.split(".", 1)[0]
            dob = dobInfo.split("Born on")[1]
            placeOfBirthCity = dob.split("in", 1)[1].strip()
            dob = dob.split("in", 1)[0].replace("\n", " ").strip()
        print(dob)
        print(placeOfBirthCity)    
        careerInfo = info.split(".",1)[1].strip()
        summary = fullName + " is the " + careerInfoDesignation
        print("*"*50)
        driver.back()
        if fullName:
            data_dict['fullName'] = fullName
        if careerInfoDesignation:
            data_dict['careerInfoDesignation'] = careerInfoDesignation
        if image:
            data_dict['image'] = image
        if dob:
            data_dict['dob'] =dob
        if placeOfBirthCity:
            data_dict['placeOfBirthCity'] = placeOfBirthCity
        if careerInfo:
            data_dict['careerInfo'] = careerInfo
        if summary:
            data_dict['summary'] = summary
        data_list.append(data_dict)
    driver.quit()
    return data_list


# In[9]:


if __name__ == '__main__':
    data_list = get_data("add_slug_name")
    to_json(data_list)

