
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
    url = "https://www.president.ir/en/president/cabinet//"
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized") 
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--log-level=3")
    translator = GoogleTranslator(target='english')
    driver = webdriver.Chrome(options=options)
    driver.get(url)
    data_dict = {}
    fullName = driver.find_element(By.XPATH, f'/html/body/form/center/div/div/div/div/div[2]/div/div/div/div[1]/a/div/h2').text
    careerInfoDesignation = driver.find_element(By.XPATH, f'/html/body/form/center/div/div/div/div/div[2]/div/div/div/div[1]/a/div/h3').text
    image = driver.find_element(By.XPATH, f'/html/body/form/center/div/div/div/div/div[2]/div/div/div/div[1]/a/img').get_attribute('src')
    summary = fullName + " is the " + careerInfoDesignation
    if fullName:
        data_dict['fullName'] = fullName
    if careerInfoDesignation:
        data_dict['careerInfoDesignation'] = careerInfoDesignation+ " of Iran."
    if image:
        data_dict['image'] = image
    if summary:
        data_dict['summary'] = summary
    data_list.append(data_dict)
    list1 = driver.find_elements(By.XPATH, f'/html/body/form/center/div/div/div/div/div[2]/div/div/div/div[2]/div/div/div/a/img')
    print(len(list1))
    for i in range(1, len(list1)+1):
        data_dict2 = {}
        fullName = driver.find_element(By.XPATH, f'/html/body/form/center/div/div/div/div/div[2]/div/div/div/div/div/div/div[{i}]/p[2]').text
        careerInfoDesignation = driver.find_element(By.XPATH, f'/html/body/form/center/div/div/div/div/div[2]/div/div/div/div/div/div/div[{i}]/p[1]').text
        image = driver.find_element(By.XPATH, f'/html/body/form/center/div/div/div/div/div[2]/div/div/div/div[2]/div/div/div[{i}]/a/img').get_attribute('src')
        summary = fullName + " is the " + careerInfoDesignation+ " of Iran."
        if fullName:
            data_dict2['fullName'] = fullName
        if careerInfoDesignation:
            data_dict2['careerInfoDesignation'] = careerInfoDesignation
        if image:
            data_dict2['image'] = image
        if summary:
            data_dict2['summary'] = summary
        data_list.append(data_dict2)

    list2 = driver.find_elements(By.XPATH, f'/html/body/form/center/div/div/div/div/div[2]/div/div/div/div[3]/div/div/div/p[1]')
    print(len(list2))
    for j in range(1, len(list2)+1):
        data_dict3 = {}
        fullName = driver.find_element(By.XPATH, f'/html/body/form/center/div/div/div/div/div[2]/div/div/div/div[3]/div/div/div[{j}]/p[2]').text
        careerInfoDesignation = driver.find_element(By.XPATH, f'/html/body/form/center/div/div/div/div/div[2]/div/div/div/div[3]/div/div/div[{j}]/p[1]').text
        try:
            image = driver.find_element(By.XPATH, f'/html/body/form/center/div/div/div/div/div[2]/div/div/div/div[3]/div/div/div[{i}]/a/img').get_attribute('src')
        except:
            pass
        summary = fullName + " is the " + careerInfoDesignation + " of Iran."
        if fullName:
            data_dict3['fullName'] = fullName
        if careerInfoDesignation:
            data_dict3['careerInfoDesignation'] = careerInfoDesignation
        if image:
            data_dict3['image'] = image
        if summary:
            data_dict3['summary'] = summary
        data_list.append(data_dict3)
    driver.quit()
    return data_list

if __name__ == '__main__':
    data_list = get_data("add_slug_name")
    to_json(data_list)



