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


# In[12]:


def get_data(slug_name):
    data_list = []
    url = "https://www.eala.org/members/category/burundi"
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized") 
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--log-level=3")
    translator = GoogleTranslator(target='english')
    driver = webdriver.Chrome(options=options)
    driver.get(url)
    while True:
        try:
            list1 = driver.find_elements(By.XPATH, f'/html/body/div[1]/main/div/div/div/div/div[1]/div/div/div/div/h6/a')
            for i in range(1, len(list1)+1):
                data_dict = {}
                fullName = driver.find_element(By.XPATH, f'/html/body/div[1]/main/div/div/div/div/div[1]/div[{i}]/div/div/div/h6/a').text
                print(fullName)
                if "," in fullName:
                    firstName = fullName.split(",")[1].strip()
                    lastName = fullName.split(",")[0].strip()
                    fullName = firstName + " " + lastName
                driver.find_element(By.XPATH, f'/html/body/div[1]/main/div/div/div/div/div[1]/div/div/div/div/h6/a').click()
                time.sleep(3)
                image = driver.find_element(By.XPATH, f'/html/body/div[1]/main/div/div/div/div/div[1]/div[1]/div/div[1]/div/figure/a/img').get_attribute("src")
                print(image)
                constituency = driver.find_element(By.XPATH, f'/html/body/div[1]/main/div/div/div/div/div[1]/div[2]/div/div/div[2]/dl/dd[1]').text
    #             constituency = constituency.split(":")[1].strip()
                print(constituency)
                memberType = driver.find_element(By.XPATH, f'/html/body/div[1]/main/div/div/div/div/div[1]/div[2]/div/div/div[2]/dl/dd[2]').text
                print(memberType)
                addressLine1 = driver.find_element(By.XPATH, f'/html/body/div[1]/main/div/div/div/div/div[1]/div[2]/div/div/div[2]/dl/dd[3]').text
                print(addressLine1)
                telephoneNos = driver.find_element(By.XPATH, f'/html/body/div[1]/main/div/div/div/div/div[1]/div[2]/div/div/div[2]/dl/dd[4]').text
                print(telephoneNos)
                emails = driver.find_element(By.XPATH, f'/html/body/div[1]/main/div/div/div/div/div[1]/div[2]/div/div/div[2]/dl/dd[5]').text
                print(emails)
                importantDates = "Member Dates: " +  driver.find_element(By.XPATH, f'/html/body/div[1]/main/div/div/div/div/div[1]/div[2]/div/div/div[2]/dl/dd[6]').text
                print(importantDates)
    #             try:

    #                 committee = driver.find_elements(By.XPATH, f'/html/body/div[1]/main/div/div/div/div/div[1]/div[2]/div/div/div[2]/dl/dd[7]/a')
    # #                 print("Here")
    # #                 committee = committee.replace("\n", "; ")
    #                 print(len(committee))
    #             except Exception as e:
    #                 print(e)
    #                 pass
    #             try:
    #                 document = driver.find_element(By.XPATH, f'/html/body/div[1]/main/div/div/div/div/div[1]/div[2]/div/div/div[2]/dl/dd[8]').text
    #                 document = document.replace("\n", "; ")
    #                 print(document)
    #             except:
    #                 pass
                additionalInfo = "Member Type: " + memberType
                summary = fullName+ " is the member of East African Legislative Assembly"
                driver.back()
                print("*"*50)
                if fullName:
                    data_dict['fullName'] = fullName
                if image:
                    data_dict['image'] = image
                if constituency:
                    data_dict['constituency'] = constituency
                if addressLine1:
                    data_dict['addressLine1'] = addressLine1
                if telephoneNos:
                    data_dict['telephoneNos'] = telephoneNos
                if emails:
                    data_dict['emails'] = emails
                if importantDates:
                    data_dict['importantDates'] = importantDates
                if additionalInfo:
                    data_dict['additionalInfo'] = additionalInfo
                if summary:
                    data_dict['summary'] = summary
                data_list.append(data_dict)
            driver.find_element(By.XPATH, f'/html/body/div[1]/main/div/div/div/div/div[2]/ul/li[3]/a/i').click()
        except Exception as e:
            print(e)
            break
    driver.quit()
    return data_list


# In[13]:


if __name__ == '__main__':
    data_list = get_data("add_slug_name")
    to_json(data_list)

