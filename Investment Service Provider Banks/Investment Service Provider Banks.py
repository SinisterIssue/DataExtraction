#!/usr/bin/env python
# coding: utf-8

# In[13]:


from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import json
import re
from deep_translator import GoogleTranslator


# In[14]:


def to_json(data):
    """
    This function takes list of dictionary as Input and 
    then Creates a JSON file in which Input data is stored
    """
    with open("data_dict.json", "w") as outfile:
        json.dump(data, outfile,indent=4)
        outfile.close()


# In[19]:


def get_data(slug_name):
    data_list = []
    url = "https://www.cba.am/EN/SitePages/fscfoinvestmentbanks.aspx"
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized") 
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--log-level=3")
    translator = GoogleTranslator(target='english')
    driver = webdriver.Chrome(options=options)
    driver.get(url)
    list1 = driver.find_elements(By.XPATH, f'//div/div/table/tbody/tr/td/table/tbody/tr/td/div/table/tbody/tr')
    for i in range(1, len(list1)+1):
        data_dict={}
        services = ""
        list2 = driver.find_elements(By.XPATH, f'//div/div/table/tbody/tr/td/table/tbody/tr/td/div/table/tbody/tr[{i}]/td')
        for j in range(1, len(list2)+1):
            if j==1:
                fullName = driver.find_element(By.XPATH, f'//div/div/table/tbody/tr/td/table/tbody/tr/td/div/table/tbody/tr[{i}]/td[{j}]').text
                fullName = fullName.split('"')
                types  = fullName[2].strip()
                fullName = fullName[1]
                print(types)
                print(fullName)
            if j==2:
                services = driver.find_element(By.XPATH, f'//div/div/table/tbody/tr/td/table/tbody/tr/td/div/table/tbody/tr[{i}]/td[{j}]').text + "; " + services
                services = services.replace("25/1", "receive and transmit customer orders for securities transactions")
            if j==3:
                services = driver.find_element(By.XPATH, f'//div/div/table/tbody/tr/td/table/tbody/tr/td/div/table/tbody/tr[{i}]/td[{j}]').text + "; " + services
                services = services.replace("25/2", "execute securities transactions on their behalf/at their expense or on their client’s behalf/at the client’s expense")
            if j==4:
                services = driver.find_element(By.XPATH, f'//div/div/table/tbody/tr/td/table/tbody/tr/td/div/table/tbody/tr[{i}]/td[{j}]').text + "; " + services
                services = services.replace("25/3", "provide consultancy to the customer about investment in securities")
            if j==5:
                services = driver.find_element(By.XPATH, f'//div/div/table/tbody/tr/td/table/tbody/tr/td/div/table/tbody/tr[{i}]/td[{j}]').text + "; " + services
                services = services.replace("25/4", "execute securities transactions at their expense and on their behalf")
            if j==6:
                services = driver.find_element(By.XPATH, f'//div/div/table/tbody/tr/td/table/tbody/tr/td/div/table/tbody/tr[{i}]/td[{j}]').text + "; " + services
                services = services.replace("25/5", "Securities portfolio management")
            if j==7:
                services = driver.find_element(By.XPATH, f'//div/div/table/tbody/tr/td/table/tbody/tr/td/div/table/tbody/tr[{i}]/td[{j}]').text + "; " + services
                services = services.replace("25/6", "guaranteed or non-guaranteed securities underwriting")
        services = services.replace(" ;  ; ", "").replace(";  ; ", "; ")
        summary = fullName+  " is one of the Investment Service Provider Banks in Armenia."
        print(services)
        print("*"*50)
        if fullName:
            data_dict['fullName'] = fullName
        if types:
            data_dict['type'] = types
        if services:
            data_dict['services'] = services
        if summary:
            data_dict['summary'] = summary
        data_list.append(data_dict)
    driver.quit()
    return data_list


# In[20]:


if __name__ == '__main__':
    data_list = get_data("add_slug_name")
    to_json(data_list)


# In[ ]:




