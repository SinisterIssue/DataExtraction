#!/usr/bin/env python
# coding: utf-8

# In[25]:


from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import json
import re
from deep_translator import GoogleTranslator


# In[26]:


def to_json(data):
    """
    This function takes list of dictionary as Input and 
    then Creates a JSON file in which Input data is stored
    """
    with open("data_dict.json", "w") as outfile:
        json.dump(data, outfile,indent=4)
        outfile.close()


# In[27]:


def get_data(slug_name):
    data_list = []
    url = "https://en.wikipedia.org/wiki/Category:People_stripped_of_honorary_degrees"
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized") 
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--log-level=3")
    translator = GoogleTranslator(target='english')
    driver = webdriver.Chrome(options=options)
    driver.get(url)
    list1 = driver.find_elements(By.XPATH, f'//div[5]/div[2]/div/div/div/div/h3')
    for i in range(1, len(list1)+1):
        list2 = driver.find_elements(By.XPATH, f'//div[5]/div[2]/div/div/div/div[{i}]/ul/li/a')
        for j in range(1, len(list2)+1):
            familyInfo =""
            educationInfo = ""
            additionalInfo = ""
            fullAddress =""
            summary = ""
            alias = ""
            image = ""
            dob= ""
            age = ""
            height=  ""
            weight = ""
            achievements =""
            politicalParty = ""
            careerInfoDesignation =""
            website =""
            nationality =""
            data_dict ={}
            fullName = driver.find_element(By.XPATH, f'//div[5]/div[2]/div/div/div/div[{i}]/ul/li[{j}]/a').text
            print(fullName)
            driver.find_element(By.XPATH, f'//div[5]/div[2]/div/div/div/div[{i}]/ul/li[{j}]/a').click()
            time.sleep(2)
            try:
                image = driver.find_element(By.XPATH, f'/html/body/div[3]/div[3]/div[5]/div[1]/table[@class="infobox vcard"]/tbody/tr[1]/td[@class="infobox-image"]/a/img').get_attribute("src")
                print(image)
            except:
                try:
                    image = driver.find_element(By.XPATH, f'/html/body/div[3]/div[3]/div[5]/div[1]/table[@class="infobox vcard"]/tbody/tr[3]/td[@class="infobox-image"]/a/img').get_attribute("src")
                    print(image)
                except:
                    try:
                        image = driver.find_element(By.XPATH, f'/html/body/div[3]/div[3]/div[5]/div[1]/table[@class="infobox biography vcard"]/tbody/tr[2]/td/a/img').get_attribute('src')
                        print(image)
                    except:
                        try:
                            image = driver.find_element(By.XPATH, f'/html/body/div[3]/div[3]/div[5]/div[1]/table[@class="infobox vcard"]/tbody/tr[2]/td/a/img').get_attribute('src')
                            print(image)
                        except:
                            try:
                                image = driver.find_element(By.XPATH, f'/html/body/div[3]/div[3]/div[5]/div[1]/div[3]/div/a/img').get_attribute('src')
                                print(image)
                            except:
                                pass
            try:
                list3 = driver.find_elements(By.XPATH, f'/html/body/div[3]/div[3]/div[5]/div[1]/table[@class="infobox biography vcard"]/tbody/tr')
                if len(list3)>0:
                    for k in range(1, len(list3)+1):
                        print("top")
                        heading = driver.find_element(By.XPATH, f'/html/body/div[3]/div[3]/div[5]/div[1]/table[@class="infobox biography vcard"]/tbody/tr[{k}]').text
                        if "Full name" in heading:
                            fullName = heading.split("Full name")[1].strip()
                            print(fullName)
                        if "Nickname" in heading:
                            alias = heading.split("Nickname")[1].replace("\n", "; ").strip()
                            print(alias)
                        if "Born" in heading:
                            born = heading.split("\n")
                            if len(born) ==3:
                                if "age" not in heading:
                                    dob = born[1]
                                    placeOfBirthCity = born[2]
                                if "age" in heading:
                                    dob= born[1]
                                    age = dob.split("age")[1].replace(")", "").strip()
                                    dob = dob.split("(")[0].strip()
                                    placeOfBirthCity = born[2].strip()
                            if len(born)==2:
                                if "age" not in heading:
                                    dob = born[0]
                                    placeOfBirthCity = born[1]
                                if "age" in heading:
                                    dob= born[0]
                                    age = dob.split("age")[1].replace(")", "").strip()
                                    dob = dob.split("(")[0].strip()
                                    placeOfBirthCity = born[1].strip()
                            if len(born)==1:
                                dob = heading.split("Born")[1].strip()
                                age = dob.split("age")[1].replace(")", "").strip()
                                dob = dob.split("(")[0].strip()       
                        if "Height" in heading:
                            height= heading.split("Height")[1].strip()
                        if "Weight" in heading:
                            weight = heading.split("Weight")[1].strip()
                        if "Major wins" in heading:
                            achievements = driver.find_element(By.XPATH, f'/html/body/div[3]/div[3]/div[5]/div[1]/table[1]/tbody/tr[{k+1}]').text
                        if "Political party" in heading:
                            politicalParty = heading.split("Political party")[1].replace("\n", "").strip()
                        if "Spouse(s)" in heading:
                            spouse = heading.split("Spouse(s)")[1].replace("\n", "").strip()
                            familyInfo = "Spouse: " + spouse + "; " + familyInfo
                        if "Children" in heading:
                            children = heading.split("Children")[1].replace("\n", "").strip()
                            familyInfo = "Children: " + children + "; "+ familyInfo
                        if "Parent(s)" in heading:
                            parent = heading.split("Parent(s)")[1].replace("\n", "; ").strip()
                            familyInfo = "Parents: "+ parent + "; " + familyInfo
                        if "Relatives" in heading:
                            relative = heading.split("Relatives")[1].replace("\n", "; ").strip()
                            familyInfo = "Relatives: " + relative + "; " + familyInfo
                        if "Residence(s)" in heading:
                            fullAddress = heading.split("Residence(s)")[1].strip()
                        if "Education" in heading:
                            educationInfo = heading.split("Education")[1].strip()
                        if "Awards" in heading:
                            achievements = heading.split("Awards")[1].replace("\n", "; ").strip()
                        if "Alma mater" in heading:
                            educationInfo = heading.split("Alma mater")[1].replace("\n", "; ").strip()
                        if "Other political\naffiliations" in heading:
                            politicalParty = politicalParty + "; " + heading.split("affiliations")[1].replace("\n", "; ").strip()
                        if "Website" in heading:
                            website = heading.split("Website")[1].replace("\n", "; ").strip()
                        if "Citizenship" in heading:
                            nationality = heading.split("Citizenship")[1].strip()
                        if "Occupation" in heading:
                            careerInfoDesignation = heading.split("Occupation")[1].replace("\n", "; ").strip()
                        if "Died" in heading:
                            died = heading.split("Died")[1].replace("\n", ",").strip()
                            importantDates = "Died: " + died
                        if "Other names" in heading:
                            alias = heading.split("Other names")[1].replace("\n", "; ").strip()
                        if "Nationality" in heading:
                            nationality = heading.split("Nationality")[1].strip()
            except Exception as e:
                print(e)
                pass
            try:
                list3 = driver.find_elements(By.XPATH, f'/html/body/div[3]/div[3]/div[5]/div[1]/table[@class="infobox vcard"]/tbody/tr')
                if len(list3)>0:
                    for k in range(1, len(list3)+1):
                        print("bot")
                        heading = driver.find_element(By.XPATH, f'/html/body/div[3]/div[3]/div[5]/div[1]/table[@class="infobox vcard"]/tbody/tr[{k}]').text
                        if "Full name" in heading:
                            fullName = heading.split("Full name")[1].strip()
                            print(fullName)
                        if "Nickname" in heading:
                            alias = heading.split("Nickname")[1].replace("\n", "; ").strip()
                            print(alias)
                        if "Born" in heading:
                            born = heading.split("\n")
                            if len(born)==3:
                                if "age" not in heading:
                                    dob = born[1]
                                    placeOfBirthCity = born[2]
                                if "age" in heading:
                                    dob= born[1]
                                    age = dob.split("age")[1].replace(")", "").strip()
                                    dob = dob.split("(")[0].strip()
                                    placeOfBirthCity = born[2].strip()
                            if len(born)==2:
                                if "age" not in heading:
                                    dob = born[0]
                                    placeOfBirthCity = born[1]
                                if "age" in heading:
                                    dob= born[0]
                                    age = dob.split("age")[1].replace(")", "").strip()
                                    dob = dob.split("(")[0].strip()
                                    placeOfBirthCity = born[1].strip()
                            if len(born)==1:
                                dob = heading.split("Born")[1].strip()
                                try:
                                    age = dob.split("age")[1].replace(")", "").strip()
                                    dob = dob.split("(")[0].strip()
                                except:
                                    pass
                        if "Height" in heading:
                            height= heading.split("Height")[1].strip()
                        if "Weight" in heading:
                            weight = heading.split("Weight")[1].strip()
                        if "Major wins" in heading:
                            achievements = driver.find_element(By.XPATH, f'/html/body/div[3]/div[3]/div[5]/div[1]/table[1]/tbody/tr[{k+1}]').text
                        if "Political party" in heading:
                            politicalParty = heading.split("Political party")[1].replace("\n", "").strip()
                        if "Spouse(s)" in heading:
                            spouse = heading.split("Spouse(s)")[1].replace("\n", "").strip()
                            familyInfo = "Spouse: " + spouse + "; " + familyInfo
                        if "Children" in heading:
                            children = heading.split("Children")[1].replace("\n", "").strip()
                            familyInfo = "Children: " + children + "; "+ familyInfo
                        if "Parent(s)" in heading:
                            parent = heading.split("Parent(s)")[1].replace("\n", "; ").strip()
                            familyInfo = "Parents: "+ parent + "; " + familyInfo
                        if "Relatives" in heading:
                            relative = heading.split("Relatives")[1].replace("\n", "; ").strip()
                            familyInfo = "Relatives: " + relative + "; " + familyInfo
                        if "Residence(s)" in heading:
                            fullAddress = heading.split("Residence(s)")[1].strip()
                        if "Education" in heading:
                            educationInfo = heading.split("Education")[1].strip()
                        if "Awards" in heading:
                            achievements = heading.split("Awards")[1].replace("\n", "; ").strip()
                        if "Alma mater" in heading:
                            educationInfo = heading.split("Alma mater")[1].replace("\n", "; ").strip()
                        if "Other political\naffiliations" in heading:
                            politicalParty = politicalParty + "; " + heading.split("affiliations")[1].replace("\n", "; ").strip()
                        if "Website" in heading:
                            website = heading.split("Website")[1].replace("\n", "; ").strip()
                        if "Citizenship" in heading:
                            nationality = heading.split("Citizenship")[1].strip()
                        if "Occupation" in heading:
                            careerInfoDesignation = heading.split("Occupation")[1].replace("\n", "; ").strip()
                        if "Died" in heading:
                            died = heading.split("Died")[1].replace("\n", ",").strip()
                            importantDates = "Died: " + died
                        if "Other names" in heading:
                            alias = heading.split("Other names")[1].replace("\n", "; ").strip()
                        if "Nationality" in heading:
                            nationality = heading.split("Nationality")[1].strip()

            except:
                pass
            list4 = driver.find_elements(By.XPATH, f'/html/body/div[3]/div[3]/div[5]/div[1]/p')
            for l in range(1, len(list4)+1):
                if l in range(1, 4):
                    summary = driver.find_element(By.XPATH, f'/html/body/div[3]/div[3]/div[5]/div[1]/p[{l}]').text + " " +summary
                else:
                    additionalInfo = driver.find_element(By.XPATH, f'/html/body/div[3]/div[3]/div[5]/div[1]/p[{l}]').text + " "+ additionalInfo

            summary = re.sub(r'\[[0-9]*\]','',summary)
            additionalInfo = re.sub(r'\[[0-9]*\]','',additionalInfo)
            height = re.sub(r'\[[0-9]*\]','',height)
            weight = re.sub(r'\[[0-9]*\]','',weight)
            familyInfo = re.sub(r'\[[0-9]*\]','',familyInfo)
            educationInfo = re.sub(r'\[[0-9]*\]','',educationInfo)
            nationality = re.sub(r'\[[0-9]*\]','',nationality)
            alias = re.sub(r'\[[0-9]*\]','',alias)
    #         netIncome = re.sub(r'\[[0-9]*\]','',netIncome)
    #         operatingIncome = re.sub(r'\[[0-9]*\]','',operatingIncome)
            driver.back()
            if fullName:
                data_dict['fullName'] = fullName
            if image:
                data_dict['image'] = image
            if alias:
                data_dict['alias'] = alias
            if dob:
                data_dict['dob'] = dob
            if age:
                data_dict['age'] = age
            if placeOfBirthCity:
                data_dict['placeOfBirthCity'] = placeOfBirthCity
            if nationality:
                data_dict['nationality'] = nationality
            if fullAddress:
                data_dict['fullAddress'] = fullAddress
            if familyInfo:
                data_dict['familyInfo'] = familyInfo
            if educationInfo:
                data_dict['educationInfo'] = educationInfo
            if careerInfoDesignation:
                data_dict['careerInfoDesignation'] = careerInfoDesignation
            if politicalParty:
                data_dict['politicalParty'] = politicalParty
            if height:
                data_dict['height'] = height
            if weight:
                data_dict['weight'] = weight
            if achievements:
                data_dict['achievements'] = achievements
            if website:
                data_dict['website'] = website
            if additionalInfo:
                data_dict['additionalInfo'] = additionalInfo
            if summary:
                data_dict['summary'] = summary
            data_list.append(data_dict)
    driver.quit()
    return data_list


# In[28]:


if __name__ == '__main__':
    data_list = get_data("add_slug_name")
    to_json(data_list)


# In[ ]:




