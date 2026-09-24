
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
    with open("data_dict_directors.json", "w") as outfile:
        json.dump(data, outfile,indent=4)
        outfile.close()

def get_data(slug_name):
    data_list = []
    url = "https://www.iiroc.ca/about-iiroc"
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
    for i in range(3, 5):
        list1 = driver.find_elements(By.XPATH, f'/html/body/div[2]/div[1]/div[1]/div[2]/div/article/div/div[2]/div/nav/ul/li[{i}]/ul/li')
        print(len(list1))
        for j in range(1, len(list1)+1):
            data_dict = {}
            educationInfo = ""
            careerInfo = ""
            description = ""
            driver.find_element(By.XPATH, f'/html/body/div[2]/div[1]/div[1]/div[2]/div/article/div/div[2]/div/nav/ul/li[{i}]/ul/li[{j}]/a').click()
            time.sleep(2)
            fullName = driver.find_element(By.XPATH, f'/html/body/div[2]/div[1]/div[1]/div[2]/div[3]/div/div').text
            print(fullName)
            if "(" in fullName:
                fullName = fullName.split("(")[0].strip()
            careerInfoDesignation = driver.find_element(By.XPATH, f'/html/body/div[2]/div[1]/div[1]/div[2]/div[4]/div/article/div/div/div/div[1]/h2/div').text
            print(careerInfoDesignation)
            image = driver.find_element(By.XPATH, f'/html/body/div[2]/div[1]/div[1]/div[2]/div[4]/div/article/div/div/div/div[1]/div/div/div[1]/div/article/div/div/img').get_attribute('src')
            print(image)
            list2 = driver.find_elements(By.XPATH, f'/html/body/div[2]/div[1]/div[1]/div[2]/div[4]/div/article/div/div/div/div[1]/div/div/div[2]/div/p')
            for k in range(1, len(list2)+1):
                info = driver.find_element(By.XPATH, f'/html/body/div[2]/div[1]/div[1]/div[2]/div[4]/div/article/div/div/div/div[1]/div/div/div[2]/div/p[{k}]').text
                if "University" in info or "holds an" in info:
                    educationInfo = educationInfo + "; " + info
                else:
                    careerInfo = careerInfo + "; " + info
            educationInfo = educationInfo.replace("; ", "", 1)
            careerInfo = careerInfo.replace("; ", "", 1)
            print(educationInfo)
            print(careerInfo)
            if careerInfo.strip() == "":
                description = educationInfo
                educationInfo = ""
                careerInfo = ""
            if i==3:
                summary = fullName + " is in the Executive Management Team and is the " + careerInfoDesignation
            if i==4:
                summary = fullName + " is one of the Board of Directors and is the " + careerInfoDesignation
            driver.back()
            print("*"*50)
            if fullName:
                data_dict['fullName'] = fullName
            if careerInfoDesignation:
                data_dict['careerInfoDesignation'] = careerInfoDesignation
            if image:
                data_dict['image'] = image
            if careerInfo:
                data_dict['careerInfo'] = careerInfo
            if description:
                data_dict['description'] = description
            if educationInfo:
                data_dict['educationInfo'] = educationInfo
            if summary:
                data_dict['summary'] = summary
            data_list.append(data_dict)
    driver.quit()
    return data_list


if __name__ == '__main__':
    data_list = get_data("add_slug_name")
    to_json(data_list)


