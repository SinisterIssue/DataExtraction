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
    url = "https://www.parliament.gov.za/ministers"
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized") 
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--log-level=3")
    translator = GoogleTranslator(target='english')
    driver = webdriver.Chrome(options=options)
    driver.get(url)
    list1 = driver.find_elements(By.XPATH, f'//div[3]/div[1]/div[2]/div/div[1]/table/tbody/tr')
    for i in range(1, len(list1)+1):
        data_dict = {}
        careerInfoDesignation = ""
        educationInfo = ""
        careerInfo  =""
        additionalInfo  =""
        emails = ""
        twitterUrl = ""
        website = ""
        prefix = ""
        politicalParty = ""
        summary = ""
        fullName = driver.find_element(By.XPATH, f'//div[3]/div[1]/div[2]/div/div[1]/table/tbody/tr[{i}]/td[2]').text
        if fullName == "Vacant":
            fullName = ""
        if fullName != "":
            prefix = fullName.split(" ", 1)[0]
            fullName = fullName.split(" ", 1)[1]
        print(fullName)
        careerInfoDesignation = driver.find_element(By.XPATH, f'//div[3]/div[1]/div[2]/div/div[1]/table/tbody/tr[{i}]/td[1]').text
        try:
            link = driver.find_element(By.XPATH, f'//div[3]/div[1]/div[2]/div/div[1]/table/tbody/tr[{i}]/td[2]/a').get_attribute("href")
            driver.execute_script("window.open('');")
            driver.switch_to.window(driver.window_handles[1])
            driver.get(link)
            time.sleep(2)
            image = driver.find_element(By.XPATH, f'/html/body/div[2]/div/div[4]/div[3]/div[1]/div[2]/div/div/div[2]/div/div[1]/img').get_attribute("src")
            careerInfoDesignation = driver.find_element(By.XPATH, f'/html/body/div[2]/div/div[4]/div[3]/div[1]/div[2]/div/div/div[2]/div/div[2]/span[2]').text
            politicalParty = driver.find_element(By.XPATH, f'/html/body/div[2]/div/div[4]/div[3]/div[1]/div[2]/div/div/div[2]/div/div[2]/span[4]').text
            print(politicalParty)
            try:
                emails = driver.find_element(By.XPATH, f'/html/body/div[2]/div/div[4]/div[3]/div[1]/div[2]/div/div/div[2]/div/div[2]/div/div[1]/p[1]/a').text
            except:
                pass
            try:
                twitterUrl = driver.find_element(By.XPATH, f'/html/body/div[2]/div/div[4]/div[3]/div[1]/div[2]/div/div/div[2]/div/div[2]/div/div[2]/p/a').get_attribute("href")
            except:
                pass
            try:
                website = driver.find_element(By.XPATH, f'/html/body/div[2]/div/div[4]/div[3]/div[1]/div[2]/div/div/div[2]/div/div[2]/div/div[1]/p[2]/a').text
            except:
                pass
            try:
                heading = driver.find_element(By.XPATH, f'/html/body/div[2]/div/div[4]/div[3]/div[1]/div[2]/div/div/div[2]/h3[1]').text
                if "PARLIAMENT MEMBERSHIP HISTORY" in heading:
                    info = driver.find_element(By.XPATH, f'/html/body/div[2]/div/div[4]/div[3]/div[1]/div[2]/div/div/div[2]').text
                    careerInfo = info.split("PARLIAMENT MEMBERSHIP HISTORY")[1].split("EDUCATION")[0].replace("\n",";").replace("POLITICAL LEADERSHIP BACKGROUND;", ", POLITICAL LEADERSHIP BACKGROUND: ").replace(" ;", "; ").replace(";", "",1).strip()
                    educationInfo = info.split("EDUCATION")[1].split("INTERESTS")[0].replace("\n", ";").replace(";", "", 1).replace(" ;", "; ").strip()
                    additionalInfo = info.split("INTERESTS")[1].replace("\n", ";").replace(";", "INTERESTS: ", 1).replace(" ;", "; ").replace("POLITICAL IDEAS / ACHIEVEMENTS GOALS & AMBITIONS FOR THE COUNTRY;", ", POLITICAL IDEAS / ACHIEVEMENTS GOALS & AMBITIONS FOR THE COUNTRY: ").strip()
                    print(careerInfo)
                    print(educationInfo)
                    print(additionalInfo)
                if "PROFILE" in heading:
                    info = driver.find_element(By.XPATH, f'/html/body/div[2]/div/div[4]/div[3]/div[1]/div[2]/div/div/div[2]').text
                    try:
                        careerInfo = info.split("PROFILE")[1].split("EDUCATION")[0].replace("\n", "; ").replace(";", "", 1).strip()
                        educationInfo = info.split("EDUCATION")[1].replace("\n", ";").replace(";", "", 1).strip()
                        print(careerInfo)
                        print(educationInfo)
                    except:
                        try:
                            careerInfo = info.split("PROFILE")[1].replace("\n", "; ").replace(";", "", 1).strip()
                            print(careerInfo)
                        except:
                            pass
            except:
                pass
            summary = fullName + " is the "+ careerInfoDesignation + " in the Parliament of the  Republic of South Africa"
            driver.close()
            driver.switch_to.window(driver.window_handles[0])
        except:
            pass
        if fullName:
            data_dict['fullName'] = fullName
            if prefix:
                data_dict['prefix'] = prefix
            if careerInfoDesignation:
                data_dict['careerInfoDesignation'] = careerInfoDesignation
            if politicalParty:
                data_dict['politicalParty'] = politicalParty
            if careerInfo:
                data_dict['careerInfo'] = careerInfo
            if educationInfo:
                data_dict['educationInfo'] = educationInfo
            if additionalInfo:
                data_dict['additionalInfo'] = additionalInfo
            if emails:
                data_dict['emails'] = emails
            if website:
                data_dict['website'] = website
            if twitterUrl:
                data_dict['twitterUrl'] = twitterUrl
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




