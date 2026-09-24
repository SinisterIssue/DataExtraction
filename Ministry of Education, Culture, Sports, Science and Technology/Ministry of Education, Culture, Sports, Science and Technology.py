
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
    url = "https://www.mext.go.jp/en/about/member/index.htm"
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized") 
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--log-level=3")
    translator = GoogleTranslator(target='english')
    driver = webdriver.Chrome(options=options)
    driver.get(url)
    list1 = driver.find_elements(By.XPATH, f'/html/body/div[2]/div[7]/div/div[1]/div[1]/div/div/div/div[1]/div[1]/div[1]/img')
    for i in range(1, len(list1)+1):
        data_dict = {}
        image = driver.find_element(By.XPATH, f'/html/body/div[2]/div[7]/div/div[1]/div[1]/div/div/div/div[1]/div[1]/div[1]/img').get_attribute('src')
        fullName = driver.find_element(By.XPATH, f'/html/body/div[2]/div[7]/div/div[1]/div[1]/div/div/div/div[1]/div/div[2]').text.title()
        fullName = fullName.replace("\nProfile", "")
        careerInfoDesignation = "Minister"
        summary = fullName + " is the " + careerInfoDesignation + " of Ministry of Education, Culture, Sports, Science and Technology."
        if fullName:
            data_dict['fullName'] = fullName
        if image:
            data_dict['image'] = image
        if careerInfoDesignation:
            data_dict['careerInfoDesignation'] = careerInfoDesignation
        if summary:
            data_dict['summary'] = summary
        data_list.append(data_dict)

    list2 = driver.find_elements(By.XPATH, f'/html/body/div[2]/div[7]/div/div[1]/div[1]/div/div/div/div/div[1]/div[1]/img')
    for j in range(1, len(list2)+1):
        data_dict2 = {}
        try:
            fullName = driver.find_element(By.XPATH, f'/html/body/div[2]/div[7]/div/div[1]/div[1]/div/div/div/div[2]/div[{j}]/div[2]').text.title()
            fullName = fullName.replace("\nProfile", "")
            image = driver.find_element(By.XPATH, f'/html/body/div[2]/div[7]/div/div[1]/div[1]/div/div/div/div[2]/div[{j}]/div/img').get_attribute('src')
            careerInfoDesignation = "State Minister"
            summary = fullName + " is the " + careerInfoDesignation + " of Ministry of Education, Culture, Sports, Science and Technology."
            if fullName:
                data_dict2['fullName'] = fullName
            if image:
                data_dict2['image'] = image
            if careerInfoDesignation:
                data_dict2['careerInfoDesignation'] = careerInfoDesignation
            if summary:
                data_dict2['summary'] = summary
            data_list.append(data_dict2)
        except:
            pass

    list3 = driver.find_elements(By.XPATH, f'/html/body/div[2]/div[7]/div/div[1]/div[1]/div/div/div/div[3]/div/div[1]/img')
    for k in range(1, len(list3)+1):
        try:
            data_dict3 = {}
            fullName = driver.find_element(By.XPATH, f'/html/body/div[2]/div[7]/div/div[1]/div[1]/div/div/div/div[3]/div[{k}]/div[2]').text.title()
            fullName = fullName.replace("\nProfile", "")
            image = driver.find_element(By.XPATH, f'/html/body/div[2]/div[7]/div/div[1]/div[1]/div/div/div/div[3]/div[{k}]/div/img').get_attribute('src')
            careerInfoDesignation = "Parliamentary Vice-Minister"
            summary = fullName + " is the " + careerInfoDesignation + " of Ministry of Education, Culture, Sports, Science and Technology."
            if fullName:
                data_dict3['fullName'] = fullName
            if image:
                data_dict3['image'] = image
            if careerInfoDesignation:
                data_dict3['careerInfoDesignation'] = careerInfoDesignation
            if summary:
                data_dict3['summary'] = summary
            data_list.append(data_dict3)
        except:
            pass
    driver.quit()
    return data_list


if __name__ == '__main__':
    data_list = get_data("add_slug_name")
    to_json(data_list)




