
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
    url = "https://www.tax.newmexico.gov/about-us/administrative-services-division/"
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
    for i in range(3, 5):
        data_dict = {}
        fullName = driver.find_element(By.XPATH, f'/html/body/div[1]/div/div/div/article/div/div/div/div[2]/div/div[2]/div/div/div[{i}]/div[2]/h4').text
        image = driver.find_element(By.XPATH, f'/html/body/div[1]/div/div/div/article/div/div/div/div[2]/div/div[2]/div/div/div[{i}]/div[1]/img').get_attribute('src')
        careerInfoDesignation = driver.find_element(By.XPATH, f'/html/body/div[1]/div/div/div/article/div/div/div/div[2]/div/div[2]/div/div/div[{i}]/div[2]/p').text
        telephoneNos = driver.find_element(By.XPATH, f'/html/body/div[1]/div/div/div/article/div/div/div/div[2]/div/div[2]/div/div/div[{i}]/div[2]/div/p[1]/a/span').text
        description = driver.find_element(By.XPATH, f'/html/body/div[1]/div/div/div/article/div/div/div/div[2]/div/div[2]/div/div/div[{i}]/div[2]/div').text
        summary = description.split("\n")[1]
        description = description.split("\n", 1)[1].replace("\n", "")
    #     print(summary)
    #     print(description)
        if fullName:
            data_dict['fullName'] = fullName
        if careerInfoDesignation:
            data_dict['careerInfoDesignation'] = careerInfoDesignation
        if image:
            data_dict['image'] = image
        if description:
            data_dict['description'] = description
        if telephoneNos:
            data_dict['telephoneNos'] = telephoneNos
        if summary:
            data_dict['summary'] = summary
        data_list.append(data_dict)

    info = driver.find_element(By.XPATH, f'/html/body/div[1]/div/div/div/article/div/div/div/div[2]/div/div[2]/div/div/div[5]').text.split("Bureau\n")
    for j in range(0, len(info)):
        if "Links" in info[j]:
            info[j] = info[j].split("Links")[0].split("\nThe ", 1)[0]
        else:
            info[j] = info[j].split("\nThe", 1)[0]
    info.pop(0)
    for k in range(0, len(info)):
        data_dict = {}
        telephoneNos = info[k].split("\n")[1].strip()
        fullName = info[k].split("\n")[0].strip().split("Chief")[1].split(",")[0].strip()
        print(fullName)
        print(telephoneNos)
        if fullName == "Manoj Shah":
            careerInfoDesignation = "Bureau Chief of Budget Bureau"
        elif fullName == "Elise Mignardot":
            careerInfoDesignation = "Bureau Chief of Financial Distribution Bureau"
        elif fullName == "Arianna Burger":
            careerInfoDesignation = "Bureau Chief of Financial Services Bureau"
        elif fullName == "Amanda Maez":
            careerInfoDesignation = "Bureau Chief of General Services Bureau"
        elif fullName == "Karen Spehar":
            careerInfoDesignation = "Bureau Chief of Human Resources Bureau"
        summary = fullName + " is the " + careerInfoDesignation + " of Administrative Services Division"
        if fullName:
            data_dict['fullName'] = fullName
        if careerInfoDesignation:
            data_dict['careerInfoDesignation'] = careerInfoDesignation
        if telephoneNos:
            data_dict['telephoneNos'] = telephoneNos
        if summary:
            data_dict['summary'] = summary
        data_list.append(data_dict)
    driver.quit()
    return data_list


if __name__ == '__main__':
    data_list = get_data("add_slug_name")
    to_json(data_list)


