#!/usr/bin/env python
# coding: utf-8

# In[41]:


from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import json
import re
from selenium.webdriver.common.keys import Keys


# In[42]:


def to_json(data):
    """
    This function takes list of dictionary as Input and 
    then Creates a JSON file in which Input data is stored
    """
    with open("data_dict.json", "w") as outfile:
        json.dump(data, outfile,indent=4)
        outfile.close()


# In[43]:


data_list = []
url = "https://www.fdic.gov/bank/individual/failed/banklist.html"
options = webdriver.ChromeOptions()
options.add_argument("--start-maximized") 
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument("--log-level=3")


# In[44]:


def get_data(slug_name):
    driver = webdriver.Chrome(options=options)
    driver.get(url)
    search = driver.find_element(By.XPATH, f'//div[3]/label/select')
    search.send_keys("All")
    search.send_keys(Keys.RETURN)
    time.sleep(3)
    list1 = driver.find_elements(By.XPATH, f'//div[2]/table/tbody/tr')
    for i in range(1, len(list1)+1):
        list2 = driver.find_elements(By.XPATH, f'//div[2]/table/tbody/tr[{i}]/td')
        description = ""
        importantDates = ""
        data_dict ={}
        print("*"*50)
        for j in range(1, len(list2)+1):
            if j==1:
                fullName = driver.find_element(By.XPATH, f'//div[2]/table/tbody/tr[{i}]/td[{j}]').text
                print(fullName)
                referenceUrls = driver.find_element(By.XPATH, f'//div[2]/table/tbody/tr[{i}]/td[{j}]/a').get_attribute("href")
                driver.execute_script("window.open('');")
                driver.switch_to.window(driver.window_handles[1])
                driver.get(referenceUrls)
                time.sleep(2)
                try:
                    description = driver.find_element(By.XPATH, f'/html/body/main/section[1]/div/div/p[2]').text
                    print(description)
                except:
                    try:
                        list3 = driver.find_elements(By.XPATH, f'/html/body/div[4]/p')
                        for k in range (1, len(list3)+1):
                            description = description + " " + driver.find_element(By.XPATH, f'/html/body/div[4]/p[{k}]').text
                        decription = description.replace("\n", "").strip()
                        print(description)
                        try:
                            list4 = driver.find_elements(By.XPATH, f'/html/body/div[4]/div[1]/div[2]/p')
                            for l in range(1, len(list4)+1):
                                text = driver.find_element(By.XPATH, f'/html/body/div[4]/div[1]/div[2]/p[{l}]').text
                                if "Notice of Termination" in text:
                                    EffectiveDate = driver.find_element(By.XPATH, f'/html/body/div[4]/div[1]/div[2]/p[{l+1}]').text
                                if "Notice of Intent to Terminate" in text:
                                    PublicationDate = driver.find_element(By.XPATH, f'/html/body/div[4]/div[1]/div[2]/p[{l+1}]').text
                            importantDates = importantDates + " Notice of Termination: " + EffectiveDate + "; Notice of Intent to Terminate: " + PublicationDate 
                        except:
                            pass
                    except:
                        pass
                driver.close()
                driver.switch_to.window(driver.window_handles[0])
            elif j==2:
                city = driver.find_element(By.XPATH, f'//div[2]/table/tbody/tr[{i}]/td[{j}]').text
            elif j==3:
                state = driver.find_element(By.XPATH, f'//div[2]/table/tbody/tr[{i}]/td[{j}]').text
            elif j==4:
                cert = driver.find_element(By.XPATH, f'//div[2]/table/tbody/tr[{i}]/td[{j}]').text
            elif j==5:
                AccquiringInstitute = driver.find_element(By.XPATH, f'//div[2]/table/tbody/tr[{i}]/td[{j}]').text.replace("No Acquirer", "None")
            elif j==6:
                closingDate = driver.find_element(By.XPATH, f'//div[2]/table/tbody/tr[{i}]/td[{j}]').text
            elif j==7:
                fund = driver.find_element(By.XPATH, f'//div[2]/table/tbody/tr[{i}]/td[{j}]').text

        importantDates = importantDates + "; Closing Date: " + closingDate
        additionalInfo = "Cert: " + cert + "; Acquiring Institution: " + AccquiringInstitute + "; Fund: " + fund
        if "None" not in AccquiringInstitute:
            summary = fullName + " is in the United States - US-U.S FDIC Failed Bank list. " + "The bank was closed on "+ closingDate + " and was acquired by "+ AccquiringInstitute
        else:
            summary = fullName + " is in the United States - US-U.S FDIC Failed Bank list. " + "The bank was closed on "+ closingDate 
        if fullName:
            data_dict['fullName'] = fullName
        if city:
            data_dict['city'] = city
        if state:
            data_dict['state'] = state
        if importantDates:
            data_dict['importantDates'] = importantDates
        if description:
            data_dict['description'] = description
        if additionalInfo:
            data_dict['additionalInfo'] = additionalInfo
        if referenceUrls:
            data_dict['referenceUrls'] = referenceUrls
        if summary:
            data_dict['summary'] = summary
        data_list.append(data_dict)
    return data_list


# In[45]:


if __name__ == '__main__':
    data_list = get_data("add_slug_name")
    to_json(data_list)


# In[ ]:




