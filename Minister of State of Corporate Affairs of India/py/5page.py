#!/usr/bin/env python
# coding: utf-8

# In[106]:


from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import json


# In[107]:


def to_json(data):
    """
    This function takes list of dictionary as Input and 
    then Creates a JSON file in which Input data is stored
    """
    with open("data_dict5.json", "w") as outfile:
        json.dump(data, outfile,indent=4)
        outfile.close()


# In[108]:


data_list = []
url = "https://www.mca.gov.in/content/mca/global/en/contact-us/DGCOA-Officers.html"
options = webdriver.ChromeOptions()
options.add_argument("--start-maximized") 
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument("--log-level=3")


# In[109]:


def get_data(slug_name):
    data_list = []
    url = "https://www.mca.gov.in/content/mca/global/en/contact-us/DGCOA-Officers.html"
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized") 
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--log-level=3")
    driver = webdriver.Chrome(options=options)
    driver.get(url)
    
#     try:
    list1 = driver.find_elements(By.XPATH, f'//div[3]/div/table/tbody/tr')
    print(len(list1))
    for j in range(1, len(list1)+1, 2):
        data_dict = {}
        list2 = driver.find_elements(By.XPATH, f'//div[3]/div/table/tbody/tr[{j}]/td')
        for k in range (1, len(list2)+1):
            if k==1:
                name = driver.find_element(By.XPATH, f'//div[3]/div/table/tbody/tr[{j}]/td[{k}]').text
                name = name.split(" ", 1)
                title = name[0]
                name = name[1]
            elif k==2:
                designation = driver.find_element(By.XPATH, f'//div[3]/div/table/tbody/tr[{j}]/td[{k}]').text
            elif k==3:
                contactDetails = driver.find_element(By.XPATH, f'//div[3]/div/table/tbody/tr[{j}]/td[{k}]').text
            elif k==4:
                emails = driver.find_element(By.XPATH, f'//div[3]/div/table/tbody/tr[{j}]/td[{k}]').text.strip()
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

#     print(data_list)
    return data_list


# In[110]:


if __name__ == '__main__':
    data_list = get_data("add_slug_name")
    to_json(data_list)


# In[ ]:





# In[ ]:


#     except:
#         pass
#         if len(name.strip()):
#             # temp_dict and temp_list will be used to remove dulicate entries for each entity
#             temp_dict['fullName'] = name
#             temp_dict['designation'] = designation
#             temp_dict['contactDetails'] = contactDetails
#             temp_dict['emails'] = emails
#             if temp_dict not in temp_list:
#                 temp_list.append(temp_dict)

#                 if len(name.strip()):
#                     data_dict['fullName'] = name
#                     if len(designation.strip()):
#                         data_dict['designation'] = designation
#                     if len(contactDetails.strip()):
#                         data_dict['contactDetails'] = contactDetails
#                     if len(emails.strip()):
#                         data_dict['emails'] = emails
#             data_list.append(data_dict)

