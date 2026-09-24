#!/usr/bin/env python
# coding: utf-8

# In[16]:


from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import json
import re
from deep_translator import GoogleTranslator


# In[17]:


def to_json(data):
    """
    This function takes list of dictionary as Input and 
    then Creates a JSON file in which Input data is stored
    """
    with open("data_dict.json", "w") as outfile:
        json.dump(data, outfile,indent=4)
        outfile.close()


# In[18]:


def get_data(slug_name):
    data_list = []
    url = "http://government.ru/en/gov/persons//"
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized") 
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--log-level=3")
    translator = GoogleTranslator(target='english')
    driver = webdriver.Chrome(options=options)
    driver.get(url)
    list1 = driver.find_elements(By.XPATH, f'/html/body/div[7]/div[2]/div[2]/div/div[6]/ul/li[2]/ul/li/a/div/p[2]')
    for i in range(1, len(list1)+1):
        data_dict = {}
        educationInfo = ""
        careerInfo = ""
        maritalStatus = ""
        familyInfo = ""
        dob =""
        placeOfBirthCity = ""
        fullName = driver.find_element(By.XPATH, f'/html/body/div[7]/div[2]/div[2]/div/div[6]/ul/li[2]/ul/li[{i}]/a/div/p[2]').text
        print(fullName)
        careerInfoDesignation = driver.find_element(By.XPATH, f'/html/body/div[7]/div[2]/div[2]/div/div[6]/ul/li[2]/ul/li[{i}]/a/div/p[1]').text
        print(careerInfoDesignation)
        image = driver.find_element(By.XPATH, f'/html/body/div[7]/div[2]/div[2]/div/div[6]/ul/li[2]/ul/li[{i}]/a/figure/picture/img').get_attribute("src")
        print(image)
        driver.find_element(By.XPATH, f'/html/body/div[7]/div[2]/div[2]/div/div[6]/ul/li[2]/ul/li[{i}]/a/div/p[2]').click()
        time.sleep(2)
        importantDates = driver.find_element(By.XPATH, f'/html/body/div[7]/div[2]/div[2]/div[1]/article/div/div[2]/div/p').text
        print(importantDates)
        try:
            info = driver.find_element(By.XPATH, f'/html/body/div[7]/div[2]/div[2]/div[2]/div/div[2]/div/div').text
            dobInfo = info.split("Education",1)[0]
            if "in" in dobInfo:
                placeOfBirthCity = dobInfo.split("in",1)[1].split(".",1)[0].strip()
                dob = dobInfo.split("Born",1)[1].split("in",1)[0].strip()
            else:
                dob = dobInfo.split("Born", 1)[1].split(".",  1)[0].strip()
            print(dob)
            print(placeOfBirthCity)
            try:
                educationInfo = info.split("Education",1)[1].split("Experience", 1)[0].replace("\n", ";").replace(";", "", 1).strip()
                print(educationInfo)
                careerInfo = info.split("Experience", 1)[1].replace("\n", ";").replace(";", "", 1).strip()
                print(careerInfo)
            except:
                try:
                    list2 = driver.find_elements(By.XPATH, f'/html/body/div[7]/div[2]/div[2]/div[2]/div/div[2]/div/div/p')
                    for j in range(1, len(list2)+1):
                        newInfo = driver.find_element(By.XPATH, f'/html/body/div[7]/div[2]/div[2]/div[2]/div/div[2]/div/div/p[{j}]').text
                        if "Graduated" in newInfo or "Completed" in newInfo or "graduated" in newInfo or "student" in newInfo:
                            educationInfo = newInfo.replace("\n", "") + "; " + educationInfo
                        elif "Married" in newInfo:
                            maritalStatus = newInfo.split(",")[0].strip()
                            familyInfo = newInfo
                        else:
                            careerInfo = newInfo + "; " + careerInfo
                    careerInfo = careerInfo.split("; Born")[0].replace("; ", "", 1).strip()
                    print(educationInfo)
                    print(careerInfo)
                    print(maritalStatus)
                    print(familyInfo)
                except:
                    pass
        except:
            pass
        summary = fullName + " is the " + careerInfoDesignation + " of The Russian Government"
        driver.back()
        print("*"*50)
        if fullName:
            data_dict['fullName'] = fullName
        if image:
            data_dict['image'] = image
        if careerInfoDesignation:
            data_dict['careerInfoDesignation'] = careerInfoDesignation
        if importantDates:
            data_dict['importantDates'] = importantDates
        if dob:
            data_dict['dob'] = dob
        if placeOfBirthCity:
            data_dict['placeOfBirthCity'] = placeOfBirthCity
        if educationInfo:
            data_dict['educationInfo'] = educationInfo
        if familyInfo:
            data_dict['familyInfo'] = familyInfo
        if maritalStatus:
            data_dict['maritalStatus'] = maritalStatus
        if careerInfo:
            data_dict['careerInfo'] = careerInfo
        if summary:
            data_dict['summary'] = summary
        data_list.append(data_dict)
    driver.quit()
    return data_list


# In[19]:


if __name__ == '__main__':
    data_list = get_data("add_slug_name")
    to_json(data_list)


# In[ ]:




