
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
    with open("data_dict1.json", "w") as outfile:
        json.dump(data, outfile,indent=4)
        outfile.close()


def get_data(slug_name):
    data_list = []
    url = "https://risp.ri.gov/mostwanted"
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized") 
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--log-level=3")
    translator = GoogleTranslator(target='english')
    driver = webdriver.Chrome(options=options)
    driver.get(url)
    list1 = driver.find_elements(By.XPATH, f'/html/body/div[1]/main/div[1]/div[2]/article/div')
    # print(len(list1))
    for i in range(2, len(list1)+1):
        data_dict = {}
        identifierType = ""
        fullName =  driver.find_element(By.XPATH, f'/html/body/div[1]/main/div[1]/div[2]/article/div[{i}]/div[1]/h3').text
        print(fullName)
        try:
            image = driver.find_element(By.XPATH, f'/html/body/div[1]/main/div[1]/div[2]/article/div[{i}]/div[2]/div[1]/div[2]/div/div/figure[3]/img').get_attribute('src')
            print(image)
        except:
            try:
                image = driver.find_element(By.XPATH, f'/html/body/div[1]/main/div[1]/div[2]/article/div[{i}]/figure/img').get_attribute('src')
                print(image)
            except:
                pass
        info = driver.find_element(By.XPATH, f'/html/body/div[1]/main/div[1]/div[2]/article/div[{i}]/div[1]/p[1]').text
        dob = info.split("D.O.B:")[1].split("\n", 1)[0].strip()
        d = dob.split("/")[1]
        m = dob.split("/")[0]
        y = dob.split("/")[2]
        dob = d+ "/" + m + "/" + y
        print(dob)
        race = info.split("Race/Ethnicity:")[1].split("\n", 1)[0].strip()
        print(race)
        gender = info.split("Sex:")[1].split("\n", 1)[0].strip()
        print(gender)
        height = info.split("Height:")[1].split("\n", 1)[0].strip()
        print(height)
        weight = info.split("Weight:")[1].split("\n", 1)[0].strip()
        print(weight)
        hair = info.split("Hair:")[1].split("\n", 1)[0].strip()
        print(hair)
        eyes = info.split("Eyes:")[1].split("\n", 1)[0].strip()
        print(eyes)
        try:
            riSID = info.split("RI - SID:")[1].split("\n", 1)[0].strip()
            identifierType = "RI - SID: " + riSID
            print(identifierType)
        except:
            pass
        address = info.split("Last Known Address:")[1].split("\n", 1)[0].strip()
        listOfAddress = "Last Known Address: " + address
        print(listOfAddress)
        alias = info.split("Alias Name/D.O.B:")[1].split("\n", 1)[0].strip()
        print(alias)
        remarks = info.split("Remarks:")[1].split("\n", 1)[0].strip()
        print(remarks)
        info2 = driver.find_element(By.XPATH, f'/html/body/div[1]/main/div[1]/div[2]/article/div[{i}]/div/p[2]').text
        charges = info2.split("Charges:")[1].split("\n", 1)[0].strip()
        print(charges)
        agency = info2.split("Originating Agency:")[1].split("\n", 1)[0].strip()
        print(agency)
        history = info2.split("History:")[1].split("\n", 1)[0].strip()
        print(history)
        status = info2.split("Status:")[1].split("\n", 1)[0].strip()
        print(status)
        if remarks =="":
            additionalInfo = "Originating Agency: "+ agency + "; History: " + history
        else:
            additionalInfo = "Remarks: " + remarks + "; Originating Agency: "+ agency + "; History: " + history
        summary = fullName + " is charged with charges " + charges
        if fullName:
            data_dict['fullName'] = fullName
        if image:
            data_dict['image'] = image
        if dob:
            data_dict['dob'] = dob
        if race:
            data_dict['race'] = race
        if gender:
            data_dict['gender'] = gender
        if height:
            data_dict['height'] = height
        if weight:
            data_dict['weight'] = weight
        if hair:
            data_dict['hair'] = hair
        if eyes:
            data_dict['eyes'] = eyes
        if identifierType:
            data_dict['identifierType'] = identifierType
        if alias:
            data_dict['alias'] = alias
        if listOfAddress:
            data_dict['listOfAddress'] = listOfAddress
        if charges:
            data_dict['charges'] = charges
        if status:
            data_dict['status'] = status
        if additionalInfo:
            data_dict['additionalInfo'] = additionalInfo
        if summary:
            data_dict['summary'] = summary
        data_list.append(data_dict)
    driver.quit()
    return data_list


if __name__ == '__main__':
    data_list = get_data("add_slug_name")
    to_json(data_list)



