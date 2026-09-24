
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
    url = "https://www.parliament.go.tz/index.php/mps-list"
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
    f=1
    while f<=20:
        f+=1
        print(f)
        try:
            list1 = driver.find_elements(By.XPATH, f'/html/body/div[4]/div[1]/div[2]/div/div[2]/div/table/tbody/tr')
            for i in range(1, len(list1)+1):
                data_dict = {}
                listOfCareerInfo = []
                educationInfo = ""
                link = driver.find_element(By.XPATH, f'/html/body/div[4]/div[1]/div[2]/div/div[2]/div/table/tbody/tr[{i}]/td[2]/a').get_attribute('href')
                driver.execute_script("window.open('');")
                driver.switch_to.window(driver.window_handles[1])
                driver.get(link)
                image = driver.find_element(By.XPATH, f'/html/body/div[4]/div[1]/div[2]/div[1]/img').get_attribute('src')
                fullName = driver.find_element(By.XPATH, f'/html/body/div[4]/div[1]/div[2]/h2').text
                print(fullName)
                list2 = driver.find_elements(By.XPATH, f'/html/body/div[4]/div[1]/div[2]/p')
                for j in range(1, len(list2)+1):
                    head = driver.find_element(By.XPATH, f'/html/body/div[4]/div[1]/div[2]/p[{j}]').text
                    if "Member" in head:
                        careerInfoDesignation = head.split(":")[1].strip()
                    if "Constituent" in head:
                        constituency = head.split(":")[1].strip()
                    if "Political" in head:
                        politicalParty = head.split(":")[1].strip()
                    if "Phone" in head:
                        telephoneNos = head.split(":")[1].strip()
                    if "P.O" in head:
                        fullAddress = head.split(":")[1].strip()
                    if "Email" in head:
                        emails = head.split(":")[1].strip()
                    if "Date" in head:
                        dob = head.split(":")[1].strip()
                        d = dob.split("-")[2]
                        m = dob.split("-")[1]
                        y = dob.split("-")[0]
                        dob = d+"/"+m+"/"+y
                        if dob== "00/00/000":
                            dob=""
                list3 = driver.find_elements(By.XPATH, f'/html/body/div[4]/div[1]/div[2]/table[1]/tbody/tr')
                for k in range(1, len(list3)+1):
                    university = driver.find_element(By.XPATH, f'/html/body/div[4]/div[1]/div[2]/table[1]/tbody/tr[{k}]/td[1]').text
                    course  = driver.find_element(By.XPATH, f'/html/body/div[4]/div[1]/div[2]/table[1]/tbody/tr[{k}]/td[2]').text
                    fromDate = driver.find_element(By.XPATH, f'/html/body/div[4]/div[1]/div[2]/table[1]/tbody/tr[{k}]/td[3]').text
                    toDate = driver.find_element(By.XPATH, f'/html/body/div[4]/div[1]/div[2]/table[1]/tbody/tr[{k}]/td[4]').text
                    level = driver.find_element(By.XPATH, f'/html/body/div[4]/div[1]/div[2]/table[1]/tbody/tr[{k}]/td[5]').text
                    educationInfo = educationInfo + "; Persued "+ level+" in " +course + " at " + university + " from " + fromDate + " - " + toDate 

                list4 = driver.find_elements(By.XPATH, f'/html/body/div[4]/div[1]/div[2]/table')
                for l in range(2, len(list4)+1):
                    list5 = driver.find_elements(By.XPATH, f'/html/body/div[4]/div[1]/div[2]/table[{l}]/tbody/tr')
                    for m in range(1, len(list5)+1):
                        temp_dict = {}
                        company = driver.find_element(By.XPATH, f'/html/body/div[4]/div[1]/div[2]/table[{l}]/tbody/tr[{m}]/td[1]').text
                        try:
                            position = driver.find_element(By.XPATH, f'/html/body/div[4]/div[1]/div[2]/table[{l}]/tbody/tr[{m}]/td[2]').text
                        except:
                            position = ""
                        startDate = driver.find_element(By.XPATH, f'/html/body/div[4]/div[1]/div[2]/table[{l}]/tbody/tr[{m}]/td[3]').text
                        endDate = driver.find_element(By.XPATH, f'/html/body/div[4]/div[1]/div[2]/table[{l}]/tbody/tr[{m}]/td[4]').text
                        if endDate=="To date":
                            endDate = ""
                        role = position + " at " + company
                        if role:
                            temp_dict['roles'] = role
                        if startDate:
                            temp_dict['startDate'] = startDate
                        if endDate:
                            temp_dict['endDate'] = endDate
                        listOfCareerInfo.append(temp_dict)
                summary = fullName + " is a part of the "+ politicalParty + " politicalParty and is a " + careerInfoDesignation 
                if fullName:
                    data_dict['fullName'] = fullName
                if image:
                    data_dict['image'] = image
                if careerInfoDesignation:
                    data_dict['careerInfoDesignation'] = careerInfoDesignation
                if constituency:
                    data_dict['constituency'] = constituency
                if politicalParty:
                    data_dict['politicalParty'] = politicalParty
                if telephoneNos:
                    data_dict['telephoneNos'] = telephoneNos
                if emails:
                    data_dict['emails'] = emails
                if fullAddress:
                    data_dict['fullAddress'] = fullAddress
                if educationInfo:
                    data_dict['educationInfo'] = educationInfo
                if listOfCareerInfo:
                    data_dict['listOfCareerInfo'] = listOfCareerInfo
                if summary:
                    data_dict['summary'] = summary
                data_list.append(data_dict)
                driver.close()
                driver.switch_to.window(driver.window_handles[0])
            driver.find_element(By.XPATH, f'/html/body/div[4]/div[1]/div[2]/div/div[3]/div[2]/div/ul/li[10]/a').click()
            time.sleep(2)
        except Exception as e:
            print(e)
            break
    driver.quit()
    return data_list

if __name__ == '__main__':
    data_list = get_data("add_slug_name")
    to_json(data_list)


