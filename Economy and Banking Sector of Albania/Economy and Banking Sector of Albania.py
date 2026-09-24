#!/usr/bin/env python
# coding: utf-8

# In[30]:


from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import json
import re
from deep_translator import GoogleTranslator


# In[31]:


def to_json(data):
    """
    This function takes list of dictionary as Input and 
    then Creates a JSON file in which Input data is stored
    """
    with open("data_dict.json", "w") as outfile:
        json.dump(data, outfile,indent=4)
        outfile.close()


# In[32]:


def get_data(slug_name):
    data_list = []
    url = "https://thebanks.eu/countries/Albania/major_banks"
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized") 
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--log-level=3")
    translator = GoogleTranslator(target='english')
    driver = webdriver.Chrome(options=options)
    driver.get(url)
    info = driver.find_element(By.XPATH, f'/html/body/div[4]/div[2]/div/div').text
    info = info.split("#")
    print(len(info))
    for i in range(1, len(info)):
        data_dict = {}
        description = ""
        ele_info = info[i]
        fullName = ele_info.split("\n", 1)[0].split(":", 1)[1].strip()
        ele_info = ele_info.split("\n", 1)[1]
        description = ele_info.split("Services", 1)[0]
        ele_info = ele_info.split("Services", 1)[1]
        services = ele_info.split("Products", 1)[0]
        ele_info = ele_info.split("Products", 1)[1]
        products = ele_info.split(fullName, 1)[0]
        ele_info = ele_info.split(fullName, 1)[1]
        totalAssets = ele_info.split("total assets were")[1].split(", providing")[0].strip()
        marketShare = ele_info.split("market share of")[1].split(". In", 1)[0].strip()
        netIncome = ele_info.split("net income was")[1].split(".", 1)[0].strip()
        ele_info = ele_info.replace("\n", " ")
        summary = fullName + ele_info

        fullName = fullName.replace(".", "")
        products = products.replace("\n", "; ").replace("; ", "", 1)
        services = services.replace("\n", "; ").replace("; ", "", 1)
        summary = summary.replace("See Also List of Banks in Albania", "")
        print(fullName)
        print(description)
        print(services)
        print(products)
        print(totalAssets)
        print(marketShare)
        print(netIncome)
        print(summary)
        print("*"*50)
        if fullName:
            data_dict['fullName'] = fullName
        if description:
            data_dict['description'] = description
        if services:
            data_dict['services'] = services
        if products:
            data_dict['products'] = products
        if totalAssets:
            data_dict['totalAssets'] = totalAssets
        if marketShare:
            data_dict['marketShare'] = marketShare
        if netIncome:
            data_dict['netIncome'] = netIncome
        if summary:
            data_dict['summary'] = summary
        data_list.append(data_dict)
    driver.quit()
    return data_list


# In[33]:


if __name__ == '__main__':
    data_list = get_data("add_slug_name")
    to_json(data_list)


# In[ ]:




