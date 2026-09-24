
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
    url = "https://www.parliament.nz/en/mps-and-electorates/members-of-parliament/"
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
    list1 = driver.find_elements(By.XPATH, f'/html/body/div[3]/div[1]/div[2]/div[1]/div/div[4]/div[3]/table/tbody/tr')
    for i in range(1, len(list1)+1):
        data_dict = {}
        listOfCareerInfo = []
        listOfCommitteeInfo = []
        driver.find_element(By.XPATH, f'/html/body/div[3]/div[1]/div[2]/div[1]/div/div[4]/div[3]/table/tbody/tr[{i}]').click()
        fullName = driver.find_element(By.XPATH, f'/html/body/div[3]/div[1]/div[1]/div[1]/h1').text
        lastUpdatedAt = driver.find_element(By.XPATH, f'/html/body/div[3]/div[1]/div[1]/div[1]/span').text.split(":")[1].strip()
        careerInfoDesignation = driver.find_element(By.XPATH, f'/html/body/div[3]/div[1]/div[1]/div[1]/div[4]/div[2]/h2[1]').text
        telephoneNos = "+64 4 817 9999"
        fullAddress = "Private Bag 18888, Parliament Buildings, Wellington 6160"
        try:
            politicalParty = careerInfoDesignation.split(",")[1].strip()
        except:
            politicalParty = ""
        careerInfoDesignation = careerInfoDesignation.split(",")[0].strip()
        try:
            careerInfoStartDate = driver.find_element(By.XPATH, f'/html/body/div[3]/div[1]/div[1]/div[1]/div[4]/div[2]/ul/li[1]').text.split(":")[1].strip()
        except:
            careerInfoStartDate = driver.find_element(By.XPATH, f'/html/body/div[3]/div[1]/div[1]/div[1]/div[4]/div[2]/div[1]/ul/li[1]').text.split(":")[1].strip()
        try:
            additionalInfo = driver.find_element(By.XPATH, f'/html/body/div[3]/div[1]/div[1]/div[1]/div[4]/div[2]/ul/li[2]').text
        except:
            additionalInfo = driver.find_element(By.XPATH, f'/html/body/div[3]/div[1]/div[1]/div[1]/div[4]/div[2]/div[1]/ul/li[2]').text
        try:
            image = driver.find_element(By.XPATH, f'/html/body/div[3]/div[1]/div[1]/div[1]/div[4]/div[1]/div[3]/img').get_attribute('src')
        except:
            pass
        summary = fullName + " is a part of the " + politicalParty + " and a " + careerInfoDesignation
        list2 = driver.find_elements(By.XPATH, f'/html/body/div[3]/div[1]/div[1]/div[1]/div[4]/div[2]/div/div/table/tbody/tr[1]')
        for j in range(1, len(list2)+1):
            list3 = driver.find_elements(By.XPATH, f'/html/body/div[3]/div[1]/div[1]/div[1]/div[4]/div[2]/div[{j}]/div/table/tbody/tr')
            for k in range(1, len(list3)+1):
                temp_dict={}
                role =""
                committeeName =""
                endDate = ""
                startDate = ""
                head = driver.find_element(By.XPATH, f'/html/body/div[3]/div[1]/div[1]/div[1]/div[4]/div[2]/div[{j}]/div/table/thead/tr/td[1]').text
                if head == "Member for / List":
                    member = driver.find_element(By.XPATH, f'/html/body/div[3]/div[1]/div[1]/div[1]/div[4]/div[2]/div[{j}]/div/table/tbody/tr[{k}]/td[1]').text
                    party = driver.find_element(By.XPATH, f'/html/body/div[3]/div[1]/div[1]/div[1]/div[4]/div[2]/div[{j}]/div/table/tbody/tr[{k}]/td[2]').text
                    if "List" in member:
                        role = "List of " + party
                    else:
                        role = "Member of "+ party + " - "+ member
                    startDate = driver.find_element(By.XPATH, f'/html/body/div[3]/div[1]/div[1]/div[1]/div[4]/div[2]/div[{j}]/div/table/tbody/tr[{k}]/td[3]').text.strip()
                    try:
                        endDate = driver.find_element(By.XPATH, f'/html/body/div[3]/div[1]/div[1]/div[1]/div[4]/div[2]/div[{j}]/div/table/tbody/tr[{k}]/td[4]').text.strip()
                    except:
                        pass
                elif head == "Parliamentary Role":
                    role = driver.find_element(By.XPATH, f'/html/body/div[3]/div[1]/div[1]/div[1]/div[4]/div[2]/div[{j}]/div/table/tbody/tr[{k}]/td[1]').text
                    startDate = driver.find_element(By.XPATH, f'/html/body/div[3]/div[1]/div[1]/div[1]/div[4]/div[2]/div[{j}]/div/table/tbody/tr[{k}]/td[2]').text
                elif head == "Party":
                    party = driver.find_element(By.XPATH, f'/html/body/div[3]/div[1]/div[1]/div[1]/div[4]/div[2]/div[{j}]/div/table/tbody/tr[{k}]/td[1]').text
                    role = driver.find_element(By.XPATH, f'/html/body/div[3]/div[1]/div[1]/div[1]/div[4]/div[2]/div[{j}]/div/table/tbody/tr[{k}]/td[2]').text
                    role = party + " - " + role
                    startDate = driver.find_element(By.XPATH, f'/html/body/div[3]/div[1]/div[1]/div[1]/div[4]/div[2]/div[{j}]/div/table/tbody/tr[{k}]/td[3]').text
                elif head == "Select Committee" or head == "Parliamentary Service Commission":
                    committeeName = driver.find_element(By.XPATH, f'/html/body/div[3]/div[1]/div[1]/div[1]/div[4]/div[2]/div[{j}]/div/table/tbody/tr[{k}]/td[1]').text
                    committeePosition = driver.find_element(By.XPATH, f'/html/body/div[3]/div[1]/div[1]/div[1]/div[4]/div[2]/div[{j}]/div/table/tbody/tr[{k}]/td[2]').text
                    committeeStartDate = driver.find_element(By.XPATH, f'/html/body/div[3]/div[1]/div[1]/div[1]/div[4]/div[2]/div[{j}]/div/table/tbody/tr[{k}]/td[3]').text
                else:
                    branch = driver.find_element(By.XPATH, f'/html/body/div[3]/div[1]/div[1]/div[1]/div[4]/div[2]/div[{j}]/div/table/tbody/tr[{k}]/td[1]').text
                    role = driver.find_element(By.XPATH, f'/html/body/div[3]/div[1]/div[1]/div[1]/div[4]/div[2]/div[{j}]/div/table/tbody/tr[{k}]/td[2]').text
                    role = role + " of " + branch
                    try:
                        startDate = driver.find_element(By.XPATH, f'/html/body/div[3]/div[1]/div[1]/div[1]/div[4]/div[2]/div[{j}]/div/table/tbody/tr[{k}]/td[3]').text 
                    except:
                        pass
                if role:
                    temp_dict['roles'] = role
                    if startDate:
                        temp_dict['startDate'] = startDate
                    if endDate:
                        temp_dict['endDate'] = endDate
                    listOfCareerInfo.append(temp_dict)
                if committeeName:
                    temp_dict['committeeName'] = committeeName
                    if committeePosition:
                        temp_dict['committeePosition'] = committeePosition
                    if committeeStartDate:
                        temp_dict['committeeStartDate'] = committeeStartDate
                    listOfCommitteeInfo.append(temp_dict)
        time.sleep(2)
        try:
            try:
                driver.find_element(By.XPATH, f'/html/body/div[3]/div[1]/div[1]/div[1]/div[4]/div[2]/div[7]/div/button').click()
            except:
                try:
                    driver.find_element(By.XPATH, f'/html/body/div[3]/div[1]/div[1]/div[1]/div[4]/div[2]/div[4]/div/button').click()
                    print("here4")
                except:
                    pass
            list4 = driver.find_elements(By.XPATH, f'/html/body/div[3]/div[1]/div[1]/div[1]/div[4]/div[2]/div[7]/div/div/div/div/div/table/tbody/tr[1]')
            if len(list4)==0:
                list4 = driver.find_elements(By.XPATH, f'/html/body/div[3]/div[1]/div[1]/div[1]/div[4]/div[2]/div[4]/div/div/div/div/div/table/tbody/tr[1]')
            print(len(list4))
            for l in range(1, len(list4)+1):
                list5 = driver.find_elements(By.XPATH, f'/html/body/div[3]/div[1]/div[1]/div[1]/div[4]/div[2]/div[7]/div/div/div/div[{l}]/div/table/tbody/tr')
                if len(list5)==0:
                    list5 = driver.find_elements(By.XPATH, f'/html/body/div[3]/div[1]/div[1]/div[1]/div[4]/div[2]/div[4]/div/div/div/div[{l}]/div/table/tbody/tr')
                print(len(list5))
                for m in range(1, len(list5)+1):
                    temp_dict={}
                    role =""
                    committeeName =""
                    try:
                        head = driver.find_element(By.XPATH, f'/html/body/div[3]/div[1]/div[1]/div[1]/div[4]/div[2]/div[4]/div/div/div/div[{l}]/div/table/thead/tr/td[1]/p').text
                        
                    except:
                        head = driver.find_element(By.XPATH, f'/html/body/div[3]/div[1]/div[1]/div[1]/div[4]/div[2]/div[7]/div/div/div/div[{l}]/div/table/thead/tr/td[1]/p').text
                    
                    if head == "Member for / List":
                        try:
                            member = driver.find_element(By.XPATH, f'/html/body/div[3]/div[1]/div[1]/div[1]/div[4]/div[2]/div[4]/div/div/div/div[{l}]/div/table/tbody/tr[{m}]/td[1]').text
                            party = driver.find_element(By.XPATH, f'/html/body/div[3]/div[1]/div[1]/div[1]/div[4]/div[2]/div[4]/div/div/div/div[{l}]/div/table/tbody/tr[{m}]/td[2]').text
                            startDate = driver.find_element(By.XPATH, f'/html/body/div[3]/div[1]/div[1]/div[1]/div[4]/div[2]/div[4]/div/div/div/div[{l}]/div/table/tbody/tr[{m}]/td[3]').text.strip()
                            endDate = driver.find_element(By.XPATH, f'/html/body/div[3]/div[1]/div[1]/div[1]/div[4]/div[2]/div[4]/div/div/div/div[{l}]/div/table/tbody/tr[{m}]/td[4]').text.strip()
                        except:
                            member = driver.find_element(By.XPATH, f'/html/body/div[3]/div[1]/div[1]/div[1]/div[4]/div[2]/div[7]/div/div/div/div[{l}]/div/table/tbody/tr[{m}]/td[1]').text
                            party = driver.find_element(By.XPATH, f'/html/body/div[3]/div[1]/div[1]/div[1]/div[4]/div[2]/div[7]/div/div/div/div[{l}]/div/table/tbody/tr[{m}]/td[2]').text
                            startDate = driver.find_element(By.XPATH, f'/html/body/div[3]/div[1]/div[1]/div[1]/div[4]/div[2]/div[7]/div/div/div/div[{l}]/div/table/tbody/tr[{m}]/td[3]').text.strip()
                            endDate = driver.find_element(By.XPATH, f'/html/body/div[3]/div[1]/div[1]/div[1]/div[4]/div[2]/div[7]/div/div/div/div[{l}]/div/table/tbody/tr[{m}]/td[4]').text.strip()
                        if "List" in member:
                            role = "List of " + party
                        else:
                            role = "Member of "+ party + " - "+ member

                    elif head == "Parliamentary Role":
                        try:
                            role = driver.find_element(By.XPATH, f'/html/body/div[3]/div[1]/div[1]/div[1]/div[4]/div[2]/div[4]/div/div/div/div[{l}]/div/table/tbody/tr[{m}]/td[1]').text
                            startDate = driver.find_element(By.XPATH, f'/html/body/div[3]/div[1]/div[1]/div[1]/div[4]/div[2]/div[4]/div/div/div/div[{l}]/div/table/tbody/tr[{m}]/td[2]').text
                            endDate = driver.find_element(By.XPATH, f'/html/body/div[3]/div[1]/div[1]/div[1]/div[4]/div[2]/div[4]/div/div/div/div[{l}]/div/table/tbody/tr[{m}]/td[3]').text
                        except:
                            role = driver.find_element(By.XPATH, f'/html/body/div[3]/div[1]/div[1]/div[1]/div[4]/div[2]/div[7]/div/div/div/div[{l}]/div/table/tbody/tr[{m}]/td[1]').text
                            startDate = driver.find_element(By.XPATH, f'/html/body/div[3]/div[1]/div[1]/div[1]/div[4]/div[2]/div[7]/div/div/div/div[{l}]/div/table/tbody/tr[{m}]/td[2]').text
                            endDate = driver.find_element(By.XPATH, f'/html/body/div[3]/div[1]/div[1]/div[1]/div[4]/div[2]/div[7]/div/div/div/div[{l}]/div/table/tbody/tr[{m}]/td[3]').text
                    elif head == "Party":
                        try:
                            party = driver.find_element(By.XPATH, f'/html/body/div[3]/div[1]/div[1]/div[1]/div[4]/div[2]/div[4]/div/div/div/div[{l}]/div/table/tbody/tr[{m}]/td[1]').text
                            role = driver.find_element(By.XPATH, f'/html/body/div[3]/div[1]/div[1]/div[1]/div[4]/div[2]/div[4]/div/div/div/div[{l}]/div/table/tbody/tr[{m}]/td[2]').text
                            startDate = driver.find_element(By.XPATH, f'/html/body/div[3]/div[1]/div[1]/div[1]/div[4]/div[2]/div[4]/div/div/div/div[{l}]/div/table/tbody/tr[{m}]/td[3]').text
                            endDate = driver.find_element(By.XPATH, f'/html/body/div[3]/div[1]/div[1]/div[1]/div[4]/div[2]/div[4]/div/div/div/div[{l}]/div/table/tbody/tr[{m}]/td[4]').text
                        except:
                            party = driver.find_element(By.XPATH, f'/html/body/div[3]/div[1]/div[1]/div[1]/div[4]/div[2]/div[7]/div/div/div/div[{l}]/div/table/tbody/tr[{m}]/td[1]').text
                            role = driver.find_element(By.XPATH, f'/html/body/div[3]/div[1]/div[1]/div[1]/div[4]/div[2]/div[7]/div/div/div/div[{l}]/div/table/tbody/tr[{m}]/td[2]').text
                            startDate = driver.find_element(By.XPATH, f'/html/body/div[3]/div[1]/div[1]/div[1]/div[4]/div[2]/div[7]/div/div/div/div[{l}]/div/table/tbody/tr[{m}]/td[3]').text
                            endDate = driver.find_element(By.XPATH, f'/html/body/div[3]/div[1]/div[1]/div[1]/div[4]/div[2]/div[7]/div/div/div/div[{l}]/div/table/tbody/tr[{m}]/td[4]').text
                        role = party + " - " + role
                    elif head == "Select Committee" or head == "Parliamentary Service Commission":
                        try:
                            committeeName = driver.find_element(By.XPATH, f'/html/body/div[3]/div[1]/div[1]/div[1]/div[4]/div[2]/div[4]/div/div/div/div[{l}]/div/table/tbody/tr[{m}]/td[1]').text
                            committeePosition = driver.find_element(By.XPATH, f'/html/body/div[3]/div[1]/div[1]/div[1]/div[4]/div[2]/div[4]/div/div/div/div[{l}]/div/table/tbody/tr[{m}]/td[2]').text
                            committeeStartDate = driver.find_element(By.XPATH, f'/html/body/div[3]/div[1]/div[1]/div[1]/div[4]/div[2]/div[4]/div/div/div/div[{l}]/div/table/tbody/tr[{m}]/td[3]').text
                            committeeEndDate = driver.find_element(By.XPATH, f'/html/body/div[3]/div[1]/div[1]/div[1]/div[4]/div[2]/div[4]/div/div/div/div[{l}]/div/table/tbody/tr[{m}]/td[4]').text
                        except:
                            committeeName = driver.find_element(By.XPATH, f'/html/body/div[3]/div[1]/div[1]/div[1]/div[4]/div[2]/div[7]/div/div/div/div[{l}]/div/table/tbody/tr[{m}]/td[1]').text
                            committeePosition = driver.find_element(By.XPATH, f'/html/body/div[3]/div[1]/div[1]/div[1]/div[4]/div[2]/div[7]/div/div/div/div[{l}]/div/table/tbody/tr[{m}]/td[2]').text
                            committeeStartDate = driver.find_element(By.XPATH, f'/html/body/div[3]/div[1]/div[1]/div[1]/div[4]/div[2]/div[7]/div/div/div/div[{l}]/div/table/tbody/tr[{m}]/td[3]').text
                            committeeEndDate = driver.find_element(By.XPATH, f'/html/body/div[3]/div[1]/div[1]/div[1]/div[4]/div[2]/div[7]/div/div/div/div[{l}]/div/table/tbody/tr[{m}]/td[4]').text
                    else:
                        try:
                            branch = driver.find_element(By.XPATH, f'/html/body/div[3]/div[1]/div[1]/div[1]/div[4]/div[2]/div[4]/div/div/div/div[{l}]/div/table/tbody/tr[{m}]/td[1]').text
                            role = driver.find_element(By.XPATH, f'/html/body/div[3]/div[1]/div[1]/div[1]/div[4]/div[2]/div[4]/div/div/div/div[{l}]/div/table/tbody/tr[{m}]/td[2]').text
                            startDate = driver.find_element(By.XPATH, f'/html/body/div[3]/div[1]/div[1]/div[1]/div[4]/div[2]/div[4]/div/div/div/div[{l}]/div/table/tbody/tr[{m}]/td[3]').text
                            endDate = driver.find_element(By.XPATH, f'/html/body/div[3]/div[1]/div[1]/div[1]/div[4]/div[2]/div[4]/div/div/div/div[{l}]/div/table/tbody/tr[{m}]/td[4]').text
                        except:
                            branch = driver.find_element(By.XPATH, f'/html/body/div[3]/div[1]/div[1]/div[1]/div[4]/div[2]/div[7]/div/div/div/div[{l}]/div/table/tbody/tr[{m}]/td[1]').text
                            role = driver.find_element(By.XPATH, f'/html/body/div[3]/div[1]/div[1]/div[1]/div[4]/div[2]/div[7]/div/div/div/div[{l}]/div/table/tbody/tr[{m}]/td[2]').text
                            startDate = driver.find_element(By.XPATH, f'/html/body/div[3]/div[1]/div[1]/div[1]/div[4]/div[2]/div[7]/div/div/div/div[{l}]/div/table/tbody/tr[{m}]/td[3]').text
                            endDate = driver.find_element(By.XPATH, f'/html/body/div[3]/div[1]/div[1]/div[1]/div[4]/div[2]/div[7]/div/div/div/div[{l}]/div/table/tbody/tr[{m}]/td[4]').text
                        role = role + " of " + branch    
                    if role:
                        temp_dict['roles'] = role
                        if startDate:
                            temp_dict['startDate'] = startDate
                        if endDate:
                            temp_dict['endDate'] = endDate
                        listOfCareerInfo.append(temp_dict)
                    if committeeName:
                        temp_dict['committeeName'] = committeeName
                        if committeePosition:
                            temp_dict['committeePosition'] = committeePosition
                        if committeeStartDate:
                            temp_dict['committeeStartDate'] = committeeStartDate
                        if committeeEndDate:
                            temp_dict['committeeEndDate'] = committeeEndDate
                        listOfCommitteeInfo.append(temp_dict)
        except Exception as e:
            print(e)
            pass
        
        if fullName:
            data_dict['fullName'] = fullName
        if image:
            data_dict['image'] = image
        if careerInfoDesignation:
            data_dict['careerInfoDesignation'] = careerInfoDesignation
        if careerInfoStartDate:
            data_dict['careerInfoStartDate'] = careerInfoStartDate
        if politicalParty:
            data_dict['politicalParty'] = politicalParty
        if telephoneNos:
            data_dict['telephoneNos'] = telephoneNos
        if fullAddress:
            data_dict['fullAddress'] = fullAddress
        if lastUpdatedAt:
            data_dict['lastUpdatedAt'] = lastUpdatedAt
        if additionalInfo:
            data_dict['additionalInfo'] = additionalInfo
        if listOfCareerInfo:
            data_dict['listOfCareerInfo'] = listOfCareerInfo
        if listOfCommitteeInfo:
            data_dict['listtOfCommitteInfo'] = listOfCommitteeInfo
        if summary:
            data_dict['summary'] = summary
        data_list.append(data_dict)
        driver.back()
        print("*"*50)
    driver.quit()
    return data_list


if __name__ == '__main__':
    data_list = get_data("add_slug_name")
    to_json(data_list)



