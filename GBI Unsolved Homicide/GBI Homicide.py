
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
    url = "https://gbi.georgia.gov/cases/unsolved-homicide"
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized") 
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--log-level=3")
    translator = GoogleTranslator(target='english')
    driver = webdriver.Chrome(options=options)
    driver.get(url)
    while True:
        try:
            list1 = driver.find_elements(By.XPATH, f'/html/body/div[1]/div/div[2]/div/div[3]/div[1]/div/div/div[2]/span/div/table/tbody/tr/td[1]/div/a')
            for i in range(1, len(list1)+1):
                data_dict = {}
                data_dict2 = {}
                data_dict3 ={}
                height = ""
                weight = ""
                race = ""
                gender = ""
                age = ""
                crimeDescription = ""
                crimeLocation = ""
                image = ""
                hair = ""
                alias = ""
                policeStation = ""
                nextName = ""
                newName = ""
                dateOfIncident = driver.find_element(By.XPATH, f'/html/body/div/div/div[2]/div/div[3]/div[1]/div/div/div[2]/span/div/table/tbody/tr[{i}]/td[8]/div').text
#                 fullName = driver.find_element(By.XPATH, f'/html/body/div[1]/div/div[2]/div/div[3]/div[1]/div/div/div[2]/span/div/table/tbody/tr[{i}]/td[1]/div/a').text
                types = "Unsolved Homicide"
#                 print(fullName)
                try:
                    image = driver.find_element(By.XPATH, f'/html/body/div[1]/div/div[2]/div/div[3]/div[1]/div/div/div[2]/span/div/table/tbody/tr[{i}]/td[2]/div/img').get_attribute("src")
                    print(image)
                except:
                    pass
                driver.find_element(By.XPATH, f'/html/body/div[1]/div/div[2]/div/div[3]/div[1]/div/div/div[2]/span/div/table/tbody/tr[{i}]/td[1]/div/a').click()
                time.sleep(2)
                fullName = driver.find_element(By.XPATH, f'/html/body/div/div/div[2]/div/div[3]/div[1]/div/div/div/h2/div').text
                if fullName == "William (Bill) Francis Greenwood":
                    alias = "Bill"
                if fullName == "Anthony Lee Dye, Sr.":
                    fullName = "Anthony Lee Dye Sr."
                if "Dean Marie" in fullName:
                    alias = fullName.split("aka", 1)[1].split("0", 1)[0].strip()
                    fullName = fullName.split("aka", 1)[0]
                fullName = fullName.replace('"', '').replace('"', '').replace("(Bill)", "")
                if fullName == "1980 Morgan County Murder":
                    fullName = ""
                if "Homicide" in fullName:
                    fullName = ""
