#!/usr/bin/env python
# coding: utf-8

# In[24]:


from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import json


# In[25]:


def to_json(data):
    """
    This function takes list of dictionary as Input and 
    then Creates a JSON file in which Input data is stored
    """
    with open("data_dict11.json", "w") as outfile:
        json.dump(data, outfile,indent=4)
        outfile.close()


# In[26]:


data_list = []
url = "https://www.mca.gov.in/content/mca/global/en/contact-us/liasion-office.html"
options = webdriver.ChromeOptions()
options.add_argument("--start-maximized") 
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument("--log-level=3")


# In[27]:


def get_data(slug_name):
    driver = webdriver.Chrome(options=options)
    driver.get(url)
    data_dict = {}
    data_dict2 = {}
    time.sleep(3)

    name = driver.find_element(By.XPATH, f'/html/body/div/div/div[2]/div/div[3]/div/div/div[2]/div[5]/div/div/div/div/div/div/p[1]').text
    name = name.split(":",1)
    name = name[1].strip()
    name = name.split(" ", 1)
    title = name[0]
    name = name[1]
    print(title)
    print(name)

    designation = driver.find_element(By.XPATH, f'/html/body/div/div/div[2]/div/div[3]/div/div/div[2]/div[5]/div/div/div/div/div/div/p[2]').text
    designation = designation.split(":",1)
    designation = designation[1].strip()
    print(designation)

    contactDetails = driver.find_element(By.XPATH, f'/html/body/div/div/div[2]/div/div[3]/div/div/div[2]/div[5]/div/div/div/div/div/div/p[3]').text
    contactDetails = contactDetails.split(":",1)
    contactDetails = contactDetails[1].strip()
    print(contactDetails)
    summary = name + " is the " + designation
    if title:
        data_dict['title'] = title
    if name:
        data_dict['fullName'] = name
    if designation:
        data_dict['designation'] = designation
    if contactDetails:
        data_dict['contactDetails'] = contactDetails
    if summary:
        data_dict['summary'] = summary
    data_list.append(data_dict)    

    name = driver.find_element(By.XPATH, f'/html/body/div/div/div[2]/div/div[3]/div/div/div[2]/div[17]/div/div/div/div/div/div/p[1]').text
    name = name.split(":",1)
    name = name[1].strip()
    name = name.split(" ", 1)
    title = name[0]
    name = name[1]
    print(title)
    print(name)

    designation = driver.find_element(By.XPATH, f'/html/body/div/div/div[2]/div/div[3]/div/div/div[2]/div[17]/div/div/div/div/div/div/p[2]').text
    designation = designation.split(":",1)
    designation = designation[1].strip()
    print(designation)

    contactDetails = driver.find_element(By.XPATH, f'/html/body/div/div/div[2]/div/div[3]/div/div/div[2]/div[17]/div/div/div/div/div/div/p[3]').text
    contactDetails = contactDetails.split(":",1)
    contactDetails = contactDetails[1].strip()
    print(contactDetails)
    summary = name + " is the " + designation
    if title:
        data_dict2['title'] = title
    if name:
        data_dict2['fullName'] = name
    if designation:
        data_dict2['designation'] = designation
    if contactDetails:
        data_dict2['contactDetails'] = contactDetails
    if summary:
        data_dict2['summary'] = summary
    data_list.append(data_dict2)    
    return data_list


# In[28]:


if __name__ == '__main__':
    data_list = get_data("add_slug_name")
    to_json(data_list)


# In[ ]:




