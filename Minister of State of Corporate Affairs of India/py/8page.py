#!/usr/bin/env python
# coding: utf-8

# In[1]:


from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import json


# In[2]:


def to_json(data):
    """
    This function takes list of dictionary as Input and 
    then Creates a JSON file in which Input data is stored
    """
    with open("data_dict8.json", "w") as outfile:
        json.dump(data, outfile,indent=4)
        outfile.close()


# In[3]:


data_list = []
url = "https://www.mca.gov.in/content/mca/global/en/contact-us/official-liquidators.html"
options = webdriver.ChromeOptions()
options.add_argument("--start-maximized") 
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument("--log-level=3")


# In[4]:


def get_data(slug_name):
    driver = webdriver.Chrome(options=options)
    driver.get(url)
    driver.find_element(By.XPATH, f'//div/div/div[2]/div[5]/div/button').click()
    list1 = driver.find_elements(By.XPATH, f'//div[5]/div/table/tbody/tr')
    for j in range (1, len(list1)+1, 2):
        data_dict = {}
        list2 = driver.find_elements(By.XPATH, f'//div[5]/div/table/tbody/tr[{j}]/td')
        for k in range (1, len(list2)+1):
            if k==1:
                name = driver.find_element(By.XPATH, f'//div[5]/div/table/tbody/tr[{j}]/td[{k}]').text
                name = name.split(" ", 1)
                title = name[0]
                name = name[1]
            elif k==2:
                designation = driver.find_element(By.XPATH, f'//div[5]/div/table/tbody/tr[{j}]/td[{k}]').text
            elif k==3:
                contactDetails = driver.find_element(By.XPATH, f'//div[5]/div/table/tbody/tr[{j}]/td[{k}]').text.replace("\n", ",").replace("[dot]", ".").replace("[at]", "@")
            elif k==4:
                fullAddress = driver.find_element(By.XPATH, f'//div[5]/div/table/tbody/tr[{j}]/td[{k}]').text.replace("\n", "").replace("View on Map", "")
        summary = name + " is the " + designation
        if title:
            data_dict['title'] = title
        if name:
            data_dict['fullName'] = name
        if designation:
            data_dict['designation'] = designation
        if contactDetails:
            data_dict['contactDetails'] = contactDetails
        if fullAddress:
            data_dict['fullAddress'] = fullAddress
        if summary:
            data_dict['summary'] = summary
        data_list.append(data_dict)
    return data_list


# In[5]:


if __name__ == '__main__':
    data_list = get_data("add_slug_name")
    to_json(data_list)


# In[ ]:




