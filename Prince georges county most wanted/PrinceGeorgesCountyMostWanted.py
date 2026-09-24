
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import json


def to_json(data):
    """
    This function takes list of dictionary as Input and 
    then Creates a JSON file in which Input data is stored
    """
    with open("data_dict.json", "w") as outfile:
        json.dump(data, outfile,indent=4)
        outfile.close()


data_list = []
url = "https://www.princegeorgescountymd.gov/697/Most-Wanted"
options = webdriver.ChromeOptions()
options.add_argument("--start-maximized") 
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument("--log-level=3")


def get_data(slug_name):
    driver = webdriver.Chrome(options=options)
    driver.get(url)
    list1 = driver.find_elements(By.XPATH, f'/html/body/div[8]/div/div[2]/div[2]/div[1]/div/div[4]/div/div/div[1]/div/div/div[1]/div/div')
    for i in range (2, len(list1)+1):
        if i in range (2, 6) or i in range (9, len(list1)+1):
            data_dict = {}
            try:
                name = driver.find_element(By.XPATH, f'/html/body/div[8]/div/div[2]/div[2]/div[1]/div/div[4]/div/div/div[1]/div/div[2]/div[1]/div/div[{i}]/div[2]/div/div/section/header').text
                firstName = name.split(" ")[0]
                middleName = name.split(" ")[1]
                lastName = name.split(" ")[2]
                print(name)
                image = driver.find_element(By.XPATH, f'/html/body/div[8]/div/div[2]/div[2]/div[1]/div/div[4]/div/div/div[1]/div/div[2]/div[1]/div/div[{i}]/div[1]/div/div/div/div/img').get_attribute("src")
                print(image)
                charges = driver.find_element(By.XPATH, f'/html/body/div[8]/div/div[2]/div[2]/div[1]/div/div[4]/div/div/div[1]/div/div[2]/div[1]/div/div[{i}]/div[2]/div/div/section/div[1]').text.strip()
                print(charges)
                additionalInfo = driver.find_element(By.XPATH, f'/html/body/div[8]/div/div[2]/div[2]/div[1]/div/div[4]/div/div/div[1]/div/div[2]/div[1]/div/div[{i}]/div[2]/div/div/section/div[2]/div/div').text.replace("\n", "")
                print(additionalInfo)
                summary = name + " is charged for " + charges
                
            except:
                try:
                    name = driver.find_element(By.XPATH, f'/html/body/div[8]/div/div[2]/div[2]/div[1]/div/div[4]/div/div/div[1]/div/div[2]/div[1]/div/div[{i}]/div/div/div[2]/section/header').text
                    firstName = name.split(" ")[0]
                    middleName = name.split(" ")[1]
                    lastName = name.split(" ")[2]
                    print(name)
                    image = driver.find_element(By.XPATH, f'/html/body/div[8]/div/div[2]/div[2]/div[1]/div/div[4]/div/div/div[1]/div/div[2]/div[1]/div/div[{i}]/div[1]/div/div/div/div/img').get_attribute("src")
                    print(image)
                    charges = driver.find_element(By.XPATH, f'/html/body/div[8]/div/div[2]/div[2]/div[1]/div/div[4]/div/div/div[1]/div/div[2]/div[1]/div/div[{i}]/div/div/div[2]/section/div[1]').text.strip()
                    print(charges)
                    additionalInfo = driver.find_element(By.XPATH, f'/html/body/div[8]/div/div[2]/div[2]/div[1]/div/div[4]/div/div/div[1]/div/div[2]/div[1]/div/div[{i}]/div/div/div[2]/section/div[2]/div/div').text.replace("\n", "")
                    print(additionalInfo)
                    summary = name + " is charged for " + charges

                except:
                    pass
            if name:
                data_dict['fullName'] = name
            if firstName:
                data_dict['firstName'] = firstName
            if middleName:
                data_dict['middleName'] = middleName
            if lastName:
                data_dict['lastName'] = lastName
            if charges:
                data_dict['charges'] = charges
            if image:
                data_dict['image'] = image
            if additionalInfo:
                data_dict['additionalInfo'] = additionalInfo
            if summary:
                data_dict['summary'] = summary
            data_list.append(data_dict)
            
        elif i == 6:
            for k in range (1, 3):
                data_dict2 = {}
                name = driver.find_element(By.XPATH, f'/html/body/div[8]/div/div[2]/div[2]/div[1]/div/div[4]/div/div/div[1]/div/div[2]/div[1]/div/div[6]/div/div[{k}]/div[2]/section/header').text
                print(name)
                try:
                    firstName = name.split(" ")[0]
                    middleName = name.split(" ")[1]
                    lastName = name.split(" ")[2]
                except:
                    try:
                        firstName = name.split(" ")[0]
                        lastName = name.split(" ")[1]
                        middleName = ""
                    except:
                        pass
                image = driver.find_element(By.XPATH, f'/html/body/div[8]/div/div[2]/div[2]/div[1]/div/div[4]/div/div/div[1]/div/div[2]/div[1]/div/div[6]/div/div[{k}]/div[1]/div/div/img').get_attribute("src")
                print(image)
                charges = driver.find_element(By.XPATH, f'/html/body/div[8]/div/div[2]/div[2]/div[1]/div/div[4]/div/div/div[1]/div/div[2]/div[1]/div/div[6]/div/div[{k}]/div[2]/section/div[1]').text
                print(charges)
                additionalInfo = driver.find_element(By.XPATH, f'/html/body/div[8]/div/div[2]/div[2]/div[1]/div/div[4]/div/div/div[1]/div/div[2]/div[1]/div/div[6]/div/div[{k}]/div[2]/section/div[2]/div/div').text.replace("\n", "")
                print(additionalInfo)
                summary = name + " is charged for " + charges
                if name:
                    data_dict2['fullName'] = name
                if firstName:
                    data_dict2['firstName'] = firstName
                if middleName:
                    data_dict2['middleName'] = middleName
                if lastName:
                    data_dict2['lastName'] = lastName
                if charges:
                    data_dict2['charges'] = charges
                if image:
                    data_dict2['image'] = image
                if additionalInfo:
                    data_dict2['additionalInfo'] = additionalInfo
                if summary:
                    data_dict2['summary'] = summary
                data_list.append(data_dict2)
        elif i == 7:
            for k in range (1, 4):
                data_dict3 = {}
                name = driver.find_element(By.XPATH, f'/html/body/div[8]/div/div[2]/div[2]/div[1]/div/div[4]/div/div/div[1]/div/div[2]/div[1]/div/div[7]/div/div[{k}]/div[2]/section/header').text
                print(name)
                try:
                    firstName = name.split(" ")[0]
                    middleName = name.split(" ")[1]
                    lastName = name.split(" ")[2]
                except:
                    try:
                        firstName = name.split(" ")[0]
                        lastName = name.split(" ")[1]
                        middleName = ""
                    except:
                        pass
                image = driver.find_element(By.XPATH, f'/html/body/div[8]/div/div[2]/div[2]/div[1]/div/div[4]/div/div/div[1]/div/div[2]/div[1]/div/div[7]/div/div[{k}]/div[1]/div/div/img').get_attribute("src")
                print(image)
                charges = driver.find_element(By.XPATH, f'/html/body/div[8]/div/div[2]/div[2]/div[1]/div/div[4]/div/div/div[1]/div/div[2]/div[1]/div/div[7]/div/div[{k}]/div[2]/section/div[1]').text
                print(charges)
                additionalInfo = driver.find_element(By.XPATH, f'/html/body/div[8]/div/div[2]/div[2]/div[1]/div/div[4]/div/div/div[1]/div/div[2]/div[1]/div/div[7]/div/div[{k}]/div[2]/section/div[2]/div/div').text.replace("\n", "")
                print(additionalInfo)
                summary = name + " is charged for " + charges
                if name:
                    data_dict3['fullName'] = name
                if firstName:
                    data_dict3['firstName'] = firstName
                if middleName:
                    data_dict3['middleName'] = middleName
                if lastName:
                    data_dict3['lastName'] = lastName
                if charges:
                    data_dict3['charges'] = charges
                if image:
                    data_dict3['image'] = image
                if additionalInfo:
                    data_dict3['additionalInfo'] = additionalInfo
                if summary:
                    data_dict3['summary'] = summary
                data_list.append(data_dict3)
        elif i == 8:
            for k in range (1, 5):
                data_dict4 = {}
                name = driver.find_element(By.XPATH, f'/html/body/div[8]/div/div[2]/div[2]/div[1]/div/div[4]/div/div/div[1]/div/div[2]/div[1]/div/div[8]/div/div[{k}]/div[2]/section/header').text
                print(name)
                try:
                    firstName = name.split(" ")[0]
                    middleName = name.split(" ")[1]
                    lastName = name.split(" ")[2]
                except:
                    try:
                        firstName = name.split(" ")[0]
                        lastName = name.split(" ")[1]
                        middleName = ""
                    except:
                        pass
                image = driver.find_element(By.XPATH, f'/html/body/div[8]/div/div[2]/div[2]/div[1]/div/div[4]/div/div/div[1]/div/div[2]/div[1]/div/div[8]/div/div[{k}]/div[1]/div/div/img').get_attribute("src")
                print(image)
                charges = driver.find_element(By.XPATH, f'/html/body/div[8]/div/div[2]/div[2]/div[1]/div/div[4]/div/div/div[1]/div/div[2]/div[1]/div/div[8]/div/div[{k}]/div[2]/section/div[1]').text
                print(charges)
                additionalInfo = driver.find_element(By.XPATH, f'/html/body/div[8]/div/div[2]/div[2]/div[1]/div/div[4]/div/div/div[1]/div/div[2]/div[1]/div/div[8]/div/div[{k}]/div[2]/section/div[2]/div/div').text.replace("\n", "")
                print(additionalInfo)
                summary = name + " is charged for " + charges
                if name:
                    data_dict4['fullName'] = name
                if firstName:
                    data_dict4['firstName'] = firstName
                if middleName:
                    data_dict4['middleName'] = middleName
                if lastName:
                    data_dict4['lastName'] = lastName
                if charges:
                    data_dict4['charges'] = charges
                if image:
                    data_dict4['image'] = image
                if additionalInfo:
                    data_dict4['additionalInfo'] = additionalInfo
                if summary:
                    data_dict4['summary'] = summary
                data_list.append(data_dict4)
    return data_list

if __name__ == '__main__':
    data_list = get_data("add_slug_name")
    to_json(data_list)



