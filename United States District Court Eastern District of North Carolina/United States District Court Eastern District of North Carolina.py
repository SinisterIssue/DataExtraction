
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import json
import re
from deep_translator import GoogleTranslator
from selenium.webdriver.common.keys import Keys
import requests
import PyPDF2
import io

def to_json(data):
    """
    This function takes list of dictionary as Input and 
    then Creates a JSON file in which Input data is stored
    """
    with open("data_dict.json", "w") as outfile:
        json.dump(data, outfile,indent=4)
        outfile.close()

def get_data(slug_name):    
    data_list = []
    url = "http://www.nced.uscourts.gov/judges/Default.aspx"
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized") 
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--log-level=3")
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
#     options.headless = True
    translator = GoogleTranslator(target='english')
    driver = webdriver.Chrome(options=options)
    driver.maximize_window()
    driver.get(url)
    time.sleep(3)
    for i in range(1, 20):
        data_dict = {}
        fullName = ""
        addressLine1 = ""
        additionalInfo = ""
        referenceUrls  =""
        status = ""
        summary = ""
        careerInfoStartDate = ""
        educationInfo = ""
        description = ""
        try:
            careerInfoDesignation = driver.find_element(By.XPATH, f'/html/body/form/section[4]/div/div/div[2]/div[2]/table/tbody/tr[{i}]/td[1]/a').text
        except:
            try:
                careerInfoDesignation = driver.find_element(By.XPATH, f'/html/body/form/section[4]/div/div/div[2]/div[2]/table/tbody/tr[{i}]/td[1]').text
            except:
                pass
        if "name" in careerInfoDesignation or careerInfoDesignation =="Chief United States District Judge" or careerInfoDesignation == "United States District Judges" or careerInfoDesignation == "United States Magistrate Judges":
            careerInfoDesignation = ""
        try:
            fullName = careerInfoDesignation.split("Judge")[1].strip()
            if "(" in fullName:
                additionalInfo = fullName.split("(")[1].replace(")", "").strip()
                print(additionalInfo)
                fullName = fullName.split("(")[0]
            print(fullName)
            print(i)
        except:
            pass
        try:
            careerInfoDesignation = careerInfoDesignation.split(fullName)[0].strip()
            print(careerInfoDesignation)
        except:
            pass
        try:
            addressLine1 = driver.find_element(By.XPATH, f'/html/body/form/section[4]/div/div/div[2]/div[2]/table/tbody/tr[{i}]/td[2]/a').text
            print(addressLine1)
        except:
            pass
        try:
            referenceUrls = driver.find_element(By.XPATH, f'/html/body/form/section[4]/div/div/div[2]/div[2]/table/tbody/tr[{i}]/td[1]/a').get_attribute('href')
            print(referenceUrls)
        except:
            pass
        if fullName != "" and additionalInfo != "":
            summary = fullName + " is the " + careerInfoDesignation + " and is currently inactive and not taking cases."
        elif fullName != "" and additionalInfo == "":
            summary = fullName + " is the " + careerInfoDesignation + " and is currently active."
        if additionalInfo == "":
            status = "Active"
        elif additionalInfo != "":
            status = "Inactive"
        try:
            driver.find_element(By.XPATH, f'/html/body/form/section[4]/div/div/div[2]/div[2]/table/tbody/tr[{i}]/td[1]/a').click()
            try:
                link = driver.find_element(By.LINK_TEXT, f'Biography').get_attribute('href')
                driver.execute_script("window.open('');")
                driver.switch_to.window(driver.window_handles[1])
                driver.get(link)
                time.sleep(2)
                user_agent = "scrapping_script/1.0"
                headers = {'User-Agent': user_agent}
                r = requests.get(link, headers=headers, stream = True)
                file = io.BytesIO(r.content)
                fileReader = PyPDF2.PdfFileReader(file)
                total = ""
                pages = fileReader.numPages
                for page in range(0, pages):
                    page = fileReader.pages[page]
                    page_content = page.extractText()
                    total = total + page_content
                if "DUCATION" in total:
                    description = total
                    careerInfoStartDate = description.split("PPOINTED:")[1].split("\n", 1)[0].strip()
                    educationInfo = description.split("DUCATION:")[1].split("E", 1)[0].strip().replace("\n", "; ")
                    description = description.split("XPERIENCE:")[1].strip().replace("\n", " ")
                if "DUCATION" not in total:
                    description = total.split(fullName, 1)[1].replace("\n", " ").strip()
                print(description)
                driver.close()
                driver.switch_to.window(driver.window_handles[0])
            except:
                pass
            driver.back()
        except:
            pass
        print("*"*50)
        if fullName:
            data_dict['fullName'] = fullName
            if careerInfoDesignation:
                data_dict['careerInfoDesignation'] = careerInfoDesignation
            if careerInfoStartDate:
                data_dict['careerInfoStartDate'] = careerInfoStartDate
            if status:
                data_dict['status'] = status
            if addressLine1:
                data_dict['addressLine1'] = addressLine1
            if description:
                data_dict['description'] = description
            if additionalInfo:
                data_dict['additionalInfo'] = additionalInfo
            if educationInfo:
                data_dict['educationInfo'] = educationInfo
            if referenceUrls:
                data_dict['referenceUrls'] = referenceUrls
            if summary:
                data_dict['summary'] = summary
            data_list.append(data_dict)
    driver.quit()
    return data_list

if __name__ == '__main__':
    data_list = get_data("add_slug_name")
    to_json(data_list)



