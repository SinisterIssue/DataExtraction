#!/usr/bin/env python
# coding: utf-8

# In[26]:


from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import json
import re
from deep_translator import GoogleTranslator


# In[27]:


def to_json(data):
    """
    This function takes list of dictionary as Input and 
    then Creates a JSON file in which Input data is stored
    """
    with open("data_dict.json", "w") as outfile:
        json.dump(data, outfile,indent=4)
        outfile.close()


# In[36]:


def get_data(slug_name):
    data_list = []
    url = "https://klag-pr-app-jailroster.azurewebsites.us/?_Tx0050000"
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized") 
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--log-level=3")
    translator = GoogleTranslator(target='english')
    driver = webdriver.Chrome(options=options)
    driver.get(url)
    driver.find_element(By.XPATH, f'/html/body/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div/button[2]').click()
    time.sleep(2)
    list1 = driver.find_elements(By.XPATH, f'/html/body/div/div/div/div[2]/div[3]/div/div/div/div')
    for i in range(1, len(list1)+1):
        data_dict = {}
        charges = ""
        fullName = driver.find_element(By.XPATH, f'/html/body/div/div/div/div[2]/div[3]/div[{i}]/div/div/div/div[2]/div[1]').text
        arrestDate = fullName.split("\n")[1].split("Arrested:")[1].strip()
        d = arrestDate.split("/")[1]
        m = arrestDate.split("/")[0]
        y = arrestDate.split("/")[2]
        arrestDate = d + "/" + m + "/" + y
        fullName = fullName.split("\n")[0]
        firstName = fullName.split(",")[1].strip()
        lastName = fullName.split(",")[0].strip()
        fullName = firstName + " " + lastName
        fullName = fullName.title()
        print(fullName)
        importantDates ="Arresting Date: "+ arrestDate
        image = driver.find_element(By.XPATH, f'/html/body/div/div/div/div[2]/div[3]/div[{i}]/div/div/div/div[1]/div/a/img').get_attribute("src")
    #     print(image)
        dob = driver.find_element(By.XPATH, f'/html/body/div/div/div/div[2]/div[3]/div[{i}]/div/div/div/div[2]/div[2]').text
        additionalInfo = dob.split("\n")[0]

        race = dob.split("\n")[1].split(":")[1].strip()
        gender = race.split("/")[1]
        race = race.split("/")[0]

        dobYear = dob.split("\n")[2]
        age = dobYear.split("Age:")[1].replace(")", "").strip()
        dobYear = dobYear.split("DOB:")[1].split("(")[0].strip()

        height = dob.split("\n")[3]
        height = height.split(":")[1].strip()
        weight = height.split("/")[1].strip()
        height = height.split("/")[0].strip()
        if gender == "M":
            gender = "Male"
        if gender == "F":
            gender = "Female"
        if race =="B":
            race = "Black"
        if race =="W":
            race = "White"
#         print(dobYear)
#         print(age)
#         print(gender)
#         print(race)
        print(height)
#         print(weight)
        info = driver.find_element(By.XPATH, f'/html/body/div/div/div/div[2]/div[3]/div[{i}]/div/div/div/div[2]/div[3]').text
        eyes = info.split("\n")[0]
        hair = eyes.split("/")[1]
        hair = hair.split(":")[1].strip()
        eyes = eyes.split(":")[1].split("/")[0].strip()
        agency = info.split("\n")[1]
        additionalInfo = additionalInfo + "; " + agency

        list2 = driver.find_elements(By.XPATH, f'/html/body/div/div/div/div[2]/div[3]/div[{i}]/div/div/div/div[2]/div[4]/table/tr')
        for j in range(1, len(list2)+1):

            warrant = ""
            bond = ""
            list3 = driver.find_elements(By.XPATH, f'/html/body/div/div/div/div[2]/div[3]/div[{i}]/div/div/div/div[2]/div[4]/table/tr[{j}]/td')
            for k in range(1, len(list3)+1):
                if k==1:
                    charge = driver.find_element(By.XPATH, f'/html/body/div/div/div/div[2]/div[3]/div[{i}]/div/div/div/div[2]/div[4]/table/tr[{j}]/td[{k}]').text
                if k==2:
                    warrant = driver.find_element(By.XPATH, f'/html/body/div/div/div/div[2]/div[3]/div[{i}]/div/div/div/div[2]/div[4]/table/tr[{j}]/td[{k}]').text
                if k==3:
                    bond = driver.find_element(By.XPATH, f'/html/body/div/div/div/div[2]/div[3]/div[{i}]/div/div/div/div[2]/div[4]/table/tr[{j}]/td[{k}]').text
    #                 print(bond)
            if warrant!="":
                newCharge = "Charges: " + charge + ", Warrant: " + warrant + "; Bond:"+ bond
            if warrant =="":
                newCharge = "Charges: " + charge + ", Bond:"+ bond
            charges = newCharge + "; " + charges
        summary = fullName + " was arrest on " + arrestDate + "by the " + agency
#         print(charges)
#         print(additionalInfo)
        if fullName:
            data_dict['fullName'] = fullName
        if image:
            data_dict['image'] = image
        if importantDates:
            data_dict['importantDates'] = importantDates
        if gender:
            data_dict['gender'] = gender
        if age:
            data_dict['age'] = age
        if height:
            data_dict['height'] = height
        if weight:
            data_dict['weight'] = weight
        if race:
            data_dict['race'] = race
        if dobYear:
            data_dict['dobYear'] = dobYear
        if eyes:
            data_dict['eyes'] = eyes
        if hair:
            data_dict['hair'] = hair
        if charges:
            data_dict['charges'] = charges
        if additionalInfo:
            data_dict['additionalInfo'] = additionalInfo
        if summary:
            data_dict['summary'] = summary
        data_list.append(data_dict)
    driver.quit()
    return data_list


# In[37]:


if __name__ == '__main__':
    data_list = get_data("add_slug_name")
    to_json(data_list)


# In[ ]:




