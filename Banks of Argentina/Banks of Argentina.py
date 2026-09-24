#!/usr/bin/env python
# coding: utf-8

# In[23]:


from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import json
import re
from deep_translator import GoogleTranslator


# In[24]:


def to_json(data):
    """
    This function takes list of dictionary as Input and 
    then Creates a JSON file in which Input data is stored
    """
    with open("data_dict.json", "w") as outfile:
        json.dump(data, outfile,indent=4)
        outfile.close()


# In[25]:


def get_data(slug_name):    
    data_list = []
    url = "https://en.wikipedia.org/wiki/Category:Banks_of_Argentina"
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized") 
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--log-level=3")
    translator = GoogleTranslator(target='english')
    driver = webdriver.Chrome(options=options)
    driver.get(url)
    list1 = driver.find_elements(By.XPATH, f'//div[2]/div[2]/div/div/div/h3')
    for i in range(1, len(list1)+1):
        list2 = driver.find_elements(By.XPATH, f'//div[5]/div[2]/div[2]/div/div/div[{i}]/ul/li')
        for j in range(1, len(list2)+1):
            fullName = driver.find_element(By.XPATH, f'//div[5]/div[2]/div[2]/div/div/div[{i}]/ul/li[{j}]').text
            print(fullName)
            driver.find_element(By.XPATH, f'//div[5]/div[2]/div[2]/div/div/div[{i}]/ul/li[{j}]/a').click()
            time.sleep(2)
            data_dict={}
            additionalInfo = ""
            rawName = ""
            alias=""
            types = ""
            tradedAs= ""
            incorporateDate = ""
            industry = ""
            addressLine1 = ""
            keyPeople = ""
            services = ""
            revenue = ""
            operatingIncome = ""
            netIncome =""
            totalAssets =""
            totalEquity = ""
            owner =""
            nosOfEmployes = ""
            subsidiaries = ""
            website = ""
            rating = ""
            summary = ""
            currency = ""
            reserves= ""
            try:
                list3 = driver.find_elements(By.XPATH, f'/html/body/div[3]/div[3]/div[5]/div[1]/table[@class="infobox vcard"]/tbody/tr')
                for k in range(1, len(list3)+1):
                    heading = driver.find_element(By.XPATH, f'/html/body/div[3]/div[3]/div[5]/div[1]/table[@class="infobox vcard"]/tbody/tr[{k}]').text
                    if "Native name" in heading:
                        rawName = driver.find_element(By.XPATH, f'/html/body/div[3]/div[3]/div[5]/div[1]/table[@class="infobox vcard"]/tbody/tr[{k}]').text
                        rawName = rawName.split("Native name")[1].strip()
                        print(rawName)
                    elif "Formerly" in heading:
                        alias = driver.find_element(By.XPATH, f'/html/body/div[3]/div[3]/div[5]/div[1]/table[@class="infobox vcard"]/tbody/tr[{k}]').text
                        alias = alias.split("Formerly")[1].strip()
                    elif "Type" in heading:
                        types  = driver.find_element(By.XPATH, f'/html/body/div[3]/div[3]/div[5]/div[1]/table[@class="infobox vcard"]/tbody/tr[{k}]').text
                        types = types.split("Type")[1].strip()
                    elif "Traded as" in heading:
                        tradedAs = driver.find_element(By.XPATH, f'/html/body/div[3]/div[3]/div[5]/div[1]/table[@class="infobox vcard"]/tbody/tr[{k}]').text
                        tradedAs = tradedAs.split("Traded as")[1].replace("\n", "; ").strip()
                    elif "Industry" in heading:
                        industry = driver.find_element(By.XPATH, f'/html/body/div[3]/div[3]/div[5]/div[1]/table[@class="infobox vcard"]/tbody/tr[{k}]').text
                        industry = industry.split("Industry")[1].replace("\n", "; ").strip()
                    elif "Founded" in heading:
                        incorporateDate = driver.find_element(By.XPATH, f'/html/body/div[3]/div[3]/div[5]/div[1]/table[@class="infobox vcard"]/tbody/tr[{k}]').text
                        incorporateDate = incorporateDate.split("Founded")[1].replace("\n", " ").strip()
                    elif "Headquarters" in heading:
                        addressLine1 = driver.find_element(By.XPATH, f'/html/body/div[3]/div[3]/div[5]/div[1]/table[@class="infobox vcard"]/tbody/tr[{k}]').text
                        addressLine1 = addressLine1.split("Headquarters")[1].strip()
                    elif "Key people" in heading:
                        keyPeople = driver.find_element(By.XPATH, f'/html/body/div[3]/div[3]/div[5]/div[1]/table[@class="infobox vcard"]/tbody/tr[{k}]').text
                        keyPeople = keyPeople.split("Key people")[1].replace("\n", " ").replace("[2]", "").replace(")", "); ").strip()
                    elif "Products" in heading:
                        services = driver.find_element(By.XPATH, f'/html/body/div[3]/div[3]/div[5]/div[1]/table[@class="infobox vcard"]/tbody/tr[{k}]').text
                        services = services.split("Products")[1].replace("\n", " ")
                    elif "Revenue" in heading:
                        revenue = driver.find_element(By.XPATH, f'/html/body/div[3]/div[3]/div[5]/div[1]/table[@class="infobox vcard"]/tbody/tr[{k}]').text
                        revenue = revenue.split("Revenue")[1].strip()
                    elif "Operating income" in heading:
                        operatingIncome = driver.find_element(By.XPATH, f'/html/body/div[3]/div[3]/div[5]/div[1]/table[@class="infobox vcard"]/tbody/tr[{k}]').text
                        operatingIncome = operatingIncome.split("Operating income")[1].strip()
                    elif "Net income" in heading:
                        netIncome = driver.find_element(By.XPATH, f'/html/body/div[3]/div[3]/div[5]/div[1]/table[@class="infobox vcard"]/tbody/tr[{k}]').text
                        netIncome = netIncome.split("Net income")[1].strip()
                    elif "Total assets" in heading:
                        totalAssets = driver.find_element(By.XPATH, f'/html/body/div[3]/div[3]/div[5]/div[1]/table[@class="infobox vcard"]/tbody/tr[{k}]').text
                        totalAssets = totalAssets.split("Total assets")[1].strip()
                    elif "Total equity" in heading:
                        totalEquity = driver.find_element(By.XPATH, f'/html/body/div[3]/div[3]/div[5]/div[1]/table[@class="infobox vcard"]/tbody/tr[{k}]').text
                        totalEquity = totalEquity.split("Total equity")[1].strip()
                    elif "Owner" in heading:
                        owner = driver.find_element(By.XPATH, f'/html/body/div[3]/div[3]/div[5]/div[1]/table[@class="infobox vcard"]/tbody/tr[{k}]').text
                        owner = owner.split("Owner")[1].replace("\n", "; ").replace("ship", "", 1).strip()
                    elif "Number of employees" in heading:
                        nosOfEmployes = driver.find_element(By.XPATH, f'/html/body/div[3]/div[3]/div[5]/div[1]/table[@class="infobox vcard"]/tbody/tr[{k}]').text
                        nosOfEmployes = nosOfEmployes.split("Number of employees")[1].strip()
                    elif "Subsidiaries" in heading:
                        subsidiaries = driver.find_element(By.XPATH, f'/html/body/div[3]/div[3]/div[5]/div[1]/table[@class="infobox vcard"]/tbody/tr[{k}]').text
                        subsidiaries = subsidiaries.split("Subsidiaries")[1].replace("\n", ", ").strip()
                    elif "Rating" in heading:
                        rating  = driver.find_element(By.XPATH, f'/html/body/div[3]/div[3]/div[5]/div[1]/table[@class="infobox vcard"]/tbody/tr[{k}]').text
                        rating = rating.split("Rating")[1].strip()
                    elif "Website" in heading:
                        website = driver.find_element(By.XPATH, f'/html/body/div[3]/div[3]/div[5]/div[1]/table[@class="infobox vcard"]/tbody/tr[{k}]').text
                        website = website.split("Website")[1].replace("\n", "; ").strip()
                    elif "Established" in heading:
                        incorporateDate = driver.find_element(By.XPATH, f'/html/body/div[3]/div[3]/div[5]/div[1]/table[@class="infobox vcard"]/tbody/tr[{k}]').text
                        incorporateDate = incorporateDate.split("Established")[1].strip()
                    elif "Ownership" in heading:
                        owner = driver.find_element(By.XPATH, f'/html/body/div[3]/div[3]/div[5]/div[1]/table[@class="infobox vcard"]/tbody/tr[{k}]').text
                        owner = owner.split("Ownership")[1].strip()
                    elif "Currency" in heading:
                        currency = driver.find_element(By.XPATH, f'/html/body/div[3]/div[3]/div[5]/div[1]/table[@class="infobox vcard"]/tbody/tr[{k}]').text
                        currency = currency.split("Currency")[1].strip()
                    elif "Reserves" in heading:
                        reserves = driver.find_element(By.XPATH, f'/html/body/div[3]/div[3]/div[5]/div[1]/table[@class="infobox vcard"]/tbody/tr[{k}]').text
                        reserves = reserves.split("Reserves")[1].replace("[1]", "").strip()
                    elif "President" in heading:
                        keyPeople = driver.find_element(By.XPATH, f'/html/body/div[3]/div[3]/div[5]/div[1]/table[@class="infobox vcard"]/tbody/tr[{k}]').text + "; " + keyPeople
            except:
                pass
            try:
                list4 = driver.find_elements(By.XPATH, f'/html/body/div[3]/div[3]/div[5]/div[1]/p')
                for l in range(1, len(list4)+1):
                    if l in range(1, 4):
                        summary = driver.find_element(By.XPATH, f'/html/body/div[3]/div[3]/div[5]/div[1]/p[{l}]').text + " " +summary
                    else:
                        additionalInfo = driver.find_element(By.XPATH, f'/html/body/div[3]/div[3]/div[5]/div[1]/p[{l}]').text + " "+ additionalInfo
            except:
                pass
            summary = re.sub(r'\[[0-9]*\]','',summary)
            additionalInfo = re.sub(r'\[[0-9]*\]','',additionalInfo)
            owner = re.sub(r'\[[0-9]*\]','',owner)
            rating = re.sub(r'\[[0-9]*\]','',rating)
            nosOfEmployes = re.sub(r'\[[0-9]*\]','',nosOfEmployes)
            revenue = re.sub(r'\[[0-9]*\]','',revenue)
            totalEquity = re.sub(r'\[[0-9]*\]','',totalEquity)
            totalAssets = re.sub(r'\[[0-9]*\]','',totalAssets)
            netIncome = re.sub(r'\[[0-9]*\]','',netIncome)
            operatingIncome = re.sub(r'\[[0-9]*\]','',operatingIncome)
            try:
                additionalInfo = additionalInfo.split("\u2033W")[1].strip()
            except:
                pass
            if fullName:
                data_dict['fullName'] = fullName
            if rawName:
                data_dict['rawName'] = rawName
            if alias:
                data_dict['alias'] = alias
            if types:
                data_dict['type'] = types
            if tradedAs:
                data_dict['tradedAs'] = tradedAs
            if incorporateDate:
                data_dict['incorporateDate'] = incorporateDate
            if addressLine1:
                data_dict['addressLine1'] = addressLine1
            if industry:
                data_dict['industry'] = industry
            if services:
                data_dict['services'] = services
            if keyPeople:
                data_dict['keyPeople'] = keyPeople
            if owner:
                data_dict['owner'] = owner
            if reserves:
                data_dict['reserves'] = reserves
            if currency:
                data_dict['currency'] = currency
            if operatingIncome:
                data_dict['operatingIncome'] = operatingIncome
            if netIncome:
                data_dict['netIncome'] = netIncome
            if totalAssets:
                data_dict['totalAssets'] = totalAssets
            if totalEquity:
                data_dict['totalEquity'] = totalEquity
            if revenue:
                data_dict['revenue'] = revenue
            if subsidiaries:
                data_dict['subsidiaries'] = subsidiaries
            if nosOfEmployes:
                data_dict['nosOfEmployes'] = nosOfEmployes
            if rating:
                data_dict['rating'] = rating
            if website:
                data_dict['website'] = website
            if additionalInfo:
                data_dict['additionalInfo'] = additionalInfo
            if summary:
                data_dict['summary'] = summary
            data_list.append(data_dict)
            driver.back()
    driver.quit()
    return data_list


# In[26]:


if __name__ == '__main__':
    data_list = get_data("add_slug_name")
    to_json(data_list)


# In[ ]:




