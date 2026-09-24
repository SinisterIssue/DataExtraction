
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
    url = "https://www.gov.uk/government/publications/publishing-details-of-deliberate-tax-defaulters-pddd/current-list-of-deliberate-tax-defaulters"
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized") 
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--log-level=3")
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.headless = True
    translator = GoogleTranslator(target='english')
    driver = webdriver.Chrome(options=options)
    driver.maximize_window()
    driver.get(url)
    time.sleep(2)
    list1 = driver.find_elements(By.XPATH, f'/html/body/div[3]/main/div[2]/div[1]/div[3]/div/div/div/table')
    for i in range(1, len(list1)+1):
        list2 = driver.find_elements(By.XPATH, f'/html/body/div[3]/main/div[2]/div[1]/div[3]/div/div/div/table[{i}]/tbody/tr')
        print(len(list2))
        for j in range(1, len(list2)+1):
            list3 = driver.find_elements(By.XPATH, f'/html/body/div[3]/main/div[2]/div[1]/div[3]/div/div/div/table[{i}]/tbody/tr[{j}]/td')
            data_dict={}
            alias = ""
            other = ""
            for k in range(1, len(list3)+1):
                if k==1:
                    fullName = driver.find_element(By.XPATH, f'/html/body/div[3]/main/div[2]/div[1]/div[3]/div/div/div/table[{i}]/tbody/tr[{j}]/td[{k}]').text
                if k==2:
                    entityType = driver.find_element(By.XPATH, f'/html/body/div[3]/main/div[2]/div[1]/div[3]/div/div/div/table[{i}]/tbody/tr[{j}]/td[{k}]').text
                if k==3:
                    fullAddress = driver.find_element(By.XPATH, f'/html/body/div[3]/main/div[2]/div[1]/div[3]/div/div/div/table[{i}]/tbody/tr[{j}]/td[{k}]').text
                if k==4:
                    importantDates = driver.find_element(By.XPATH, f'/html/body/div[3]/main/div[2]/div[1]/div[3]/div/div/div/table[{i}]/tbody/tr[{j}]/td[{k}]').text
                if k==5:
                    tax = driver.find_element(By.XPATH, f'/html/body/div[3]/main/div[2]/div[1]/div[3]/div/div/div/table[{i}]/tbody/tr[{j}]/td[{k}]').text
                if k==6:
                    penalties = driver.find_element(By.XPATH, f'/html/body/div[3]/main/div[2]/div[1]/div[3]/div/div/div/table[{i}]/tbody/tr[{j}]/td[{k}]').text
                if k==7:
                    other = driver.find_element(By.XPATH, f'/html/body/div[3]/main/div[2]/div[1]/div[3]/div/div/div/table[{i}]/tbody/tr[{j}]/td[{k}]').text
            additionalInfo = "Total amount of tax/duty on which penalties are based: "+ tax + "; Total amount of penalties charged: "+ penalties
            other = other.strip()
            if other != "":
                print("here")
                try:
                    alias = other.split("‘")[1].split("’")[0]
                except:
                    pass
            summary = fullName + " is a " + entityType + " with " + additionalInfo
            if fullName:
                data_dict['fullName'] = fullName
                if alias:
                    data_dict['alias'] = alias
                if entityType:
                    data_dict['entityType'] = entityType
                if fullAddress:
                    data_dict['fullAddress'] = fullAddress
                if importantDates:
                    data_dict['importantDates'] = importantDates
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



