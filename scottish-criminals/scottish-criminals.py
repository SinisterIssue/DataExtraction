#!/usr/bin/env python
# coding: utf-8

# In[48]:


from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import json
import re


# In[49]:


def to_json(data):
    """
    This function takes list of dictionary as Input and 
    then Creates a JSON file in which Input data is stored
    """
    with open("data_dict.json", "w") as outfile:
        json.dump(data, outfile,indent=4)
        outfile.close()


# In[50]:


def get_data(slug_name): 
    data_list = []
    url = "https://www.thefamouspeople.com/scottish-criminals.php"
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized") 
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--log-level=3")
    driver = webdriver.Chrome(options=options)
    driver.get(url)
    list1 = driver.find_elements(By.XPATH, f'/html/body/div[6]/div/div/div[3]/div[5]/div/article/div[1]/div[1]/div[2]/a')
    for i in range(1, len(list1)*4):
        data_dict = {}
        fullName = ""
        placeOfBirthCity= ""
        image=  ""
        dob =""
        importantDates = ""
        identifierType = ""
        types= ""
        familyInfo =""
        crimeDescription = ""
        additionalInfo = ""
        alias = ""
        educationInfo = ""
        careerInfoDesignation  =""
        country = ""
        nationality = ""
        description = ""

        try:
            link = driver.find_element(By.XPATH, f'/html/body/div[6]/div/div/div[3]/div[5]/div[{i}]/article/div[1]/div[1]/div[2]/a').get_attribute("href")
            try:
                image = driver.find_element(By.XPATH, f'/html/body/div[6]/div/div/div[3]/div[5]/div[{i}]/article/div[3]/img').get_attribute("src")
                print(image)
                info = driver.find_element(By.XPATH, f'/html/body/div[6]/div/div/div[3]/div[5]/div[{i}]/article/div[4]').text
    #             print(info)
                if "Birthplace" in info:
                    placeOfBirthCity = info.split("Birthplace:")[1].split("\n")[0].strip()
                    print(placeOfBirthCity)
                if "Birthdate" in info:
                    dob = info.split("Birthdate:")[1].split("\n")[0].strip()
                    print(dob)
                if "Died" in info:
                    importantDates = "Died: " + info.split("Died:")[1].split("\n")[0].strip()
                    print(importantDates)
                if "Sun Sign" in info:
                    identifierType = "Sun Sign: " + info.split("Sun Sign:")[1].split("\n")[0].strip()
                    print(identifierType)
                types = driver.find_element(By.XPATH, f'/html/body/div[6]/div/div/div[3]/div[5]/div[{i}]/article/div[1]/div[1]/div[2]/div').text
            except:
                pass
            driver.execute_script("window.open('');")
            driver.switch_to.window(driver.window_handles[1])
            driver.get(link)
            time.sleep(2)
            if i==1:
                image = driver.find_element(By.XPATH, f'/html/body/div[6]/div/div[2]/div[1]/div/div/a/img').get_attribute("src")
                print(image)
                fullName = "Alexander Bean"
                alias = "Sawney Bean"
                placeOfBirthCity = driver.find_element(By.XPATH, f'/html/body/div[6]/div/div[2]/div[2]/p').text
                placeOfBirthCity =  placeOfBirthCity.split(":")[1].strip()
                description = driver.find_element(By.XPATH, f'/html/body/div[6]/div/div[1]/div[7]').text
                familyInfo = driver.find_element(By.XPATH, f'/html/body/div[10]/div/div[2]/div[14]/div[1]/div[3]/div').text
    #             print(familyInfo)
                additionalInfo = driver.find_element(By.XPATH, f'/html/body/div[10]/div/div[2]/div[14]/div[4]').text.replace("\n", "; ").replace("Career; ", "")
    #             print(careerInfo)
                types = "criminal"
            elif i==14:
                dob = "January 5, 1942"
                importantDates = "Died: August 15, 1963"
                placeOfBirthCity = "Aberdeen, United Kingdom"
                description = driver.find_element(By.XPATH, f'/html/body/div[3]/div[3]/div[5]/div[1]/p[2]').text
                familyInfo = driver.find_element(By.XPATH, f'/html/body/div[3]/div[3]/div[5]/div[1]').text
                crimeDescription = familyInfo.split("Events of 31 May 1963")[1].split("Trial")[0].replace("\n", "").strip()
                additionalInfo = familyInfo.split("Trial")[1].split("See also")[0].replace("\n", "").strip()
                familyInfo = familyInfo.split("Background")[1].split("Events of 31 May 1963")[0].replace("\n", "").strip()
            else:
                try:
                    image = driver.find_element(By.XPATH, f'/html/body/div[3]/div[3]/div[5]/div[1]/table[@class="infobox biography vcard"]/tbody/tr[2]/td/a/img').get_attribute("src")
    #                 print(image)
                except:
                    pass
                fullName = driver.find_element(By.XPATH, f'/html/body/div[3]/div[3]/div[5]/div[1]/table/tbody/tr[1]/th').text
                print(fullName)
                list2 = driver.find_elements(By.XPATH, f'/html/body/div[3]/div[3]/div[5]/div[1]/table[@class="infobox biography vcard"]/tbody/tr')
                for j in range(1, len(list2)+1):
                    heading = driver.find_element(By.XPATH, f'/html/body/div[3]/div[3]/div[5]/div[1]/table[@class="infobox biography vcard"]/tbody/tr[{j}]').text
                    if "Education" in heading:
                        educationInfo = driver.find_element(By.XPATH, f'/html/body/div[3]/div[3]/div[5]/div[1]/table[@class="infobox biography vcard"]/tbody/tr[{j}]').text
                        educationInfo = educationInfo.split("Education")[1].strip()
                        print(educationInfo)
                    if "Other names" in heading:
                        alias = driver.find_element(By.XPATH, f'/html/body/div[3]/div[3]/div[5]/div[1]/table[@class="infobox biography vcard"]/tbody/tr[{j}]').text
                        alias = alias.split("Other names")[1].replace("\n", "; ").strip()
                        print(alias)
                    if "Nationality" in heading:
                        nationality = driver.find_element(By.XPATH, f'/html/body/div[3]/div[3]/div[5]/div[1]/table[@class="infobox biography vcard"]/tbody/tr[{j}]').text
                        nationality = nationality.split("Nationality")[1].strip()
                        print(nationality)
                    if "Country" in heading:
                        country = driver.find_element(By.XPATH, f'/html/body/div[3]/div[3]/div[5]/div[1]/table[@class="infobox biography vcard"]/tbody/tr[{j}]').text
                        country = country.split("Country")[1].strip()
                        print(country)
                    if "Date apprehended" in heading:
                        dateAp = driver.find_element(By.XPATH, f'/html/body/div[3]/div[3]/div[5]/div[1]/table[@class="infobox biography vcard"]/tbody/tr[{j}]').text
                        dateAp = dateAp.split("Date apprehended")[1].strip()
                        importantDates = "Date Apprehended: " + dateAp + "; " + importantDates
                    if "Occupation" in heading:
                        careerInfoDesignation = driver.find_element(By.XPATH, f'/html/body/div[3]/div[3]/div[5]/div[1]/table[@class="infobox biography vcard"]/tbody/tr[{j}]').text
                        careerInfoDesignation = careerInfoDesignation.split("Occupation")[1].strip()
                try:
                    list4 = driver.find_elements(By.XPATH, f'/html/body/div[3]/div[3]/div[5]/div[1]/p')
                    for l in range(1, len(list4)+1):
                        if l in range(1, 4):
                            description = driver.find_element(By.XPATH, f'/html/body/div[3]/div[3]/div[5]/div[1]/p[{l}]').text + " " +summary
                        else:
                            additionalInfo = driver.find_element(By.XPATH, f'/html/body/div[3]/div[3]/div[5]/div[1]/p[{l}]').text + " "+ additionalInfo
                except:
                    pass
            additionalInfo = re.sub(r'\[[0-9]*\]','',additionalInfo)
            alias = re.sub(r'\[[0-9]*\]','',alias)
            if fullName !="":
                summary = fullName + " is one of the Most Wicked Scottish Criminals for " + types
            driver.close()
            driver.switch_to.window(driver.window_handles[0])
            print("*"*50)
        except:
            pass
        if fullName:
            data_dict['fullName'] = fullName
            if image:
                data_dict['image'] = image
            if dob:
                data_dict['dob'] = dob
            if placeOfBirthCity:
                data_dict['placeOfBirthCity'] = placeOfBirthCity
            if identifierType:
                data_dict['identifierType'] = identifierType
            if alias:
                data_dict['alias'] = alias
            if importantDates:
                data_dict['importantDates'] = importantDates
            if types:
                data_dict['type'] = types
            if familyInfo:
                data_dict['familyInfo'] = familyInfo
            if description:
                data_dict['description'] = description
            if careerInfoDesignation:
                data_dict['careerInfoDesignation'] = careerInfoDesignation
            if crimeDescription:
                data_dict['crimeDescription'] = crimeDescription
            if educationInfo:
                data_dict['educationInfo'] = educationInfo
            if nationality:
                data_dict['nationality'] = nationality
            if country:
                data_dict['country'] = country
            if additionalInfo:
                data_dict['additionalInfo'] = additionalInfo
            if summary:
                data_dict['summary'] = summary
        if len(data_dict) != 0:
            data_list.append(data_dict)
    driver.quit()
    return data_list


# In[51]:


if __name__ == '__main__':
    data_list = get_data("add_slug_name")
    to_json(data_list)


# In[ ]:




