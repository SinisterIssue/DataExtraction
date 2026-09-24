#!/usr/bin/env python
# coding: utf-8

# In[10]:


from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import json
import re


# In[11]:


def to_json(data):
    """
    This function takes list of dictionary as Input and 
    then Creates a JSON file in which Input data is stored
    """
    with open("data_dict.json", "w") as outfile:
        json.dump(data, outfile,indent=4)
        outfile.close()


# In[12]:


data_list = []
url = "http://english.ah.gov.cn/content/column/6787051?liId=721"
options = webdriver.ChromeOptions()
options.add_argument("--start-maximized") 
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument("--log-level=3")


# In[15]:


def get_data(slug_name):
    driver = webdriver.Chrome(options=options)
    driver.get(url)
    driver.find_element(By.XPATH, f'/html/body/div/div[3]/div[1]/a[2]').click()
    list1 = driver.find_elements(By.XPATH, f'/html/body/div/div[3]/div[2]/div/div/ul[1]/li/a/div')
    for i in range(2, len(list1)+2):
        placeOfBirthCity = ""
        data_dict = {}
        fullName = driver.find_element(By.XPATH, f'/html/body/div/div[3]/div[2]/div/div/ul[1]/li[{i}]/a/div').text
        print(fullName)
        firstName = fullName.split(" ")[0]
        lastName = fullName.split(" ")[1]
        link = driver.find_element(By.XPATH, f'/html/body/div/div[3]/div[2]/div/div/ul[1]/li[{i}]/a').get_attribute("href")        
        driver.execute_script("window.open('');")
        driver.switch_to.window(driver.window_handles[1])
        driver.get(link)
        careerInfoDesignation = driver.find_element(By.XPATH, f'/html/body/div/div[3]/div[2]/div/div/div[1]/div/div[2]/span[1]').text
        print(careerInfoDesignation)
        image = driver.find_element(By.XPATH, f'/html/body/div/div[3]/div[2]/div/div/div[1]/div/div[1]/img').get_attribute("src")
        print(image)
        description = driver.find_element(By.XPATH, f'/html/body/div/div[3]/div[2]/div/div/div[2]/div[1]/div[1]').text.replace("\n", " ")
        description = fullName + " is " + description
        info = driver.find_element(By.XPATH, f'/html/body/div/div[3]/div[2]/div/div/div[2]/div[1]/div[2]').text
        info2 = info.split("\n", 1)[0]
        dobInfo = info2.split(".", 1)[0]
        dobInfo = dobInfo.split(",")
        sex = dobInfo[1].strip()
        race = dobInfo[2].strip()
        dob = dobInfo[3].replace(" was born in", "").strip()
        try:
            placeOfBirthCity = dob.split("and is from")[1].strip()
            dob = dob.split("and is from")[0].strip()
        except:
            pass
        educationInfo = info2.split(".", 1)[1].replace("He", fullName, 1)
        careerInfo = info.split("\n", 1)[1].replace("\n", " ")
        summary = fullName + " is the " + careerInfoDesignation + " of the government body in Anhui, China."
        print(race)
        print(sex)
        print(dob)
        print(placeOfBirthCity)
        print("*"*50)

        driver.close()
        driver.switch_to.window(driver.window_handles[0])
        if fullName:
            data_dict['fullName'] = fullName
            if firstName:
                data_dict['firstName'] = firstName
            if lastName:
                data_dict['lastName'] = lastName
            if image:
                data_dict['image'] = image
            if careerInfoDesignation:
                data_dict['careerInfoDesignation'] = careerInfoDesignation
            if description:
                data_dict['description'] = description
            if dob:
                data_dict['dob'] = dob
            if placeOfBirthCity:
                data_dict['placeOfBirthCity'] = placeOfBirthCity
            if race:
                data_dict['race'] = race
            if sex:
                data_dict['sex'] = sex
            if educationInfo:
                data_dict['educationInfo'] = educationInfo
            if careerInfo:
                data_dict['careerInfo'] = careerInfo
            if summary:
                data_dict['summary'] = summary
            data_list.append(data_dict)
    return data_list


# In[16]:


if __name__ == '__main__':
    data_list = get_data("add_slug_name")
    to_json(data_list)


# In[ ]:




