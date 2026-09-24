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
    url = "https://www.india.gov.in/my-government/whos-who/governors"
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
    list1 = driver.find_elements(By.XPATH, f'/html/body/div[1]/main/div[2]/div/section/div/div/div/div/div[2]/div/div/div/div/div/div[2]/table/tbody/tr')
    for i in range(1, len(list1)+1):
        list2 = driver.find_elements(By.XPATH, f'/html/body/div[1]/main/div[2]/div/section/div/div/div/div/div[2]/div/div/div/div/div/div[2]/table/tbody/tr[{i}]/td')
        data_dict = {}
        for j in range(1, len(list2)+1):
            if j==1:
                state = driver.find_element(By.XPATH, f'/html/body/div[1]/main/div[2]/div/section/div/div/div/div/div[2]/div/div/div/div/div/div[2]/table/tbody/tr[{i}]/td[{j}]').text
            if j==2:
                fullName = driver.find_element(By.XPATH, f'/html/body/div[1]/main/div[2]/div/section/div/div/div/div/div[2]/div/div/div/div/div/div[2]/table/tbody/tr[{i}]/td[{j}]').text
                referenceUrls = driver.find_element(By.XPATH, f'/html/body/div[1]/main/div[2]/div/section/div/div/div/div/div[2]/div/div/div/div/div/div[2]/table/tbody/tr[{i}]/td[{j}]/a').get_attribute('href') 
        careerInfoDesignation = "Governor of " + state
        summary = fullName + " is the governor of " + state
        if fullName:
            data_dict['fullName'] = fullName
        if state:
            data_dict['state'] = state
        if careerInfoDesignation:
            data_dict['careerInfoDesignation'] = careerInfoDesignation
        if referenceUrls:
            data_dict['referenceUrls'] = referenceUrls
        if summary:
            data_dict['summary'] = summary
        data_list.append(data_dict)
    driver.quit()
    return data_list


if __name__ == '__main__':
    data_list = get_data("add_slug_name")
    to_json(data_list)

