
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import json
import re
from deep_translator import GoogleTranslator

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
    url = "https://www.bmf.gv.at/en/the-ministry/minister-of-finance.html"
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized") 
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--log-level=3")
    translator = GoogleTranslator(target='english')
    driver = webdriver.Chrome(options=options)
    driver.get(url)
    list1 = driver.find_elements(By.XPATH, f'/html/body/div[2]/div/div/div/div[2]/aside/nav/ul/li/a')
    for i in range(1, 3):
        data_dict ={}
        careerInfo = ""
        educationInfo =""
        fullAddress =""
        telephoneNos =""
        emails =""
        title =""
        driver.find_element(By.XPATH, f'/html/body/div[2]/div/div/div/div[2]/aside/nav/ul/li[{i}]/a').click()
        careerInfoDesignation = driver.find_element(By.XPATH, f'/html/body/div[2]/div/div/div/div[2]/main/h1/span').text
    #     print(careerInfoDesignation)
        if "Finance" in careerInfoDesignation:
            fullName = careerInfoDesignation.split("Dr")[1].strip()
            careerInfoDesignation = careerInfoDesignation.split("Dr")[0]
            title = "Dr"
        if "State" in careerInfoDesignation:
            fullName = careerInfoDesignation.split(" ", 2)[2].replace("\n", "")
            careerInfoDesignation = "State Secretary"
        print(fullName)
        print(careerInfoDesignation)
        image = driver.find_element(By.XPATH, f'/html/body/div[2]/div/div/div/div[2]/main/figure/img').get_attribute('src')
        print(image)
        list2 = driver.find_elements(By.XPATH, f'/html/body/div[2]/div/div/div/div[2]/main/p')
        for j in range(1, len(list2)+1):
            info = driver.find_element(By.XPATH, f'/html/body/div[2]/div/div/div/div[2]/main/p[{j}]').text
            if "born:" in info or "Born:" in info:
                try:
                    dob = info.split("born:")[1].strip()
                except:
                    dob = info.split("Born:")[1].strip()
                placeOfBirthCity = dob.split(",")[1].strip()
                dob = dob.split(",")[0]
                dob = dob.replace(".", "/")
                print(dob)
                print(placeOfBirthCity)
        list3 = driver.find_elements(By.XPATH, f'/html/body/div[2]/div/div/div/div[2]/main/ul')
        for k in range(1, len(list3)+1):
            info2 = driver.find_element(By.XPATH, f'/html/body/div[2]/div/div/div/div[2]/main/ul[{k}]').text
            if "Universität" in info2 or " University" in info2:
                educationInfo = info2.replace("\n", "; ")
            else:
                careerInfo = careerInfo + info2
        careerInfo = careerInfo.replace("\n", "; ")
        print(educationInfo)
        print(careerInfo)
        try:

            info3 = driver.find_element(By.XPATH, f'/html/body/div[2]/div/div/div/div[2]/main/p[5]').text
            if "Educational background" not in info3:
                fullAddress = info3.split("\n")[0]
                print(fullAddress)
                telephoneNos = info3.split("\n")[1].split(":")[1].strip()
                print(telephoneNos)
                emails = info3.split("\n")[2].split(":")[1].strip()
                print(emails)
        except:
            pass
        summary = fullName + " is the "+ careerInfoDesignation+ " in Federal Ministry for Finance."
        if fullName:
            data_dict['fullName'] = fullName
        if careerInfoDesignation:
            data_dict['careerInfoDesignation'] = careerInfoDesignation
        if title:
            data_dict['title'] = title
        if dob:
            data_dict['dob'] = dob
        if placeOfBirthCity:
            data_dict['placeOfBirthCity'] = placeOfBirthCity
        if educationInfo:
            data_dict['educationInfo'] = educationInfo
        if careerInfo:
            data_dict['careerInfo'] = careerInfo
        if fullAddress:
            data_dict['fullAddress'] = fullAddress
        if telephoneNos:
            data_dict['telephoneNos'] = telephoneNos
        if emails:
            data_dict['emails'] = emails
        if summary:
            data_dict['summary'] = summary
        data_list.append(data_dict)

    driver.find_element(By.XPATH, f'/html/body/div[2]/div/div/div/div[2]/aside/nav/ul/li[1]/a').click()
    driver.find_element(By.XPATH, f'/html/body/div[2]/div/div/div/div[2]/aside/nav/ul/li[1]/ul/li/a').click()
    list4 = driver.find_elements(By.XPATH, f'/html/body/div[2]/div/div/div/div[2]/main/h2')
    for l in range(1, len(list4)+1):
        data_dict2 = {}
        careerInfoDesignation = ""
        fullName = driver.find_element(By.XPATH, f'/html/body/div[2]/div/div/div/div[2]/main/h2[{l}]').text
        print(fullName)
        try:
            careerInfoDesignation = driver.find_element(By.XPATH, f'/html/body/div[2]/div/div/div/div[2]/main/p[{l}]').text.replace("\n", "; ")
            print(careerInfoDesignation)
        except:
            pass
        
        if "Contact" in fullName or "Governmental coordination" in fullName:
            fullName = ""
        if "Martin Humer" in fullName:
            careerInfoDesignation = "Deputy Chef de Cabinet"
        if "Florian Seifert" in fullName:
            careerInfoDesignation = "Specialist"
        summary = fullName + " is the "+ careerInfoDesignation+ " in Federal Ministry for Finance."
        if fullName:
            data_dict2['fullName'] = fullName
            if careerInfoDesignation:
                data_dict2['careerInfoDesignation'] = careerInfoDesignation
            if summary:
                data_dict2['summary'] = summary
            data_list.append(data_dict2)
    driver.quit()
    return data_list


if __name__ == '__main__':
    data_list = get_data("add_slug_name")
    to_json(data_list)



