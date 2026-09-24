
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
    url = "https://www.ssdt.org.uk/members/solicitor-members/"
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized") 
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--log-level=3")
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    translator = GoogleTranslator(target='english')
    driver = webdriver.Chrome(options=options)
    driver.maximize_window()
    driver.get(url)
    time.sleep(5)
    list1 = driver.find_elements(By.XPATH, f'/html/body/div[2]/div/div[5]/div/div/div[1]/div/div/div/div/h2')
    for i in range(2, len(list1)+1):
        data_dict = {}
        careerInfoDesignation = ""
        fullName = driver.find_element(By.XPATH, f'/html/body/div[2]/div/div[5]/div/div/div[1]/div/div[{i}]/div/div/h2').text
#         print(fullName)
        if "(" in fullName:
            careerInfoDesignation = fullName.split("(")[1].replace(")", "").strip()
            print(careerInfoDesignation)
            fullName = fullName.split("(")[0].strip()
        print(fullName)
        description = driver.find_element(By.XPATH, f'/html/body/div[2]/div/div[5]/div/div/div[1]/div/div[{i}]/div/div/div').text
        print(description)
        if careerInfoDesignation:
            summary = fullName + " is the " + careerInfoDesignation + " of the Scottish Solicitors Discipline Tribunal."
        else:
            summary = fullName + " is the " + description
        if fullName:
            data_dict['fullName'] = fullName
        if careerInfoDesignation:
            data_dict['careerInfoDesignation'] = careerInfoDesignation
        if description:
            data_dict['description'] = description
        if summary:
            data_dict['summary'] = summary
        data_list.append(data_dict)
    driver.quit()
    return data_list

if __name__ == '__main__':
    data_list = get_data("add_slug_name")
    to_json(data_list)
