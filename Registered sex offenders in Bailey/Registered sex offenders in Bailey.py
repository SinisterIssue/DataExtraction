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


# In[23]:


def get_data(slug_name):
    data_list = []
    url = "https://www.city-data.com/so/so-Bailey-Texas.html"
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized") 
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--log-level=3")
    translator = GoogleTranslator(target='english')
    driver = webdriver.Chrome(options=options)
    driver.get(url)
    list1 = driver.find_elements(By.XPATH, f'/html/body/div[3]/div[4]/div/div/a[2]')
    for i in range(4, len(list1)+4):
        link = driver.find_element(By.XPATH, f'/html/body/div[3]/div[4]/div[{i}]/div/a[2]').get_attribute("href")
        driver.execute_script("window.open('');")
        driver.switch_to.window(driver.window_handles[1])
        driver.get(link)
        time.sleep(2)
        image = driver.find_element(By.XPATH, f'/html/body/div[2]/div[2]/main/div[4]/div/div[2]/img').get_attribute('src')
        print(image)
        data_dict = {}
        crimeInfo = ""
        offense = ""
        additionalInfo = ""
        list2 = driver.find_elements(By.XPATH, f'/html/body/div[2]/div[2]/main/div[4]/div/div[3]/table/tbody/tr')
        fullName = driver.find_element(By.XPATH, f'/html/body/div[2]/div[2]/main/div[4]/div/h1').text
        firstName = fullName.split(",")[1].strip()
        lastName = fullName.split(",")[0].strip()
        fullName = firstName + " " + lastName
        print(fullName)
        for j in range(1, len(list2)+1):
            heading = driver.find_element(By.XPATH, f'/html/body/div[2]/div[2]/main/div[4]/div/div[3]/table/tbody/tr[{j}]').text
            if "SID" in heading:
                sid = heading.split("SID")[1].strip()
                identifierType = "SID: " + sid
    #             print(identifierType)
            if "Risk Level" in heading:
                riskLevel = heading.split("Risk Level")[1].strip()
    #             print(riskLevel)
            if "Sex" in heading:
                gender = heading.split("Sex")[1].strip()
    #             print(gender)
            if "Race" in heading:
                race = heading.split("Race")[1].strip()
    #             print(race)
            if "Height" in heading:
                height = heading.split("Height")[1].strip()
    #             print(height)
            if "Weight" in heading:
                weight = heading.split("Weight")[1].strip()
    #             print(weight)
            if "Hair Color" in heading:
                hair = heading.split("Hair Color")[1].strip()
    #             print(hair)
            if "Eye Color" in heading:
                eyes = heading.split("Eye Color")[1].strip()
    #             print(eyes)
            if "Shoe Size" in heading:
                shoeSize = heading.split("Shoe Size")[1].strip() 
                additionalInfo = additionalInfo + "Shoe Size: " + shoeSize
            if "Shoe Width" in heading:
                shoeWidth = heading.split("Shoe Width")[1].strip()
                additionalInfo = additionalInfo + "; Shoe Width: "+  shoeWidth
        alias = driver.find_element(By.XPATH, f'/html/body/div[2]/div[2]/main/div[4]/div/ul[1]').text
        alias = alias.replace("\n", "; ")
        listOfDob = driver.find_element(By.XPATH, f'/html/body/div[2]/div[2]/main/div[4]/div/ul[2]').text.replace("\n", "; ")
        dob = listOfDob.split("(")[0].strip()
        fullAddress = driver.find_element(By.XPATH, f'/html/body/div[2]/div[2]/main/div[4]/div/div[5]/table/tbody/tr/td').text.replace("\n", ", ")
    #     print(alias)
    #     print(listOfDob)
        list3 = driver.find_elements(By.XPATH, f'/html/body/div[2]/div[2]/main/div[4]/div/h2')
        for k in range(1, len(list3)+1):
            head = driver.find_element(By.XPATH, f'/html/body/div[2]/div[2]/main/div[4]/div/h2[{k}]').text
            if "Offense" in head:
                if head.split("Offense:")[1].strip() not in offense:
                    offense = head.split("Offense:")[1].strip() + "; " + offense
        print(offense)
        list4 = driver.find_elements(By.XPATH, f'/html/body/div[2]/div[2]/main/div[4]/div/div/table')
        print(len(list4))
        for l in range(7, 2*len(list4)):
            try:
                crime = driver.find_element(By.XPATH, f'/html/body/div[2]/div[2]/main/div[4]/div/div[{l}]/table').text.replace("\n", ", ")
    #             print(crime)
                crimeInfo = crime + "; " + crimeInfo
            except:
                pass
        print(crimeInfo)
        summary = "According to our research of Texas and other state lists, there were 4 registered sex offenders living in Bailey as of August 10, 2022. The ratio of all residents to sex offenders in Bailey is 52 to 1. " + fullName + " is one of them"
        driver.close()
        driver.switch_to.window(driver.window_handles[0])
        print("*"*50)
        if fullName:
            data_dict['fullName'] = fullName
        if alias:
            data_dict['alias'] = alias
        if image:
            data_dict['image'] = image
        if offense:
            data_dict['offence'] = offense
        if dob:
            data_dict['dob'] = dob
        if listOfDob:
            data_dict['listOfDob'] = listOfDob
        if riskLevel:
            data_dict['riskLevel'] = riskLevel
        if gender:
            data_dict['gender'] = gender
        if race:
            data_dict['race'] = race
        if height:
            data_dict['height'] = height
        if weight:
            data_dict['weight'] = weight
        if hair:
            data_dict['hair'] = hair
        if eyes:
            data_dict['eyes'] = eyes
        if fullAddress:
            data_dict['fullAddress'] = fullAddress
        if identifierType:
            data_dict['identifierType'] = identifierType
        if crimeInfo:
            data_dict['crimeInfo'] = crimeInfo
        if additionalInfo:
            data_dict['additionalInfo'] = additionalInfo
        if summary:
            data_dict['summary'] = summary
        data_list.append(data_dict)
    driver.quit()
    return data_list


# In[24]:


if __name__ == '__main__':
    data_list = get_data("add_slug_name")
    to_json(data_list)


# In[ ]:




