
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
    url = "https://www.gikai.pref.fukuoka.lg.jp/giin/se-fukuokashi.html#01"
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized") 
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--log-level=3")
    translator = GoogleTranslator(target='english')
    driver = webdriver.Chrome(options=options)
    driver.get(url)
    list1 = driver.find_elements(By.XPATH, f'/html/body/div[2]/div[2]/div[2]/div/div/div[3]/table')
    for i in range(1, len(list1)+1):
        list2 = driver.find_elements(By.XPATH, f'/html/body/div[2]/div[2]/div[2]/div/div/div[3]/table[{i}]/tbody/tr')
        for j in range(2, len(list2)+1):
            data_dict = {}
            fullName = driver.find_element(By.XPATH, f'/html/body/div[2]/div[2]/div[2]/div/div/div[3]/table[{i}]/tbody/tr[{j}]/td[2]/a').text
            fullName = translator.translate(fullName)
            print(fullName)
            driver.find_element(By.XPATH, f'/html/body/div[2]/div[2]/div[2]/div/div/div[3]/table[{i}]/tbody/tr[{j}]/td[2]/a').click()
            time.sleep(2)
            try:
                image = driver.find_element(By.XPATH, f'/html/body/div[2]/div[2]/div[2]/div/div/div[3]/div/div/img').get_attribute('src')
                print(image)
            except:
                pass
            list3 = driver.find_elements(By.XPATH, f'/html/body/div[2]/div[2]/div[2]/div/div/div[3]/table/tbody/tr')
            for k in range(1, len(list3)+1):
                info = driver.find_element(By.XPATH, f'/html/body/div[2]/div[2]/div[2]/div/div/div[3]/table/tbody/tr[{k}]/th').text
                info = translator.translate(info)
#                 print(info)
                if "constituency" in info:
                    constituency = driver.find_element(By.XPATH, f'/html/body/div[2]/div[2]/div[2]/div/div/div[3]/table/tbody/tr[{k}]/td').text
                    constituency = translator.translate(constituency)
                    print(constituency)
                if "denomination" in info:
                    politicalParty = driver.find_element(By.XPATH, f'/html/body/div[2]/div[2]/div[2]/div/div/div[3]/table/tbody/tr[{k}]/td').text
                    politicalParty = translator.translate(politicalParty)
                    print(politicalParty)
                if "Winning times" in info:
                    win = driver.find_element(By.XPATH, f'/html/body/div[2]/div[2]/div[2]/div/div/div[3]/table/tbody/tr[{k}]/td').text
                    win = translator.translate(win)
                    print(win)
                if "Date of birth" in info:
                    dob = driver.find_element(By.XPATH, f'/html/body/div[2]/div[2]/div[2]/div/div/div[3]/table/tbody/tr[{k}]/td').text
                    dob = translator.translate(dob)
                    print(dob)
                if "committees" in info:
                    committee = driver.find_element(By.XPATH, f'/html/body/div[2]/div[2]/div[2]/div/div/div[3]/table/tbody/tr[{k}]/td').text
                    committee = translator.translate(committee)
                    print(committee)
                if "address" in info:
                    fullAddress = driver.find_element(By.XPATH, f'/html/body/div[2]/div[2]/div[2]/div/div/div[3]/table/tbody/tr[{k}]/td').text
                    fullAddress = translator.translate(fullAddress)
                    fullAddress = fullAddress.replace("\n", ", ")
                    print(fullAddress)
                if "phone number" in info:
                    telephoneNos = driver.find_element(By.XPATH, f'/html/body/div[2]/div[2]/div[2]/div/div/div[3]/table/tbody/tr[{k}]/td').text
                    telephoneNos = translator.translate(telephoneNos)
                    telephoneNos = telephoneNos.replace(" (Office)", "")
                    print(telephoneNos)
                if "fax number" in info:
                    fax = driver.find_element(By.XPATH, f'/html/body/div[2]/div[2]/div[2]/div/div/div[3]/table/tbody/tr[{k}]/td').text
                    fax = translator.translate(fax)
                    fax = fax.replace(" (Office)", "")
                    print(fax)
            additionalInfo = "Winning Times: " + win + "; Affiliated committees: " + committee
            summary = fullName + " is a representative of the " + politicalParty + ", belonging to the constituency of " + constituency
            if fullName:
                data_dict['fullName'] = fullName
            if image:
                data_dict['image'] = image
            if constituency:
                data_dict['constituency'] = constituency
            if politicalParty:
                data_dict['politicalParty'] = politicalParty
            if dob:
                data_dict['dob'] = dob
            if fullAddress:
                data_dict['fullAddress'] = fullAddress
            if telephoneNos:
                data_dict['telephoneNos'] = telephoneNos
            if fax:
                data_dict['fax'] = fax
            if additionalInfo:
                data_dict['additionalInfo'] = additionalInfo
            if summary:
                data_dict['summary'] = summary
            data_list.append(data_dict)

            driver.back()
    driver.quit()
    return data_list

if __name__ == '__main__':
    data_list = get_data("add_slug_name")
    to_json(data_list)




