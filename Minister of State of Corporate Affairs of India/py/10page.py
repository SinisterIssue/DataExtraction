#!/usr/bin/env python
# coding: utf-8

# In[17]:


from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import json


# In[18]:


def to_json(data):
    """
    This function takes list of dictionary as Input and 
    then Creates a JSON file in which Input data is stored
    """
    with open("data_dict10.json", "w") as outfile:
        json.dump(data, outfile,indent=4)
        outfile.close()


# In[19]:


data_list = []
url = "https://www.mca.gov.in/content/mca/global/en/contact-us/nodal-officers.html"
options = webdriver.ChromeOptions()
options.add_argument("--start-maximized") 
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument("--log-level=3")
driver = webdriver.Chrome(options=options)


# In[22]:


def get_data(slug_name):
    data_list = []
    url = "https://www.mca.gov.in/content/mca/global/en/contact-us/nodal-officers.html"
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized") 
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--log-level=3")
    driver = webdriver.Chrome(options=options)
    driver.get(url)
    data_dict = {}
    name = driver.find_element(By.XPATH, f'//div[2]/div[3]/div/div/div/div/div/div[1]/div/p[1]').text
    name = name.strip()
    name = name.split(" ", 1)
    title = name[0]
    name = name[1]
#     data_dict['fullName'] = name
#     data_dict['title'] = title
    print(name)
    print(title)

    designation = driver.find_element(By.XPATH, f'//div[2]/div[3]/div/div/div/div/div/div[1]/div/p[2]').text
    designation = designation.strip()
#     data_dict['designation'] = designation
    print(designation)
    
    contactDetails = driver.find_element(By.XPATH, f'//div[2]/div[3]/div/div/div/div/div/div[1]/div/p[3]').text
    contactDetails = contactDetails.strip()
    contactDetails = contactDetails.split(":", 1)
    contactDetails = contactDetails[1].replace("[dot]", ".").replace("[at]", "@").replace("\n", "")
    contactDetails = contactDetails.split(" ")
    print(contactDetails)
    emails = contactDetails[2]
    contactDetails = contactDetails[1]
    print(emails)
    print(contactDetails)
    
    fullAddress = driver.find_element(By.XPATH, f'//div[2]/div[3]/div/div/div/div/div/div[1]/div/p[4]').text.strip()
    fullAddress = fullAddress.split(":", 1)
    fullAddress = fullAddress[1].replace("\n", "")
    print(fullAddress)
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
    driver.find_element(By.XPATH, '//div[3]/div/div/div/div//*[@id="view-ofc"]').click()
    time.sleep(3)
    list1 = driver.find_elements(By.XPATH, f'//div[@class="office-table"]/table/tbody/tr')
    for j in range(1, len(list1)+1):
        data_dict2 = {}
        list2 = driver.find_elements(By.XPATH, f'//div[@class="office-table"]/table/tbody/tr[{j}]/td')
        for k in range (1, len(list2)+1):
            if k==1:
                name = driver.find_element(By.XPATH, f'//div[@class="office-table"]/table/tbody/tr[{j}]/td[{k}]').text
                name = name.split(" ", 1)
                title = name[0]
                name = name[1]
                print(title)
                print(name)
            elif k==2:
                designation = driver.find_element(By.XPATH, f'//div[@class="office-table"]/table/tbody/tr[{j}]/td[{k}]').text
                print(designation)
            elif k==3:
                contactDetails = driver.find_element(By.XPATH, f'//div[@class="office-table"]/table/tbody/tr[{j}]/td[{k}]').text.replace("\n", ",")
                print(contactDetails)
            elif k==4:
                emails = driver.find_element(By.XPATH, f'//div[@class="office-table"]/table/tbody/tr[{j}]/td[{k}]').text.replace("[dot]", ".").replace("[at]", "@")
                if emails == "-":
                    emails = ""
                print(emails)
                
            summary = name + " is the " + designation
        if title:
            data_dict2['title'] = title
        if name:
            data_dict2['fullName'] = name
        if designation:
            data_dict2['designation'] = designation
        if contactDetails:
            data_dict2['contactDetails'] = contactDetails
        if emails:
            data_dict2['emails'] = emails
        if summary:
            data_dict2['summary'] = summary
        data_list.append(data_dict2)
   
    return data_list


# In[23]:


if __name__ == '__main__':
    data_list = get_data("add_slug_name")
    to_json(data_list)


# In[ ]:




