
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
    url = "https://office.incometaxindia.gov.in/administration/Pages/tax-defaulters.aspx"
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
    k=1
    while k<=5:
        k+=1
        try:
            list1 = driver.find_elements(By.XPATH, f'//div/div/div/div/div[1]/div[4]/div[3]/h1/ul/li')
            for i in range(1, len(list1)+1):
                data_dict = {}
                familyInfo = ""
                companyInfo = ""
                assessmentYear = ""
                catAssessment =""
                incomeTaxAuthotiy =""
                dob =""
                incorporateDate = ""
                fullName = driver.find_element(By.XPATH, f'//div/div/div/div/div[1]/div[4]/div[3]/h1[{i}]/ul/li/span[1]').text
                print(fullName)
                if "(LATE)" in fullName:
                    familyInfo = fullName.split("(LATE)")[1]
                    fullName = fullName.split("(LATE)")[0]
                identifierType = "PAN"
                identifierID = driver.find_element(By.XPATH, f'//div/div/div/div/div[1]/div[4]/div[3]/h1[{i}]/ul/li/span[2]').text
                familyInfo =familyInfo + ", "+ driver.find_element(By.XPATH, f'//div/div/div/div/div[1]/div[4]/div[3]/h1[{i}]/ul/li/span[3]').text
                entityType = "Individual"
                if "DIRECTOR" in familyInfo:
                    entityType = "Organization"
                    companyInfo = familyInfo
                    familyInfo = ""
                tax = driver.find_element(By.XPATH, f'//div/div/div/div/div[1]/div[4]/div[3]/h1[{i}]/ul/li/span[4]').text
                try:
                    driver.find_element(By.XPATH, f'//div/div/div/div/div[1]/div[4]/div[3]/h1[{i}]/ul/li/span[4]').click()
                    time.sleep(3)
#                     list2 = driver.find_elements(By.XPATH, f'//div/div/div/div/div[1]/div[4]/div[3]/div/table/tbody/tr[1]/td[2]')
#                     print(len(list2))
#                     for j in range(1, len(list2)+1):
                    listOfAddress = "Last Known Address: " +  driver.find_element(By.XPATH, f'//div/div/div/div/div[1]/div[4]/div[3]/div[{i}]/table/tbody/tr[1]/td[2]').text.replace("\n", "")
                    print(listOfAddress)
                    if entityType == "Individual":
                        dob = driver.find_element(By.XPATH, f'//div/div/div/div/div[1]/div[4]/div[3]/div[{i}]/table/tbody/tr[2]/td[2]').text
#                             print(dob)
                    else:
                        incorporateDate = driver.find_element(By.XPATH, f'//div/div/div/div/div[1]/div[4]/div[3]/div[{i}]/table/tbody/tr[2]/td[2]').text
#                             print(incorporateDate)
                    income = driver.find_element(By.XPATH, f'//div/div/div/div/div[1]/div[4]/div[3]/div[{i}]/table/tbody/tr[3]/td[2]').text
                    income = income.replace("NOT AVAILABLE").strip()
                    print(income)
                    assessmentYear = driver.find_element(By.XPATH, f'//div/div/div/div/div[1]/div[4]/div[3]/div[{i}]/table/tbody/tr[4]/td[2]').text
                    print(assessmentYear)
                    catAssessment = driver.find_element(By.XPATH, f'//div/div/div/div/div[1]/div[4]/div[3]/div[{i}]/table/tbody/tr[5]/td[2]').text
                    incomeTaxAuthotiy = driver.find_element(By.XPATH, f'//div/div/div/div/div[1]/div[4]/div[3]/div[{i}]/table/tbody/tr[4]/td[4]').text
                    driver.find_element(By.XPATH, f'//div/div/div/div/div[1]/div[4]/div[3]/h1[{i}]/ul/li/span[4]').click()

                except:
                    pass
                if income != "":
                    additionalInfo = "Tax Arrear: " + tax + "; Last Known Source of Income: " + income + "; Assessment Year: " + assessmentYear + "; Category of Assessment: " + catAssessment + "; Income Tax Authority: " + incomeTaxAuthotiy
                else:
                    additionalInfo = "Tax Arrear: " + tax + "; Assessment Year: " + assessmentYear + "; Category of Assessment: " + catAssessment + "; Income Tax Authority: " + incomeTaxAuthotiy
                summary = fullName + " is an " + entityType + " present in the Tax Defaulters Individuals List with a Tax Arrear of " + tax
                if fullName:
                    data_dict['fullName'] = fullName
                if entityType:
                    data_dict['entityType'] = entityType
                if identifierType:
                    data_dict['identifierType'] = identifierType
                if identifierID:
                    data_dict['identifierID'] = identifierID
                if familyInfo:
                    data_dict['familyInfo'] = familyInfo
                if companyInfo:
                    data_dict['companyInfo'] = companyInfo
                if dob:
                    data_dict['dob'] = dob
                if incorporateDate:
                    data_dict['incorporateDate'] = incorporateDate
                if listOfAddress:
                    data_dict['listOfAddress'] = listOfAddress
                if additionalInfo:
                    data_dict['additionalInfo'] = additionalInfo
                if summary:
                    data_dict['summary'] = summary
                data_list.append(data_dict)
            driver.find_element(By.XPATH, f'/html/body/form/div[4]/div/div[9]/section/div/span/div[1]/div[3]/div[2]/div[1]/div/div/div/div/div[1]/div[4]/div[4]/table/tbody/tr/td/table/tbody/tr/td[4]/input').click()
        except Exception as e:
            print(e)
            break
    driver.quit()
    return data_list

if __name__ == '__main__':
    data_list = get_data("add_slug_name")
    to_json(data_list)


