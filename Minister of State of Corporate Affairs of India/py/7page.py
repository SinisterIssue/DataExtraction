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
    with open("data_dict7.json", "w") as outfile:
        json.dump(data, outfile,indent=4)
        outfile.close()


# In[3]:


data_list = []
url = "https://www.mca.gov.in/content/mca/global/en/contact-us/roc.html"
options = webdriver.ChromeOptions()
options.add_argument("--start-maximized") 
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument("--log-level=3")


# In[4]:


def get_data(slug_name):
    driver = webdriver.Chrome(options=options)
    driver.get(url)
    list1 = driver.find_elements(By.XPATH, f'//div/table/tbody/tr')
    for i in range(1, len(list1)+1):
        data_dict = {}
        try:
            driver.find_element(By.XPATH, f'//div/div/table[{i}]/tbody/tr[1]/td/img').click()
            time.sleep(3)
            name = driver.find_element(By.XPATH, f'//div/div/table[{i}]/tbody/tr[2]/td/div/div/div/p').text
            name = name.split(" ", 1)
            title = name[0]
            name = name[1]
            name = name.split("(", 1)
            roc = name[1].replace(")", "")
            name = name[0]
            
            contactDetails = driver.find_element(By.XPATH, f'//div/div/table[{i}]/tbody/tr[2]/td/div/div/div/table[2]/tbody/tr[1]/td[2]').text.strip().replace("\n", ",").replace("[dot]", ".").replace("[at]", "@")
            print(contactDetails)

            fullAddress = driver.find_element(By.XPATH, f'//div/div/table[{i}]/tbody/tr[2]/td/div/div/div/table[2]/tbody/tr[2]/td[2]/p').text.strip().replace("\n", "")
            print(fullAddress)

            rd = driver.find_element(By.XPATH, f'//div/div/table[{i}]/tbody/tr[2]/td/div/div/div/table[2]/tbody/tr[3]/td[2]/p').text.strip()
            print(rd)

            summary = name + " is the Registar of companies of " + rd+ "."

            if title:
                data_dict['title'] = title
            if name:
                data_dict['fullName'] = name
            if contactDetails:
                data_dict['contactDetails'] = contactDetails
            if fullAddress:
                data_dict['fullAddress'] = fullAddress
            if rd:
                data_dict['rd'] = rd
            if roc:
                data_dict['roc'] = roc
            if summary:
                data_dict['summary'] = summary
            data_list.append(data_dict)
        except:
            pass
    return data_list


# In[5]:


if __name__ == '__main__':
    data_list = get_data("add_slug_name")
    to_json(data_list)


# In[ ]:




