
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import json
import re
from deep_translator import GoogleTranslator
from selenium.webdriver.common.keys import Keys

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
    url = "https://www.nbs.sk/en/about-the-bank/bank-board-of-the-nbs"
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized") 
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--log-level=3")
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    # options.headless = True
    translator = GoogleTranslator(target='english')
    driver = webdriver.Chrome(options=options)
    driver.maximize_window()
    driver.get(url)
    list1 = driver.find_elements(By.XPATH, f'/html/body/div[3]/div[2]/div/div[1]/div/div')
    for i in range(2, len(list1)+1):
        list2 = driver.find_elements(By.XPATH, f'/html/body/div[3]/div[2]/div/div[1]/div/div[{i}]/div/div/div/div/p/a')
        for j in range(1, len(list2)+1):
            achievements = ""
            publicationUrl = ""
            languagesKnown = ""
            website = ""
            additionalInfo = ""
            listOfCareerInfo = []
            data_dict = {}
            try:
                driver.find_element(By.XPATH, f'/html/body/div[4]/div[1]/div/div[2]/button[1]').click()
            except:
                pass
            time.sleep(2)
            driver.find_element(By.XPATH, f'/html/body/div[3]/div[2]/div/div[1]/div/div[{i}]/div/div/div[{j}]/div/p/a').click()
            careerInfoDesignation = driver.find_element(By.XPATH, f'/html/body/div[3]/div[2]/div/div[1]/div/h1').text
            print(careerInfoDesignation)
            fullName = driver.find_element(By.XPATH, f'/html/body/div[3]/div[2]/div/div[1]/div/h2').text
            print(fullName)
            image = driver.find_element(By.XPATH, f'/html/body/div[3]/div[2]/div/div[1]/div/div[1]/figure/img').get_attribute('src')
            print(image)
            educationInfo = driver.find_element(By.XPATH, f'/html/body/div[3]/div[2]/div/div[1]/div/div[3]/div[2]/div/figure/table/tbody').text.replace("\n", " ", 1).replace("\n", "; ", 1).replace("\n", " ", 1)
            print(educationInfo)
            try:
                publicationUrl = driver.find_element(By.XPATH, f'/html/body/div[3]/div[2]/div/div[1]/div/div[5]/div[2]/div/figure/table/tbody/tr/td[2]/a').get_attribute('href')
                print(publicationUrl)
            except:
                pass
            list3 = driver.find_elements(By.XPATH, f'/html/body/div[3]/div[2]/div/div[1]/div/p')
            for k in range(1, len(list3)+1):
                info = driver.find_element(By.XPATH, f'/html/body/div[3]/div[2]/div/div[1]/div/p[{k}]').text
                if "Date of birth:" in info:
                    dob = info.split("Date of birth:")[1].split("\n", 1)[0].strip().replace(".", "")
                    print(dob)
                    placeOfBirthCity = info.split("Place of birth:")[1].split("\n", 1)[0].strip()
                    print(placeOfBirthCity)
                    careerInfoStartDate = info.split("Start of term of office:")[1].split("\n", 1)[0].strip().replace(".", "")
                    print(careerInfoStartDate)
                    careerInfoEndDate = info.split("End of term of office:")[1].split("\n", 1)[0].strip().replace(".", "")
                    print(careerInfoEndDate)
                elif "fluent" in info:
                    languagesKnown = info
                    print(languagesKnown)
                elif "Website" in info:
                    website = info
                    website = website.split("Website:")[1].replace("\n", "").strip()
                    print(website)
                elif "Award" in info or "award" in info:
                    achievements = achievements + " " + info
                else:
                    additionalInfo = additionalInfo + " " + info
            additionalInfo = additionalInfo.split("Additional")[1].replace("\n", " ").replace("information", "").strip()        
            print(additionalInfo)
            list4 = driver.find_elements(By.XPATH, f'/html/body/div[3]/div[2]/div/div[1]/div/div[4]/div[2]/div/figure/table/tbody/tr')
            
            designations = ""
            for l in range(1, len(list4)+1):
                terms = driver.find_element(By.XPATH, f'/html/body/div[3]/div[2]/div/div[1]/div/div[4]/div[2]/div/figure/table/tbody/tr[{l}]/td[1]').text
                temp_dict = {}
                startDate = ""
                startMonth = ""
                startYear = ""
                endYear =""
                if "Since" in terms:
                    if len(terms.split(" ")) ==4:
                        startDate = terms.split("Since ")[1]
                        startMonth = terms.split(" ")[2]
                        startYear = terms.split(" ")[3]
                        endYear = ""
                    if len(terms.split(" ")) ==2:
                        startYear = terms.split("Since")[1].strip()
                    if len(terms.split(" ")) ==3:
                        startMonth = terms.split(" ")[1]
                        startYear = terms.split(" ")[2]
                else:
                    print(terms.split("–"))
                    startYear = terms.split("–")[0].strip()
                    endYear = terms.split("–")[1].strip()
                roles = driver.find_element(By.XPATH, f'/html/body/div[3]/div[2]/div/div[1]/div/div[4]/div[2]/div/figure/table/tbody/tr[{l}]/td[2]').text.replace("\n", " ")
                if roles:
                    temp_dict['roles'] = roles
                if terms:
                    temp_dict['terms'] = terms
                if startDate:
                    temp_dict['startDate'] = startDate
                if startMonth:
                    temp_dict['startMonth'] = startMonth
                if startYear:
                    temp_dict['startYear'] = startYear
                if endYear:
                    temp_dict['endYear'] = endYear
                listOfCareerInfo.append(temp_dict)
            print(listOfCareerInfo)
            summary = fullName + " is the " + careerInfoDesignation + " of the NBS Bank"
            if fullName:
                data_dict['fullName'] = fullName
            if careerInfoDesignation:
                data_dict['careerInfoDesignation'] = careerInfoDesignation
            if careerInfoStartDate:
                data_dict['careerInfoStartDate'] = careerInfoStartDate
            if careerInfoEndDate:
                data_dict['careerInfoEndDate'] = careerInfoEndDate
            if image:
                data_dict['image'] = image
            if educationInfo:
                data_dict['educationInfo'] = educationInfo
            if publicationUrl:
                data_dict['publicationUrl'] = publicationUrl
            if dob:
                data_dict['dob'] = dob
            if placeOfBirthCity:
                data_dict['placeOfBirthCity']= placeOfBirthCity
            if languagesKnown:
                data_dict['languagesKnown'] = languagesKnown
            if website:
                data_dict['website'] = website
            if achievements:
                data_dict['achievements'] = achievements
            if additionalInfo:
                data_dict['additionalInfo'] = additionalInfo
            if listOfCareerInfo:
                data_dict['listOfCareerInfo'] = listOfCareerInfo
            if summary:
                data_dict['summary'] = summary
            data_list.append(data_dict)
            print("*"*50)
            driver.back()
    driver.quit()
    return data_list

if __name__ == '__main__':
    data_list = get_data("add_slug_name")
    to_json(data_list)



