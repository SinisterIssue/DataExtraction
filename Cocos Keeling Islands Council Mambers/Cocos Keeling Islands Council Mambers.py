
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
    url = "https://shire.cc/en/your-council/meet-the-council.html"
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
    list1 = driver.find_elements(By.XPATH, f'/html/body/div[1]/div[2]/div[1]/div[3]/div[1]/div[2]/table[1]/tbody/tr')
    for i in range(1, len(list1)+1):

        list2 = driver.find_elements(By.XPATH, f'/html/body/div[1]/div[2]/div[1]/div[3]/div[1]/div[2]/table[1]/tbody/tr[{i}]/td')
        for j in range(1, len(list2)+1):
            data_dict = {}
            image = ""
            careerInfoDesignation =""
            try:
                image = driver.find_element(By.XPATH, f'/html/body/div[1]/div[2]/div[1]/div[3]/div[1]/div[2]/table[1]/tbody/tr[{i}]/td[{j}]/img').get_attribute('src')
            except:
                try:
                    image = driver.find_element(By.XPATH, f'/html/body/div[1]/div[2]/div[1]/div[3]/div[1]/div[2]/table[1]/tbody/tr[{i}]/td[{j}]/p/img').get_attribute('src')
                except:
                    pass
            try:
                fullName = driver.find_element(By.XPATH, f'/html/body/div[1]/div[2]/div[1]/div[3]/div[1]/div[2]/table[1]/tbody/tr[{i}]/td[{j}]/p[1]').text
                careerInfoDesignation = fullName.split("\n", 1)[1].split("\n", 1)[0]
                fullName = fullName.split("\n", 1)[0]
            except:
                try:
                    fullName = driver.find_element(By.XPATH, f'/html/body/div[1]/div[2]/div[1]/div[3]/div[1]/div[2]/table[1]/tbody/tr[{i}]/td[{j}]/strong').text
                    careerInfoDesignation = driver.find_element(By.XPATH, f'/html/body/div[1]/div[2]/div[1]/div[3]/div[1]/div[2]/table[1]/tbody/tr[{i}]/td[{j}]/em').text
                except:
                    pass
            print(fullName)
            print(image)
            print(careerInfoDesignation)
            try:
                emails = driver.find_element(By.XPATH, f'/html/body/div[1]/div[2]/div[1]/div[3]/div[1]/div[2]/table[1]/tbody/tr[{i}]/td[{j}]/p/span/a').text
            except:
                try:
                    emails = driver.find_element(By.XPATH, f'/html/body/div[1]/div[2]/div[1]/div[3]/div[1]/div[2]/table[1]/tbody/tr[{i}]/td[{j}]/span/a').text
                except:
                    pass
            try:
                careerInfoTerms = driver.find_element(By.XPATH, f'/html/body/div[1]/div[2]/div[1]/div[3]/div[1]/div[2]/table[1]/tbody/tr[{i}]/td[{j}]/p[2]').text
                careerInfoTerms = careerInfoTerms.split(":")[1].strip()
            except:
                try:
                    careerInfoTerms = driver.find_element(By.XPATH, f'/html/body/div[1]/div[2]/div[1]/div[3]/div[1]/div[2]/table[1]/tbody/tr[{i}]/td[{j}]/p').text
                    careerInfoTerms = careerInfoTerms.split(":")[1].strip()
                except:
                    try:
                        careerInfoTerms = driver.find_element(By.XPATH, f'/html/body/div[1]/div[2]/div[1]/div[3]/div[1]/div[2]/table[1]/tbody/tr[{i}]/td[{j}]').text
                        careerInfoTerms = careerInfoTerms.split(":")[1].strip()
                    except:
                        pass
            summary = fullName + " is the " + careerInfoDesignation + " in Cocos Keeling Islands Council for the term " + careerInfoTerms
            print("*"*50)
            if fullName.strip():
                data_dict['fullName'] = fullName
                if careerInfoDesignation:
                    data_dict['careerInfoDesignation'] = careerInfoDesignation
                if careerInfoTerms:
                    data_dict['careerInfoTerms'] = careerInfoTerms
                if image:
                    data_dict['image'] = image
                if emails:
                    data_dict['emails'] = emails
                if summary:
                    data_dict['summary'] = summary
                data_list.append(data_dict)

    list3 = driver.find_elements(By.XPATH, f'/html/body/div[1]/div[2]/div[1]/div[3]/div[1]/div[2]/table[2]/tbody/tr')
    for k in range(1, len(list3)+1):
        data_dict2 = {}
        fullName = driver.find_element(By.XPATH, f'/html/body/div[1]/div[2]/div[1]/div[3]/div[1]/div[2]/table[2]/tbody/tr[{k}]/td[1]').text.strip().title()
        careerInfoDesignation = driver.find_element(By.XPATH, f'/html/body/div[1]/div[2]/div[1]/div[3]/div[1]/div[2]/table[2]/tbody/tr[{k}]/td[2]').text
        summary = fullName + " is the " + careerInfoDesignation + " in Cocos Keeling Islands Council"
        if fullName:
            data_dict2['fullName'] = fullName
        if careerInfoDesignation:
            data_dict2['careerInfoDesignation'] = careerInfoDesignation
        if summary:
            data_dict2['summary'] = summary
        data_list.append(data_dict2)
    driver.quit()
    return data_list

if __name__ == '__main__':
    data_list = get_data("add_slug_name")
    to_json(data_list)


