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
    with open("data_dict4.json", "w") as outfile:
        json.dump(data, outfile,indent=4)
        outfile.close()


# In[3]:


data_list = []
url = "https://www.mca.gov.in/content/mca/global/en/contact-us/officials-at-head-quarters.html"
options = webdriver.ChromeOptions()
options.add_argument("--start-maximized") 
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument("--log-level=3")
driver = webdriver.Chrome(options=options)


# In[4]:


def get_data(slug_name):
    data_list = []
    url = "https://www.mca.gov.in/content/mca/global/en/contact-us/officials-at-head-quarters.html"
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized") 
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--log-level=3")
    driver = webdriver.Chrome(options=options)
    driver.get(url)
    data_dict = {}
    name = driver.find_element(By.XPATH, f'//div/div[1]/div[2]//*[@class="profileHeader row"]').text
    name = name.strip()
    name = name.split(" ", 1)
    title = name[0]
    name = name[1]
    data_dict['fullName'] = name
    data_dict['title'] = title

    designation = driver.find_element(By.XPATH, f'//div/div/div[1]/div[2]/p[2]//*[@class="contentdata col-9"]').text
    designation = designation.strip()
    data_dict['designation'] = designation

    image = driver.find_element(By.XPATH, f'//div/div/div[1]/div[1]//*[@class="profilecard-img"]').get_attribute("src")
    data_dict['image'] = image
    data_list.append(data_dict)
    summary = name + " is the " + designation
    data_dict['summary'] = summary
    
    driver.find_element(By.XPATH, '//div[3]/div/div/div/div//*[@id="view-ofc"]').click()
    driver.find_element(By.XPATH, '//div/div[2]/div[4]/div//*[@id="viewmore"]').click()
    time.sleep(3)
    list1 = driver.find_elements(By.XPATH, f'//div[@class="office-table"]/table/tbody/tr')
    for j in range(1, len(list1)+1):
        data_dict2 = {}
        list2 = driver.find_elements(By.XPATH, f'//div/table/tbody/tr[{j}]/td')
        for k in range (1, len(list2)+1):
            if k==1:
                name = driver.find_element(By.XPATH, f'//div/table/tbody/tr[{j}]/td[{k}]').text
                name = name.split(" ", 1)
                title = name[0]
                name = name[1]
                print(name)
            elif k==2:
                designation = driver.find_element(By.XPATH, f'//div/table/tbody/tr[{j}]/td[{k}]').text
                print(designation)
            elif k==3:
                contactDetails = driver.find_element(By.XPATH, f'//div/table/tbody/tr[{j}]/td[{k}]').text.replace("\n", ",")
                print(contactDetails)
            elif k==4:
                emails = driver.find_element(By.XPATH, f'//div/table/tbody/tr[{j}]/td[{k}]').text.replace("[dot]", ".").replace("[at]", "@")
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
    try:
        list3 = driver.find_elements(By.XPATH, f'//div[@class="tableComponent mt-4"]/table/tbody/tr')
        for j in range(1, len(list3)+1, 2):
            data_dict3 = {}
            list4 = driver.find_elements(By.XPATH, f'//div[@class="tableComponent mt-4"]/table/tbody/tr[{j}]/td')
            try:
                driver.find_element(By.XPATH, f'//div[@class="tableComponent mt-4"]/table/tbody/tr[{j}]/td[5]/img').click()
                time.sleep(2)
            except:
                pass
            for k in range(1, len(list4)+1):
                if k==1:
                    name = driver.find_element(By.XPATH, f'//div[@class="tableComponent mt-4"]/table/tbody/tr[{j}]/td[{k}]').text
                    name = name.split(" ", 1)
                    title = name[0]
                    name = name[1]
                elif k==2:
                    designation = driver.find_element(By.XPATH, f'//div[@class="tableComponent mt-4"]/table/tbody/tr[{j}]/td[{k}]').text
                elif k==3:
                    contactDetails = driver.find_element(By.XPATH, f'//div[@class="tableComponent mt-4"]/table/tbody/tr[{j}]/td[{k}]').text.replace("\n", ",")
                    if contactDetails ==  "-":
                        contactDetails = ""
                elif k==4:
                    emails = driver.find_element(By.XPATH, f'//div[@class="tableComponent mt-4"]/table/tbody/tr[{j}]/td[{k}]').text.replace("[dot]", ".").replace("[at]", "@").replace("\n", "")
                    if emails == "-":
                        emails = ""
                summary = name + " is the " + designation
            if title:
                data_dict3['title'] = title
            if name:
                data_dict3['fullName'] = name
            if designation:
                data_dict3['designation'] = designation
            if contactDetails:
                data_dict3['contactDetails'] = contactDetails
            if emails:
                data_dict3['emails'] = emails
            if summary:
                data_dict3['summary'] = summary
            data_list.append(data_dict3)

    except:
        pass
    return data_list


# In[5]:


if __name__ == '__main__':
    data_list = get_data("add_slug_name")
    to_json(data_list)


# In[ ]:




