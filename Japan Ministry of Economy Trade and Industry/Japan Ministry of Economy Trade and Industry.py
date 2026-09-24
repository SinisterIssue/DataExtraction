#!/usr/bin/env python
# coding: utf-8

# In[48]:


from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import json
import re
from deep_translator import GoogleTranslator


# In[49]:


def to_json(data):
    """
    This function takes list of dictionary as Input and 
    then Creates a JSON file in which Input data is stored
    """
    with open("data_dict.json", "w") as outfile:
        json.dump(data, outfile,indent=4)
        outfile.close()


# In[50]:


def get_data(slug_name): 
    data_list = []
    url = "https://www.meti.go.jp/english/aboutmeti/profiles/"
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized") 
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--log-level=3")
    translator = GoogleTranslator(target='english')
    driver = webdriver.Chrome(options=options)
    driver.get(url)
    for i in range(1, 5):
        list1 = driver.find_elements(By.XPATH, f'/html/body/div/div[3]/div[{i}]/div')
        for j in range(1, len(list1)+1):
            data_dict = {}
            careerInfo = ""
            educationInfo = ""
            lastUpdatedAt = ""
            dob=""
            placeOfBirthCity= ""
            try:
                image = driver.find_element(By.XPATH, f'/html/body/div/div[3]/div[{i}]/div[{j}]/a/img').get_attribute('src')
    #             print(image)
                fullName = driver.find_element(By.XPATH, f'/html/body/div/div[3]/div[{i}]/div[{j}]/a').text
                careerInfoDesignation = fullName.split("\n")[0]
                fullName = fullName.split("\n")[1].title()
                print(fullName)
                try:
                    driver.find_element(By.XPATH, f'/html/body/div/div[3]/div[{i}]/div[{j}]/a').click()
                    time.sleep(2)
                    list2 = driver.find_elements(By.XPATH, f'/html/body/div/div[3]/div[1]/p')
                    for k in range(1, len(list2)+1):
                        heading = driver.find_element(By.XPATH, f'/html/body/div/div[3]/div[1]/p[{k}]').text
                        if "born on" in heading:
                            dob = driver.find_element(By.XPATH, f'/html/body/div/div[3]/div[1]/p[{k}]').text
                            dob = dob.split("born on")[1]
                            try:
                                placeOfBirthCity = dob.split(", in")[1].replace(".", "").strip()
                                dob = dob.split(", in")[0].replace(".", "").strip()
                            except:
                                placeOfBirthCity = dob.split("in")[1].strip()
                                dob = dob.split("in")[0].replace(".", "").strip()
    #                         print(placeOfBirthCity)
                        elif "born in" in heading:
                            placeOfBirthCity = driver.find_element(By.XPATH, f'/html/body/div/div[3]/div[1]/p[{k}]').text
                            placeOfBirthCity = placeOfBirthCity.split("born in")[1]
                            dob = placeOfBirthCity.split("on")[1].replace(".", "").strip()
                            placeOfBirthCity = placeOfBirthCity.split("on")[0].replace(".", "").strip()
    #                         print(dob)
    #                         print(placeOfBirthCity)
                        else:
                            careerInfo = driver.find_element(By.XPATH, f'/html/body/div/div[3]/div[1]/p[{k}]').text + careerInfo
                        if "graduate" in heading:
                            educationInfo = driver.find_element(By.XPATH, f'/html/body/div/div[3]/div[1]/p[{k}]').text  
                            if "born on" in educationInfo:
                                educationInfo = educationInfo.split(",", 1)[0]
                            if "born in" in heading:
                                if len(educationInfo.split("."))<=3:
                                    print(educationInfo.split("."))
                                    educationInfo = educationInfo.split(".")[0].split(",")[0]
                                if len(educationInfo.split("."))>3:
    #                                 print("here")
                                    educationInfo = educationInfo.split(".")[1].strip()

                            print(educationInfo)

    #                 print(careerInfo)
                    lastUpdatedAt = driver.find_element(By.XPATH, f'/html/body/div/div[3]/div[2]/p').text
                    lastUpdatedAt = lastUpdatedAt.split("Last updated:")[1]
                    d = lastUpdatedAt.split("-")[2]
                    m = lastUpdatedAt.split("-")[1]
                    y = lastUpdatedAt.split("-")[0]
                    lastUpdatedAt = d + "/" + m + "/" + y
                    driver.back()
                except:
                    pass
            except:
                image = driver.find_element(By.XPATH, f'/html/body/div/div[3]/div[{i}]/div[{j}]/img').get_attribute('src')
    #             print(image)
                fullName = driver.find_element(By.XPATH, f'/html/body/div/div[3]/div[{i}]/div[{j}]').text
                careerInfoDesignation = fullName.split("\n")[0]
                fullName = fullName.split("\n")[1].title()
                print(fullName)
                lastUpdatedAt = driver.find_element(By.XPATH, f'/html/body/div/div[3]/div[5]/p').text
                lastUpdatedAt = lastUpdatedAt.split("Last updated:")[1]
                d = lastUpdatedAt.split("-")[2]
                m = lastUpdatedAt.split("-")[1]
                y = lastUpdatedAt.split("-")[0]
                lastUpdatedAt = d + "/" + m + "/" + y
            summary = fullName + " is the "  + careerInfoDesignation
            if fullName:
                data_dict['fullName'] = fullName
            if careerInfoDesignation:
                data_dict['careerInfoDesignation'] = careerInfoDesignation
            if image:
                data_dict['image'] = image
            if dob:
                data_dict['dob'] = dob
            if placeOfBirthCity:
                data_dict['placeOfBirthCity'] = placeOfBirthCity
            if careerInfo:
                data_dict['careerInfo'] = careerInfo
            if educationInfo:
                data_dict['educationInfo'] = educationInfo
            if lastUpdatedAt:
                data_dict['lastUpdatedAt'] = lastUpdatedAt
            if summary:
                data_dict['summary'] = summary
            data_list.append(data_dict)
            print("*"*50)
    driver.quit()
    return data_list


# In[51]:


if __name__ == '__main__':
    data_list = get_data("add_slug_name")
    to_json(data_list)


# In[ ]:




