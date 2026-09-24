
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
    url = "https://www.caa.co.uk/Our-work/About-us/CAA-board-and-staff/"
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
    list1 = driver.find_elements(By.XPATH, f'/html/body/main/div/div/div[1]/div/section/div/article')
    for i in range(1, len(list1)+1):
        list2 = driver.find_elements(By.XPATH, f'/html/body/main/div/div/div[1]/div/section/div/article[{i}]/article')
        careerInfoDesignation = ""
        image = ""
        
        for j in range(1, len(list2)+1):
            data_dict = {}
            info = driver.find_element(By.XPATH, f'/html/body/main/div/div/div[1]/div/section/div/article[{i}]/article[{j}]').text
            fullName = info.split("\n", 1)[0]
            print(fullName)
            info = info.split("\n", 1)[1]
            try:
                careerInfoDesignation = info.split("as", 1)[1].split(" in", 1)[0].strip()
                careerInfoDesignation = careerInfoDesignation.split("as ", 1)[1].split(" on ", 1)[0].strip()
            except:
                try:
                    careerInfoDesignation = info.split("became", 1)[1].split(" on ", 1)[0].strip()
                except:
                    try:
                        careerInfoDesignation = info.split("as ", 1)[1].split("in ", 1)[0].strip()
                    except:
                        pass
            if fullName == "Jonathan Spence":
                careerInfoDesignation = "General counsel and secretary"
            if fullName == "Tim Johnson":
                careerInfoDesignation = "Policy Director for the CAA"
            if fullName == "Sir Stephen Hillier":
                careerInfoDesignation = "Chair of the Civil Aviation Authority"
            careerInfoDesignation = careerInfoDesignation.replace("a ", "").replace("its ", "")
            print(careerInfoDesignation)
            careerInfo = info.replace("\n", " ")
            print(careerInfo)
            try:
                image = driver.find_element(By.XPATH, f'/html/body/main/div/div/div[1]/div/section/div/article[{i}]/article[{j}]/picture/img').get_attribute('src')
            except:
                pass
            print(image)
            summary = fullName + " is the " + careerInfoDesignation
            print("*"*50)
            if fullName:
                data_dict['fullName'] = fullName
            if careerInfoDesignation:
                data_dict['careerInfoDesignation'] = careerInfoDesignation
            if image:
                data_dict['image'] = image
            if careerInfo:
                data_dict['careerInfo'] = careerInfo
            if summary:
                data_dict['summary'] = summary
            data_list.append(data_dict)
    driver.quit()
    return data_list
    

if __name__ == '__main__':
    data_list = get_data("add_slug_name")
    to_json(data_list)



