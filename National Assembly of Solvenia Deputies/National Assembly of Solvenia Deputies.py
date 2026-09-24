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
    url = "https://www.dz-rs.si/wps/portal/newEn/Home/Deputies/Deputies/!ut/p/z1/04_Sj9CPykssy0xPLMnMz0vMAfIjo8zivSy9Hb283Q0N3I2CTA0CXYycfIMNjA2cvc30w_EpMHEy0I_Co9_XEKrfAAdwJFI_HgVRFLgfpCAKv_MKckOBwFERACalbtg!/dz/d5/L2dBISEvZ0FBIS9nQSEh/"
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized") 
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--log-level=3")
    translator = GoogleTranslator(target='english')
    driver = webdriver.Chrome(options=options)
    driver.get(url)
    list1 = driver.find_elements(By.XPATH, f'//div[2]/div/div/div/div[2]/div/div/form/div[7]/div[4]/div/div')
    for i in range(1, len(list1)+1):
        data_dict = {}
        dob= ""
        placeOfBirthCity = ""
        educationInfo = ""
        careerInfo =""
        linkedinUrl = ""
        facebookUrl =""
        prefix = ""
        instagramUrl = ""
        twitterUrl = ""
        otherSocialUrls = ""
        image = driver.find_element(By.XPATH, f'//div[2]/div/div/div/div[2]/div/div/form/div[7]/div[4]/div/div[{i}]/img').get_attribute("src")
        fullName = driver.find_element(By.XPATH, f'//div[2]/div/div/div/div[2]/div/div/form/div[7]/div[4]/div/div[{i}]/div[1]').text
        if "." in fullName:
            prefix = fullName.split(".")[0]
            fullName = fullName.split(".")[1].strip()
        print(fullName)
        politicalParty = driver.find_element(By.XPATH, f'//div[2]/div/div/div/div[2]/div/div/form/div[7]/div[4]/div/div[{i}]/div[2]').text
    #     print(politicalParty)
        link = driver.find_element(By.XPATH, f'//div[2]/div/div/div/div[2]/div/div/form/div[7]/div[4]/div/div[{i}]/div[1]/a').get_attribute("href")
        driver.execute_script("window.open('');")
        driver.switch_to.window(driver.window_handles[1])
        driver.get(link)
        time.sleep(2)
        importantDates = driver.find_element(By.XPATH, f'//div/div/div/div/div[2]/div/div/form/div[4]/div[1]/div[2]/div[1]/div/div[1]/div[2]').text
        importantDates = importantDates.replace(". ", "/")
    #     print(importantDates)
        constituency = driver.find_element(By.XPATH, f'//div/div/div/div[2]/div/div/form/div[4]/div[1]/div[2]/div[1]/div/div[3]/div[2]').text
    #     print(constituency)
        try:
            facebookUrl = driver.find_element(By.XPATH, f'//div[2]/div/div/form/div[4]/div[1]/div[1]/div[1]/div[2]/div/div/div[3]/div/span[@title="Facebook"]/a').get_attribute("href")
    #         print(facebookUrl)
        except:
            pass
        try:
            instagramUrl = driver.find_element(By.XPATH, f'//div[2]/div/div/form/div[4]/div[1]/div[1]/div[1]/div[2]/div/div/div[3]/div/span[@title="Instagram"]/a').get_attribute("href")
    #         print(instagramUrl)
        except:
            pass
        try:
            linkedinUrl = driver.find_element(By.XPATH, f'//div[2]/div/div/form/div[4]/div[1]/div[1]/div[1]/div[2]/div/div/div[3]/div/span[@title="LinkedIn"]/a').get_attribute("href")
    #         print(linkedinUrl)
        except:
            pass
        try:
            twitterUrl = driver.find_element(By.XPATH, f'//div[2]/div/div/form/div[4]/div[1]/div[1]/div[1]/div[2]/div/div/div[3]/div/span[@title="Twitter"]/a').get_attribute("href")
        except:
            pass
        try:
            otherSocialUrls = driver.find_element(By.XPATH, f'//div[2]/div/div/form/div[4]/div[1]/div[1]/div[1]/div[2]/div/div/div[3]/div/span[@title="Osebni blog"]/a').get_attribute("href")
            otherSocialUrls = "Osebni blog: " + otherSocialUrls
        except:
            pass
        try:
            driver.find_element(By.LINK_TEXT, f'Curriculum vitae').click()
            time.sleep(2)
            info = driver.find_element(By.XPATH, f'/html/body/div[1]/div[1]/div[3]/div/div[2]/div/div/div/div/div[2]/div/div/form/div[4]/div[1]/div[1]/div[3]/div').text
            dobInfo = info.split("Personal data:")[1].split("Education:")[0]
            dob = dobInfo.split("Born on")[1].strip()
            if "in" in dob:
                placeOfBirthCity = dob.split("in", 1)[1].strip()
                dob = dob.split("in", 1)[0].strip()
            print(dob)
            educationInfo = info.split("Education", 1)[1].split("Work experience:")[0].replace("\n", "; ").replace(":;", "")
            careerInfo = info.split("Work experience:")[1].replace("\n", "; ").replace("; ", "", 1)
        except:
            pass
        summary = fullName + " is one of the Deputies of the National Assembly and belongs to the " + politicalParty + " political party."
        driver.close()
        driver.switch_to.window(driver.window_handles[0])
        print("*"*50)
        if fullName:
            data_dict['fullName'] = fullName
        if prefix:
            data_dict['prefix'] = prefix
        if image:
            data_dict['image'] = image
        if politicalParty:
            data_dict['politicalParty'] = politicalParty
        if constituency:
            data_dict['constituency'] = constituency
        if dob:
            data_dict['dob'] = dob
        if placeOfBirthCity:
            data_dict['placeOfBirthCity'] = placeOfBirthCity
        if importantDates:
            data_dict['importantDates'] = importantDates
        if educationInfo:
            data_dict['educationInfo'] = educationInfo
        if careerInfo:
            data_dict['careerInfo'] = careerInfo
        if facebookUrl:
            data_dict['facebookUrl'] = facebookUrl
        if linkedinUrl:
            data_dict['linkedinUrl'] = linkedinUrl
        if instagramUrl:
            data_dict['instagramUrl'] = instagramUrl
        if twitterUrl:
            data_dict['twitterUrl'] = twitterUrl
        if otherSocialUrls:
            data_dict['otherSocialUrls'] = otherSocialUrls
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