#                 print(fullName)
                if fullName == "Robert M. Woody and Patricia A. Woody":
                    nextName = fullName.split(" and")[1].strip()
                    print(nextName)
                    fullName = fullName.split(" and")[0].strip()
                if fullName == "Jose Luis Gaitan, Ramon Obino, Juan Camacho Recendes, and Nabor Recendes":
                    newName = fullName.split(",", 1)[1].replace("and", "").strip()
                    fullName = fullName.split(",", 1)[0].strip()
                    print(newName)
                print(fullName)
                info = driver.find_element(By.XPATH, f'/html/body/div[1]/div/div[2]/div/div[3]/div[1]/div/main/div/div[2]').text
                if "Contact Info" in info:
                    policeStation = info.split(":",1)[1]
                    info = driver.find_element(By.XPATH, f'/html/body/div[1]/div/div[2]/div/div[3]/div[1]/div/main/div/div[1]').text
                if "Case Info" not in info:
                    info = driver.find_element(By.XPATH, f'/html/body/div/div/div[2]/div/div[3]/div[1]/div/main/div/div[1]').text
                try:
                    race = info.split("Race:")[1].split("\n", 1)[0].strip()
                    print(race)
                except:
                    pass
                try:
                    gender = info.split("Sex:")[1].split("\n", 1)[0].strip()
                    print(gender)
                except:
                    pass
                try:
                    age = info.split("Age:")[1].split("\n", 1)[0].strip().replace("Newborn", "").split("(", 1)[0].strip()
                    print(age)
                except:
                    pass
                try:
                    hair = info.split("Hair Color:")[1].split("\n", 1)[0].strip()
                except:
                    pass
                try:
                    crimeLocation = info.split("Location:")[1].split("\n", 1)[0].strip()
                    print(crimeLocation)
                except:
                    pass
                try:
                    height = info.split("Height:")[1].split("\n", 1)[0].strip()
                    print(height)
                except:
                    pass
                try:
                    weight = info.split("Weight:")[1].split("\n", 1)[0].strip()
                    print(weight)
                except:
                    pass
                try:
                    crimeDescription = driver.find_element(By.XPATH, f'/html/body/div[1]/div/div[2]/div/div[3]/div[1]/div/main/div/div[4]').text.replace("\n", "")
                except:
                    pass
                if fullName.split(" ", 1)[0] not in crimeDescription:
                    try:
                        crimeDescription = driver.find_element(By.XPATH, f'/html/body/div/div/div[2]/div/div[3]/div[1]/div/main/div/div[3]').text.replace("\n", " ")
                        if fullName == "Laneshia Crowder":
                            crimeDescription = driver.find_element(By.XPATH, f'/html/body/div/div/div[2]/div/div[3]/div[1]/div/main/div/div[4]').text.replace("\n", " ")
                    except:
                        pass
                if "GBI" not in policeStation:
                    try:
                        policeStation = driver.find_element(By.XPATH, f'/html/body/div[1]/div/div[2]/div/div[3]/div[1]/div/main/div/div[3]').text
                    except:
                        pass
                if ":" in policeStation:
                    policeStation = policeStation.split(":", 1)[1].strip()
                print("*"*50)
                summary = fullName + " is involved in " + types
                driver.back()
                if fullName:
                    data_dict['fullName'] = fullName
                    if alias:
                        data_dict['alias'] = alias
                    if dateOfIncident:
                        data_dict['dateOfIncident'] = dateOfIncident
                    if types:
                        data_dict['type'] = types
                    if image:
                        data_dict['image'] = image
                    if race:
                        data_dict['race'] = race
                    if hair:
                        data_dict['hair'] = hair
                    if gender:
                        data_dict['gender'] = gender
                    if age:
                        data_dict['age'] = age
                    if crimeLocation:
                        data_dict['crimeLocation'] = crimeLocation
                    if height:
                        data_dict['height'] = height
                    if weight:
                        data_dict['weight'] = weight
                    if crimeDescription:
                        data_dict['crimeDescription'] = crimeDescription
                    if policeStation:
                        data_dict['policeStation'] = policeStation
                    if summary:
                        data_dict['summary'] = summary
                    data_list.append(data_dict)
                if nextName:
                    print(nextName)
                    data_dict2['fullName'] = nextName
                    if alias:
                        data_dict2['alias'] = alias
                    if dateOfIncident:
                        data_dict2['dateOfIncident'] = dateOfIncident
                    if types:
                        data_dict2['type'] = types
                    if image:
                        data_dict2['image'] = image
                    if race:
                        data_dict2['race'] = race
                    if hair:
                        data_dict2['hair'] = hair
                    if gender:
                        data_dict2['gender'] = gender
                    if age:
                        data_dict2['age'] = age
                    if crimeLocation:
                        data_dict2['crimeLocation'] = crimeLocation
                    if height:
                        data_dict2['height'] = height
                    if weight:
                        data_dict2['weight'] = weight
                    if crimeDescription:
                        data_dict2['crimeDescription'] = crimeDescription
                    if policeStation:
                        data_dict2['policeStation'] = policeStation
                    if summary:
                        summary = nextName + " is involved in " + types
                        data_dict2['summary'] = summary
                    data_list.append(data_dict2)
                if newName:
                    newName = newName.split(",")
                    print(newName)
                    for j in range(0, len(newName)):
                        nextName = newName[j]
                        data_dict3 = {}
                        if nextName:
                            data_dict3['fullName'] = nextName.strip()
                            if alias:
                                data_dict3['alias'] = alias
                            if dateOfIncident:
                                data_dict3['dateOfIncident'] = dateOfIncident
                            if types:
                                data_dict3['type'] = types
                            if image:
                                data_dict3['image'] = image
                            if race:
                                data_dict3['race'] = race
                            if hair:
                                data_dict3['hair'] = hair
                            if gender:
                                data_dict3['gender'] = gender
                            if age:
                                data_dict3['age'] = age
                            if crimeLocation:
                                data_dict3['crimeLocation'] = crimeLocation
                            if height:
                                data_dict3['height'] = height
                            if weight:
                                data_dict3['weight'] = weight
                            if crimeDescription:
                                data_dict3['crimeDescription'] = crimeDescription
                            if policeStation:
                                data_dict3['policeStation'] = policeStation
                            if summary:
                                summary = nextName + " is involved in " + types
                                data_dict3['summary'] = summary
                            data_list.append(data_dict3)
            driver.find_element(By.LINK_TEXT, f'next').click()
        except Exception as e:
            print(e)
            break
            
    driver.quit()
    return data_list

if __name__ == '__main__':
    data_list = get_data("add_slug_name")
    to_json(data_list)



