#!/usr/bin/env python
# coding: utf-8

# In[43]:


from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import json


# In[44]:


def to_json(data):
    """
    This function takes list of dictionary as Input and 
    then Creates a JSON file in which Input data is stored
    """
    with open("data_dict9.json", "w") as outfile:
        json.dump(data, outfile,indent=4)
        outfile.close()


# In[45]:


data_list = []
url = "https://www.mca.gov.in/content/mca/global/en/contact-us/cost-audit-branch.html"
options = webdriver.ChromeOptions()
options.add_argument("--start-maximized") 
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument("--log-level=3")


# In[46]:


def get_data(slug_name):
    driver = webdriver.Chrome(options=options)
    driver.get(url)
    list1 = driver.find_elements(By.XPATH, f'//div[@class="tableComponent mt-4"]/table/tbody/tr')
    print(len(list1))
    for j in range (1, len(list1)+1, 2):
        data_dict = {}
        list2 = driver.find_elements(By.XPATH, f'//div[@class="tableComponent mt-4"]/table/tbody/tr[{j}]/td')
        for k in range (1, len(list2)+1):
            if k==1:
                name = driver.find_element(By.XPATH, f'//div[@class="tableComponent mt-4"]/table/tbody/tr[{j}]/td[{k}]').text
                name = name.split(" ", 1)
                title = name[0]
                name = name[1]
            elif k==2:
                designation = driver.find_element(By.XPATH, f'//div[@class="tableComponent mt-4"]/table/tbody/tr[{j}]/td[{k}]').text
            elif k==3:
                contactDetails = driver.find_element(By.XPATH, f'//div[@class="tableComponent mt-4"]/table/tbody/tr[{j}]/td[{k}]').text.replace("\n", ",")
            elif k==4:
                emails = driver.find_element(By.XPATH, f'//div[@class="tableComponent mt-4"]/table/tbody/tr[{j}]/td[{k}]').text.strip()
                emails = emails.replace("[dot]", ".").replace("[at]", "@").replace("\n", "")
        summary = name + " is the " + designation 
        if title:
            data_dict['title'] = title
        if name:
            data_dict['fullName'] = name
        if designation:
            data_dict['designation'] = designation
        if contactDetails:
            data_dict['contactDetails'] = contactDetails
        if emails:
            data_dict['emails'] = emails
        if summary:
            data_dict['summary'] = summary
        data_list.append(data_dict)
    return  data_list


# In[47]:


if __name__ == '__main__':
    data_list = get_data("add_slug_name")
    to_json(data_list)


# In[ ]:




