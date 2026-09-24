
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import json
import re

def to_json(data):
    """
    This function takes list of dictionary as Input and 
    then Creates a JSON file in which Input data is stored
    """
    with open("data_dict.json", "w") as outfile:
        json.dump(data, outfile,indent=4)
        outfile.close()


data_list = []
url = "https://www.parliament.bg/en/MP"
options = webdriver.ChromeOptions()
options.add_argument("--start-maximized") 
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument("--log-level=3")


def get_data(slug_name):
    driver = webdriver.Chrome(options=options)
    driver.get(url)
    time.sleep(2)
    driver.find_element(By.XPATH, f'/html/body/div/nav/div/ul/li[2]/a').click()
    time.sleep(2)
    list1 = driver.find_elements(By.XPATH, f'/html/body/div/main/div/div/div[2]/div[2]/div/div[2]/div[1]/p/div[2]/div/div[2]/a')
    for i in range(1, len(list1)+1):
        careerInfo = ""
        additionalInfo = ""
        placeOfBirthCity =""
        placeOfBirthCountry=""
        languagesKnown =""
        telephoneNos = ""
        data_dict = {}
        listOfCareerInfo = []
        fullName = driver.find_element(By.XPATH, f'/html/body/div/main/div/div/div[2]/div[2]/div/div[2]/div[1]/p/div[2]/div[{i}]/div[2]/a').text.title()
        print(fullName)
        careerInfoDesignation = driver.find_element(By.XPATH, f'/html/body/div/main/div/div/div[2]/div[2]/div/div[2]/div[1]/p/div[2]/div[{i}]/div[2]/div[1]').text
        print(careerInfoDesignation)
        link = driver.find_element(By.XPATH, f'/html/body/div/main/div/div/div[2]/div[2]/div/div[2]/div[1]/p/div[2]/div[{i}]/div[2]/a').get_attribute("href")
        driver.execute_script("window.open('');")
        driver.switch_to.window(driver.window_handles[1])
        driver.get(link)
        time.sleep(2)
        image = driver.find_element(By.XPATH, f'/html/body/div/main/div/div/div[2]/div[1]/div/div[1]/img').get_attribute("src")
        print(image)
        list2 = driver.find_elements(By.XPATH, f'/html/body/div/main/div/div/div[2]/div[1]/div/div[2]/ul/li')
        for j in range(1, len(list2)+1):
            headings = driver.find_element(By.XPATH, f'/html/body/div/main/div/div/div[2]/div[1]/div/div[2]/ul/li[{j}]').text
            if "Date of birth " in headings:
                dob = driver.find_element(By.XPATH, f'/html/body/div/main/div/div/div[2]/div[1]/div/div[2]/ul/li[{j}]').text
                dob = dob.split(":")[1].strip()
                if "," in dob:
                    placeOfBirthCity = dob.split(",")[1].strip()
                    try:
                        placeOfBirthCountry = dob.split(",")[2].strip()
                    except:
                        pass
                    dob = dob.split(",")[0].strip()
                print(dob)
            elif "Profession: " in headings:
                profession = driver.find_element(By.XPATH, f'/html/body/div/main/div/div/div[2]/div[1]/div/div[2]/ul/li[{j}]').text
                profession = profession.split(":")[1].strip()
                if profession != "":
                    additionalInfo = "Profession: " + profession + "; " + additionalInfo
            elif "Languages: " in headings:
                languagesKnown = driver.find_element(By.XPATH, f'/html/body/div/main/div/div/div[2]/div[1]/div/div[2]/ul/li[{j}]').text
                languagesKnown = languagesKnown.split(":")[1].strip()
                print(languagesKnown)
            elif "Political force: " in headings:
                politicalForce = driver.find_element(By.XPATH, f'/html/body/div/main/div/div/div[2]/div[1]/div/div[2]/ul/li[{j}]').text
                politicalForce = politicalForce.split(":")[1].strip()
                politicalParty = politicalForce.split(",")[0].strip()
                if politicalForce != "":
                    additionalInfo = "Political Force: "+  politicalForce + "; " + additionalInfo
            elif "E-mail: " in headings:
                emails = driver.find_element(By.XPATH, f'/html/body/div/main/div/div/div[2]/div[1]/div/div[2]/ul/li[{j}]').text
                emails = emails.split(":")[1].strip()
            elif "Phone:: " in headings:
                telephoneNos = driver.find_element(By.XPATH, f'/html/body/div/main/div/div/div[2]/div[1]/div/div[2]/ul/li[{j}]').text
                telephoneNos = telephoneNos.split("::")[1].strip()
            elif "Member of the previos NA:" in headings:
                members = driver.find_element(By.XPATH, f'/html/body/div/main/div/div/div[2]/div[1]/div/div[2]/ul/li[{j}]').text
                members = members.split(":")[1].strip()
                members = members.replace(";", ",")
                if members != "":
                    additionalInfo = "Member of the previos NA: " + members + "; " + additionalInfo

        print(additionalInfo)

        info = []
        careerInfo = driver.find_element(By.XPATH, f'/html/body/div/main/div/div/div[2]/div[2]/div/div[2]/div/p/ul').text.split("\n")
        print(range(0, len(careerInfo)-2))
        for k in range(0, len(careerInfo)-3, 2):
            info.append(careerInfo[k]+"; " + careerInfo[k+1])
#             print(info)
        for l in range(0, len(info)):
            temp_dict = {}
            startDate = ""
            endDate = ""
            terms = info[l].split(";")[1].strip()
            roles = info[l].split(";")[0].strip()
            startDate = terms.split("-")[0].strip()
            endDate = terms.split("-")[1].strip()
            if roles:
                temp_dict['roles'] = roles
            if terms:
                temp_dict['terms'] = terms
            if startDate:
                temp_dict['startDate'] = startDate
            if endDate:
                temp_dict['endDate'] = endDate
            listOfCareerInfo.append(temp_dict)
        summary = fullName + " is the " + careerInfoDesignation + " of the German Parliament " + "and belongs to the political party " + politicalParty
        print("*"*50)
        driver.close()
        driver.switch_to.window(driver.window_handles[0])
        if fullName:
            data_dict['fullName'] = fullName
        if careerInfoDesignation:
            data_dict['careerInfoDesignation'] = careerInfoDesignation
        if politicalParty:
            data_dict['politicalParty'] = politicalParty
        if image:
            data_dict['image'] = image
        if dob:
            data_dict['dob'] = dob
        if placeOfBirthCity:
            data_dict['placeOfBirthCity'] = placeOfBirthCity
        if placeOfBirthCountry:
            data_dict['placeOfBirthCountry'] = placeOfBirthCountry
        if languagesKnown:
            data_dict['languagesKnown'] = languagesKnown
        if emails:
            data_dict['emails'] = emails
        if telephoneNos:
            data_dict['telephoneNos'] = telephoneNos
        if listOfCareerInfo:
            data_dict['listOfCareerInfo'] = listOfCareerInfo
        if additionalInfo:
            data_dict['additionalInfo'] = additionalInfo
        if summary:
            data_dict['summary'] = summary
        data_list.append(data_dict)
    return data_list


if __name__ == '__main__':
    data_list = get_data("add_slug_name")
    to_json(data_list)


