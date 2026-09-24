#!/usr/bin/env python
# coding: utf-8

# In[31]:


from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import json
import re


# In[32]:


def to_json(data):
    """
    This function takes list of dictionary as Input and 
    then Creates a JSON file in which Input data is stored
    """
    with open("data_dict.json", "w") as outfile:
        json.dump(data, outfile,indent=4)
        outfile.close()


# In[33]:


data_list = []
url = "https://www.insider.com/most-famous-popular-celebrity-born-each-year-2017-10"
options = webdriver.ChromeOptions()
options.add_argument("--start-maximized") 
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument("--log-level=3")


# In[34]:


def get_data(slug_name):
    driver = webdriver.Chrome(options=options)
    driver.get(url)
    list1 = driver.find_elements(By.XPATH, f'//div/div/div/div/div[1]/h2')
    for i in range(2, 2*len(list1)):
        data_dict = {}
        try:
            info = driver.find_element(By.XPATH, f'//div/div/div[{i}]/div/div[1]/h2').text
            dob = info.split(":")[0]
    #         print(dob)
            name = info.split(":")[1].strip()
            prefix = ""
            alias = ""
            if "and" not in name and "Prince" not in name and "Pincess" not in name:
                fullName = name
            if "and" in name:
                fullName = ""
            if "Prince" in name:
                prefix = name.split(" ")[0]
                name = name.split(" ")[1]
                fullName = name
            if "Princess" in name:
                prefix = name.split(" ")[0]
                name = name.split(" ")[1]
                fullName = name
#             print(fullName)
            image = driver.find_element(By.XPATH, f'//div/div/div[{i}]/div/figure/div/img').get_attribute("data-srcs")
            image = image.split('"')[1]
            print(image)
            additionalInfo = driver.find_element(By.XPATH, f'//div/div/div[{i}]/div/p[1]').text
    #         print(additionalInfo)
            try:
                dobMonthDate = re.findall('[A-Za-z]{3,12} \d{1,2}',additionalInfo)[0]
                if dobMonthDate=="year 19":
                    dobMonthDate = ''
                dobFull = ''
                if dobMonthDate:
                    dobFull = dobMonthDate + " "+dob
            except:
                pass
            fullName = fullName.replace(".", "")
            summary = prefix + " " +fullName + " is the most famous celebrity born on the year " + dob
            
            if fullName:
                data_dict['fullName'] = fullName
                if prefix:
                    data_dict['prefix'] = prefix
                if dobFull:
                    data_dict['dob'] = dobFull
                if dob:
                    data_dict['dobYear'] = dob
                if image:
                    data_dict['image'] = image
                if additionalInfo:
                    data_dict['additionalInfo'] = additionalInfo
                if summary:
                    data_dict['summary'] = summary
            if len(data_dict) != 0:
                    data_list.append(data_dict)
            newNames = driver.find_element(By.XPATH, f'//div/div/div[{i}]/div/p[2]').text
            newNames = newNames.split(":")[1].strip()
            newNames = newNames.replace("and ", "")
            newNames = newNames.replace("  ", ",")
#             print(newNames)
            newNames = newNames.split(",")
            for j in range(0, len(newNames)):
                data_dict2 = {}
                alias = ""
                prefix=""
                fullNames = newNames[j].strip()
                if "born" in fullNames:
                    fullNames=""
                if "twins"in fullNames:
                    fullNames = fullNames.split("twins")[1].strip()
                if "child" in fullNames:
                    fullNames = fullNames.split("child")[1].strip()
#                 print(fullNames)
                if "Prince" in fullNames:
                    prefix = fullNames.split(" ")[0]
                    fullNames = fullNames.split(" ")[1]
                if "At some point" in fullNames:
                    fullNames = ""
                if "50 Cent" in fullNames:
                    alias = fullNames
                    fullNames = "Curtis James Jackson III"
                if "Psy." in fullNames:
                    alias = fullNames
                    fullNames = "Park Jae-sang"
                if "Bow Wow" in fullNames:
                    alias = fullNames
                    fullNames = "Shad Gregory Moss"
                if "the Creator" in fullNames:
                    alias = fullNames
                    fullNames = "Tyler Gregory Okonma"
                if "Chance the Rapper" in fullNames:
                    alias = fullNames
                    fullNames = "Chancelor Johnathan Bennett"
                dobYear = dob
                fullNames = fullNames.replace(".", "")
                summary = prefix +" " +fullNames + " is one of the famous celebrity born on the year " + dobYear
                
                if fullNames:
                    data_dict2['fullName'] = fullNames
                    if prefix:
                        data_dict2['prefix'] = prefix
                    if alias:
                        data_dict2['alias'] = alias
                    if dobYear:
                        data_dict2['dobYear'] = dobYear
                    if summary:
                        data_dict2['summary'] = summary
                if len(data_dict2) != 0:
                    data_list.append(data_dict2)
        except:
            pass
    return data_list


# In[35]:


if __name__ == '__main__':
    data_list = get_data("add_slug_name")
    to_json(data_list)


# In[ ]:




