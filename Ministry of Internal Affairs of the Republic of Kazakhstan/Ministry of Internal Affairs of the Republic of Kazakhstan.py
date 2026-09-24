#!/usr/bin/env python
# coding: utf-8

# In[88]:


from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import json
import re
from deep_translator import GoogleTranslator


# In[89]:


def to_json(data):
    """
    This function takes list of dictionary as Input and 
    then Creates a JSON file in which Input data is stored
    """
    with open("data_dict.json", "w") as outfile:
        json.dump(data, outfile,indent=4)
        outfile.close()


# In[90]:


data_list = []
url = "https://www.gov.kz/memleket/entities/qriim/about/structure?lang=kk"
options = webdriver.ChromeOptions()
options.add_argument("--start-maximized") 
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument("--log-level=3")
translator = GoogleTranslator(target='english')


# In[91]:


def get_data(slug_name):
    driver = webdriver.Chrome(options=options)
    driver.get(url)
    # time.sleep(5)
    # driver.find_element(By.XPATH, f'/html/body/div/header/div[1]/div/div/div[2]/div/div[2]/button/div').click()
    # time.sleep(2)
    # driver.find_element(By.XPATH, f'/html/body/div/header/div[1]/div/div/div[2]/div/div[2]/div/div/li[3]').click()
    time.sleep(10)
    list1 = driver.find_elements(By.XPATH, f'/html/body/div/main/div/section/div[2]/div/div[2]/div/div/div/div/div[3]/div/a')
    for i in range(1, len(list1)+1):
        data_dict = {}
        placeOfBirthCity = ""
        additionalInfo = ""
        dob=""
        educationInfo = ""
        careerInfo = ""
        maritalStatus = ""
        familyInfo = ""

        fullName = driver.find_element(By.XPATH, f'//div[2]/div/div[2]/div/div/div[{i}]/div/div[3]/div/a').text
        fullName = translator.translate(fullName)
        print(fullName)
        careerInfoDesignation = driver.find_element(By.XPATH, f'//div[2]/div/div[2]/div/div/div[{i}]/div/div[3]/div/p').text
        careerInfoDesignation = translator.translate(careerInfoDesignation)
        print(careerInfoDesignation)
        image = driver.find_element(By.XPATH, f'//div[2]/div/div[2]/div/div/div[{i}]/div/div[1]/div[1]/img').get_attribute('src')
        print(image)
        additionalInfo = driver.find_element(By.XPATH, f'/html/body/div[1]/main/div/section/div[2]/div/div[2]/div/div/div[{i}]/div/div[3]/div/div[2]/div').text
        if "Телефон:" in additionalInfo:
            additionalInfo = ""
        else:
            additionalInfo = translator.translate(additionalInfo)
            additionalInfo = "Areas of Work: " + additionalInfo
        print(additionalInfo)
        link = driver.find_element(By.XPATH, f'//div[2]/div/div[2]/div/div/div[{i}]/div/div[3]/div/a').get_attribute("href")
        driver.execute_script("window.open('');")
        driver.switch_to.window(driver.window_handles[1])
        driver.get(link)
        time.sleep(5)
        telephoneNos = driver.find_element(By.XPATH, f'/html/body/div/main/div/section[2]/div/div/div/div[1]/div/div[3]/button/p').text
        print(telephoneNos)
        try:
            list2 = driver.find_elements(By.XPATH, f'/html/body/div/main/div/section[2]/div/div/div/div[2]/section[1]/div[2]/div/p')
            for j in range(1, len(list2)+1):
                info = driver.find_element(By.XPATH, f'/html/body/div/main/div/section[2]/div/div/div/div[2]/section[1]/div[2]/div/p[{j}]').text
                info = translator.translate(info)
                print(info)
                if "born on" in info:
                    dob = info.split("born on")[1].strip()
                    educationInfo = dob.split(".")[1].strip()
                    dob = dob.split(".")[0].strip()
                elif "Married" in info:
                    maritalStatus = info.split(",")[0].split(":")[1].strip()
                    familyInfo = info.split(",")[1].strip()
                else:
                    additionalInfo = "Awards: " + info + "; " + additionalInfo
            careerInfo = driver.find_element(By.XPATH, f'/html/body/div/main/div/section[2]/div/div/div/div[2]/section[2]/div[2]/div').text
            careerInfo = translator.translate(careerInfo)
            careerInfo = careerInfo.replace("\n", "; ")
        except:
            pass
        try:
            print("here")
            list2 = driver.find_elements(By.XPATH, f'/html/body/div/main/div/section[2]/div/div/div/div[2]/section[2]/div[2]/div/p')
            for k in range(1, len(list2)+1):
                info = driver.find_element(By.XPATH, f'/html/body/div/main/div/section[2]/div/div/div/div[2]/section[2]/div[2]/div/p[{k}]').text
                info = translator.translate(info)
                print(info)
                if "born in" in info:
                    dob = info.split("born in")[1]
                    if "in the" in dob:
                        placeOfBirthCity = dob.split("in the")[1].strip()
                        dob = dob.split("in the")[0]
                    else:
                        placeOfBirthCity = dob.split("in", 1)[1].strip()
                        dob = dob.split("in", 1)[0]
                elif "born on" in info:
                    dob = info.split("born on", 1)[1]
                    placeOfBirthCity = dob.split("in", 1)[1].strip()
                    try:
                        educationInfo = placeOfBirthCity.split("\n", 1)[1].strip()
                        placeOfBirthCity = placeOfBirthCity.split("\n", 1)[0].strip()
                    except:
                        pass
                    dob = dob.split("in")[0]
                elif "married" in info:
                    maritalStatus = info.split(",")[0].split(":")[1].strip()
                    familyInfo = info.split(",")[1].strip()
                elif "graduated" in info:
                    educationInfo = info
                elif "awarded" in info:
                    additionalInfo = "Awards: " + info + "; " + additionalInfo
        except:
            pass
        try:
            careerInfo = driver.find_element(By.XPATH, f'/html/body/div/main/div/section[2]/div/div/div/div[2]/section[3]/div[2]/div').text
            careerInfo = careerInfo.replace("\n", "")
            careerInfo = translator.translate(careerInfo)
        except:
            pass

        driver.close()
        driver.switch_to.window(driver.window_handles[0])
        summary = fullName + " is one of the Ministry of Internal Affairs of the Republic of Kazakhstan."
        time.sleep(5)
        print("*"*50)
        if fullName:
            data_dict['fullName'] = fullName
        if image:
            data_dict['image'] = image
        if careerInfoDesignation:
            data_dict['careerInfoDesignation'] = careerInfoDesignation
        if telephoneNos:
            data_dict['telephoneNos'] = telephoneNos
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
        if additionalInfo:
            data_dict['additionalInfo'] = additionalInfo
        if summary:
            data_dict['summary'] = summary
        data_list.append(data_dict)
    driver.quit()
    return data_list


# In[92]:


if __name__ == '__main__':
    data_list = get_data("add_slug_name")
    to_json(data_list)


# In[ ]:




