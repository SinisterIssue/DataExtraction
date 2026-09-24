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


# In[14]:


def get_data(slug_name):
    data_list = []
    url = "https://www.bis.doc.gov/index.php/about-bis/organization/senior-management-team"
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized") 
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--log-level=3")
    translator = GoogleTranslator(target='english')
    driver = webdriver.Chrome(options=options)
    driver.get(url)
    list1 = driver.find_elements(By.XPATH, f'/html/body/div[1]/div[2]/div[2]/div[1]/div[2]/div[2]/p')
    print(len(list1))
    for i in range(1, len(list1)):
        try:
            data_dict = {}
            image = ""
            careerInfo = ""
            educationInfo = ""
            fullName = driver.find_element(By.XPATH, f'/html/body/div[1]/div[2]/div[2]/div[1]/div[2]/div[2]/p[{i}]').text
            careerInfoDesignation = fullName.split(",")[1].strip()
            fullName = fullName.split(",")[0]
            print(fullName)
            print(careerInfoDesignation)
            try:
                try:
                    driver.find_element(By.XPATH, f'/html/body/div[1]/div[2]/div[2]/div[1]/div[2]/div[2]/p[{i}]/a').click()
                except:
                    try:
                        driver.find_element(By.XPATH, f'/html/body/div[1]/div[2]/div[2]/div[1]/div[2]/div[2]/p[{i}]/span/a').click()
                    except:
                        try:
                            driver.find_element(By.XPATH, f'/html/body/div[1]/div[2]/div[2]/div[1]/div[2]/div[2]/p[{i}]/span[1]/span/a').click()
                        except:
                            try:
                                driver.find_element(By.XPATH, f'/html/body/div[1]/div[2]/div[2]/div[1]/div[2]/div[2]/p[{i}]/span/span/span/span/a').click()
                            except:
                                pass
                time.sleep(2)
                try:
                    image = driver.find_element(By.XPATH, f'/html/body/div[1]/div[2]/div[1]/div[1]/div[2]/div[3]/p[1]/img').get_attribute('src')
                    print(image)
                except:
                    try:
                        image = driver.find_element(By.XPATH, f'/html/body/div[1]/div[2]/div[1]/div[1]/div[2]/div[2]/p[4]/img').get_attribute('src')
                        print(image)
                    except:
                        pass
                careerInfo = driver.find_element(By.XPATH, f'/html/body/div[1]/div[2]/div[1]/div[1]/div[2]/div[2]').text
                if "Print" in careerInfo:
                    careerInfo = driver.find_element(By.XPATH, f'/html/body/div[1]/div[2]/div[1]/div[1]/div[2]/div[3]').text
                careerInfo = careerInfo.replace("\n", "; ").strip()
                print(careerInfo)
                educationInfo = careerInfo.split(".;")[-2].strip()
                print(educationInfo)
                driver.back()
            except:
                pass
            summary = fullName + " is the "+ careerInfoDesignation + " of Bureau of Industry and Security."
            if fullName:
                data_dict['fullName'] = fullName
            if careerInfoDesignation:
                data_dict['careerInfoDesignation'] = careerInfoDesignation
            if image:
                data_dict['image'] = image
            if careerInfo:
                data_dict['careerInfo'] = careerInfo
            if educationInfo:
                data_dict['educationInfo'] = educationInfo
            if summary:
                data_dict['summary'] = summary
            data_list.append(data_dict)
        except:
            pass
        print("*"*50)
    driver.quit()
    return data_list


# In[15]:


if __name__ == '__main__':
    data_list = get_data("add_slug_name")
    to_json(data_list)


# In[ ]:




