#!/usr/bin/env python
# coding: utf-8

# In[8]:


from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import json
import requests
import hashlib
import re
from PyPDF2 import PdfFileReader
from six.moves.urllib.request import urlopen
import io


# In[9]:


def get_hash_of_html(html_string):
    hash_object = hashlib.md5(html_string.encode('utf-8'))
    hash_of_html = hash_object.hexdigest()
    return hash_of_html


# In[10]:


def get_text(bbox,reader,page_img):
    new = page_img.crop(bbox)
    bounds = reader.readtext(np.array(new), paragraph= True, x_ths = 2.0)
    lst = [bounds[i][1] for i in range(len(bounds))]
    return lst


# In[11]:


def to_json(dictionary):
    hash_obj = json.dumps(dictionary)
    with open("dictionary.json", "w") as ts:
        json.dump(dictionary, ts,indent=4)
#         ts.write(hash_obj)


# In[12]:


data_list = []
link = 'https://assets.publishing.service.gov.uk/government/uploads/system/uploads/attachment_data/file/1088191/Cyber.pdf'
user_agent = "scrapping_script/1.0"
headers = {'User-Agent': user_agent}
r = requests.get(link, headers=headers, stream = True)


# In[111]:


def get_data(slug_name):
    file = io.BytesIO(r.content)
    fileReader = PyPDF2.PdfFileReader(file)

    total = ""
    pages = fileReader.numPages
    for page in range(0, pages):
        page = fileReader.pages[page]
        page_content = page.extractText()
        total = total + page_content
    # print(total)
    total_ind = total.split("INDIVIDUALS")[1].split("ENTITIES")[0]
    total_org = total.split("ENTITIES")[1]
    total_ind = total_ind.split("Name 6:")
    for i in range(1, len(total_ind)):
        data_dict = {}
        identifierType = ""
        alias =""
        addressLine1 = ""
        fullName = total_ind[i].split(".", 1)[0].replace("n/a", "").strip()
        fullName = re.sub(r"[0-9]","",fullName)
        fullName = fullName.replace(":", "").replace("  ", " ").strip()
        print(fullName)
        total_ind[i] = total_ind[i].split(".", 1)[1]
        info = total_ind[i]
        dob = info.split("DOB:")[1].split("POB:")[0].split(".")[0].replace("(1) ", "").strip()
        print(dob)
    #     print(info)
        try:
            placeOfBirthCity = info.split("POB:")[1].split("Nationality",1)[0].split("a.k.a")[0].strip()
            print(placeOfBirthCity)
        except:
            pass
        try:
            nationality = info.split("Nationality:")[1].split("Position:")[0].strip().split(" ", 1)[0]
            print(nationality)
        except:
            pass
        try:
            alias = info.split("a.k.a:")[1].split("Nationality")[0].strip()
            print(alias)
        except:
            pass
        try:
            careerInfoDesignation = info.split("Position:")[1].split("Other Information:")[0].replace("\n", "; ").replace("; ", " ").strip()
            print(careerInfoDesignation)
        except:
            pass
        try:
            addressLine1 = info.split("Address:")[1].split(".",1)[0].replace("\n", " ").strip()
            print(addressLine1)
        except:
            pass
        try:
            passport = info.split("Passport Number:")[1].split("Address")[0].strip()
            identifierType = "Passport Number: " + passport
            print(identifierType)
        except:
            pass
        try:
            additionalInfo = info.split("Other Information:")[1].split("Listed on:")[0].replace("\n", "").strip()
            gender = additionalInfo.split("(Gender):")[1]
            print(gender)
            additionalInfo = additionalInfo.split("(Gender):")[0]
            print(additionalInfo)
        except:
            pass
        try:
            listedOn = info.split("Listed on:")[1].split("UK Sanctions List Date Designated")[0].strip()
            print(listedOn)
            listDate = info.split("UK Sanctions List Date Designated:")[1].split("Updated")[0].strip()
            importantDates = "UK Sanctions List Date Designated: " + listDate.replace("Last", "").replace("\n", "")
            print(importantDates)
            lastUpdatedAt = info.split("Updated:")[1].split("Group ID")[0].strip()
            print(lastUpdatedAt)
            groupID = info.split("Group ID:")[1].split(".", 1)[0].strip()
            identifierType = "Group ID: " + groupID + "; " + identifierType
            print(identifierType)
        except:
            pass
        summary = fullName + " is present in CONSOLIDATED LIST OF FINANCIAL SANCTIONS TARGETS IN THE UK, Regime: Cyber"
        entityType = "Individual"
        print("*"*50)
        if fullName:
            data_dict['fullName'] = fullName
        if dob:
            data_dict['dob'] = dob
        if entityType:
            data_dict['entityType'] = entityType
        if placeOfBirthCity:
            data_dict['placeOfBirthCity'] = placeOfBirthCity
        if nationality:
            data_dict['nationality'] = nationality
        if alias:
            data_dict['alias'] = alias
        if careerInfoDesignation:
            data_dict['careerInfoDesignation'] = careerInfoDesignation
        if addressLine1:
            data_dict['addressLine1'] = addressLine1
        if identifierType:
            data_dict['identifierType'] = identifierType
        if gender:
            data_dict['gender'] = gender
        if additionalInfo:
            data_dict['additionalInfo'] = additionalInfo
        if listedOn:
            data_dict['listedOn'] = listedOn
        if importantDates:
            data_dict['importantDates'] = importantDates
        if lastUpdatedAt:
            data_dict['lastUpdatedAt'] = lastUpdatedAt
        if summary:
            data_dict['summary'] = summary
        data_list.append(data_dict)

    total_org = total_org.split("Organisation Name:")
    for j in range(1, len(total_org)):
        data_dict2 = {}
        groupID = ""
        identifierType =""
        info = total_org[j]
        fullName = info.split("a.k.a", 1)[0].replace("\n", " ").strip()
        print(fullName)
        alias = info.split("a.k.a:")[1].split("Address")[0].split("Other Information")[0].strip()
        print(alias)
        try:
            addressLine1 = info.split("Address:")[1].split("Other Information")[0].replace("\n", "").strip()
            print(addressLine1)
        except:
            pass
        additionalInfo = info.split("Other Information:")[1].split("Listed on")[0].split("Listedon")[0].replace("\n", "").strip()
        print(additionalInfo)
        listedOn = info.split("Listed")[1].split("UK Sanctions List Date Designated")[0].strip()
        listedOn = listedOn.split(":")[1].strip()
        print(listedOn)
        listDate = info.split("UK Sanctions List Date Designated:")[1].split("Updated")[0].strip()
        importantDates = "UK Sanctions List Date Designated: " + listDate.replace("Last", "").replace("\n", "")
        print(importantDates)
        lastUpdatedAt = info.split("Updated:")[1].split("Group ID")[0].strip()
        print(lastUpdatedAt)
        groupID = info.split("Group ID:")[1].split(".", 1)[0].strip()
        identifierType = "Group ID: " + groupID + "; " + identifierType
        print(identifierType)
        summary = fullName + " is present in CONSOLIDATED LIST OF FINANCIAL SANCTIONS TARGETS IN THE UK, Regime: Cyber"
        entityType = "Company"
        print("*"*50)
        if fullName:
            data_dict2['fullName'] = fullName
        if entityType:
            data_dict2['entityType'] = entityType
        if alias:
            data_dict2['alias'] = alias
        if addressLine1:
            data_dict2['addressLine1'] = addressLine1
        if identifierType:
            data_dict2['identifierType'] = identifierType
        if additionalInfo:
            data_dict2['additionalInfo'] = additionalInfo
        if listedOn:
            data_dict2['listedOn'] = listedOn
        if importantDates:
            data_dict2['importantDates'] = importantDates
        if lastUpdatedAt:
            data_dict2['lastUpdatedAt'] = lastUpdatedAt
        if summary:
            data_dict2['summary'] = summary
        data_list.append(data_dict2)
    return data_list


# In[112]:


if __name__ == "__main__":
    data_list = get_data('add-slug-here')
    to_json(data_list)


# In[ ]:




