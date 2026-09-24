#!/usr/bin/env python
# coding: utf-8

# In[1]:


from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import json
import re
from deep_translator import GoogleTranslator


# In[2]:


def to_json(data):
    """
    This function takes list of dictionary as Input and 
    then Creates a JSON file in which Input data is stored
    """
    with open("data_dict.json", "w") as outfile:
        json.dump(data, outfile,indent=4)
        outfile.close()


# In[5]:


def get_data(slug_name):
    data_list = []
    url = "http://www.crimestopperssiouxempire.com/Wanteds.aspx?ID=207&Sort=WantedDate&F="
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized") 
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--log-level=3")
    translator = GoogleTranslator(target='english')
    driver = webdriver.Chrome(options=options)
    driver.get(url)
    while True:
        try:
            time.sleep(3)
            list1 = driver.find_elements(By.XPATH, f'/html/body/form/div[3]/div/div/div/div[2]/div')
    #         print(len(list1))

            for i in range(2, len(list1)+1):
                importantDates = ""
                captureDate_dmy =""
                wantedDate_dmy = ""
                offence = ""
                data_dict = {}
                crimeDescription = ""
                arrestWarrant =""
                list2 = driver.find_elements(By.XPATH, f'/html/body/form/div[3]/div/div/div/div[2]/div[{i}]/div[2]/table/tbody/tr')
                for j in range(1, len(list2)+1):
                    heading = driver.find_element(By.XPATH, f'/html/body/form/div[3]/div/div/div/div[2]/div[{i}]/div[2]/table/tbody/tr[{j}]').text
    #                 print(heading)
                    if j==1:
                        offence = driver.find_element(By.XPATH, f'/html/body/form/div[3]/div/div/div/div[2]/div[{i}]/div[2]/table/tbody/tr[{j}]').text
    #                     print(offence)
                        wantedDate = offence.split("\n")[1]
                        offence = offence.split("\n")[0]
                        offence = offence.replace("/", ";")
                        if "Wanted" in wantedDate and "CAPTURED" not in wantedDate:
                            status = "Wanted"
                            wantedDate_dmy = wantedDate.split(" ")[3]
                            d = wantedDate_dmy.split("/")[1]
                            m = wantedDate_dmy.split("/")[0]
                            y = wantedDate_dmy.split("/")[2]
                            wantedDate_dmy = d + "/" + m + "/" + y
                            importantDates = "Wanted as of: " + wantedDate_dmy
                            print(importantDates)
                        if "CAPTURED" in wantedDate:
                            status = "Captured"
    #                         print(wantedDate)
                            captureDate_dmy = wantedDate.split("CAPTURED")[1].split("***")[0].strip()
                            d = captureDate_dmy.split("/")[1]
                            m = captureDate_dmy.split("/")[0]
                            y = captureDate_dmy.split("/")[2]
                            captureDate_dmy = d + "/" + m + "/" + y
                            importantDates = "Captured on: " + captureDate_dmy
                            print(importantDates)
                    if "Name:" in heading:
                        fullName = heading.split("Name:")[1].strip()
                        firstName = fullName.split(",")[1]
                        lastName = fullName.split(",")[0]
                        fullName = firstName + " " + lastName
                        fullName = fullName.strip()
                        print(fullName)
                    if "Gender:" in heading:
                        gender = heading.split("Gender:")[1].split("Race:")[0].strip()
                        race = heading.split("Race:")[1].strip()
                        print(gender)
                        print(race)
                    if "Height:" in heading:
                        height = heading.split("Height:")[1].split("Weight:")[0].strip()
                        weight = heading.split("Weight:")[1].strip()
                        height = height.replace("ft", "'").replace('in', '"')
                        print(height)
                        print(weight)
                    if "Hair:" in heading:
                        hair = heading.split("Hair:")[1].split("Eyes:")[0].strip()
                        eyes = heading.split("Eyes:")[1].strip()
                        print(hair)
                        print(eyes)
                    if "DOB:" in heading:
                        dob = heading.split("DOB:")[1].split("Age")[0].strip()
                        age = heading.split("Age:")[1].strip()
                        print(dob)
                        print(age)
                    if "Warrant:" in heading:
                        arrestWarrant = heading.split("Warrant:")[1].replace("/", "; ").strip()
                    if "As of" in heading:
                        crimeDescription = heading.replace("\n", "")
                        print(crimeDescription)
                try:
                    crimeDescription = driver.find_element(By.XPATH, f'/html/body/form/div[3]/div/div/div/div[2]/div[4]/div[3]/div').text
                    print(crimeDescription)
                except:
                    pass
                summary = fullName + " is " + status + " for the offence " + offence
                print("*"*50)
                if fullName:
                    data_dict['fullName'] = fullName
                if offence:
                    data_dict['offence'] = offence
                if status:
                    data_dict['status'] = status
                if dob:
                    data_dict['dob'] = dob
                if age:
                    data_dict['age'] = age
                if gender:
                    data_dict['gender'] = gender
                if race:
                    data_dict['race'] = race
                if height:
                    data_dict['height'] = height
                if weight:
                    data_dict['weight'] = weight
                if hair:
                    data_dict['hair'] = hair
                if eyes:
                    data_dict['eyes'] = eyes
                if arrestWarrant:
                    data_dict['arrestWarrant'] = arrestWarrant
                if importantDates:
                    data_dict['importantDates'] = importantDates
                if crimeDescription:
                    data_dict['crimeDescription'] = crimeDescription
                if summary:
                    data_dict['summary'] = summary
                data_list.append(data_dict)
            driver.find_element(By.LINK_TEXT, f'Next').click()
        except:
            break
    driver.quit()
    return data_list


# In[6]:


if __name__ == '__main__':
    data_list = get_data("add_slug_name")
    to_json(data_list)


# In[ ]:




