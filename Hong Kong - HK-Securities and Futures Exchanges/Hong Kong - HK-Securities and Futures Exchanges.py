
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
    url = "https://www.sfc.hk/en/About-the-SFC/Organisational-chart/Board-of-directors/Non-Executive-Directors"
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized") 
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--log-level=3")
    translator = GoogleTranslator(target='english')
    driver = webdriver.Chrome(options=options)
    driver.get(url)
    list1 = driver.find_elements(By.XPATH, f'/html/body/div[3]/div/div[2]/p/a')
    for i in range(1, len(list1)+1):
        data_dict = {}
        careerInfo =""
        title = ""
        educationInfo = ""
        name = driver.find_element(By.XPATH, f'/html/body/div[3]/div/div[2]/p[{i}]/a').text
        lastName = name.split(",", 1)[0].split("›", 1)[1]
    #     print(lastName)
        firstName = name.split(",")[1]
    #     print(firstName)
        fullName = firstName  + lastName
        fullName = fullName.title().strip()
        print(fullName)
        try:
            title = name.split(",", 2)[2].strip()
            print(title)
        except:
            pass
        driver.find_element(By.XPATH, f'/html/body/div[3]/div/div[2]/p[{i}]/a').click()
        time.sleep(2)
        image = driver.find_element(By.XPATH, f'/html/body/div[3]/div/div[2]/div[2]/div[1]/img').get_attribute('src')
        print(image)
        careerInfoStartDate = driver.find_element(By.XPATH, f'/html/body/div[3]/div/div[2]/div[2]/div[2]/div[2]').text
        careerInfoStartDate = careerInfoStartDate.split("From")[1].strip()
        print(careerInfoStartDate)
        careerInfoEndDate = driver.find_element(By.XPATH, f'/html/body/div[3]/div/div[2]/div[2]/div[2]/div[3]').text
        careerInfoEndDate = careerInfoEndDate.split("on")[1].strip()
        print(careerInfoEndDate)
        list2 = driver.find_elements(By.XPATH, f'/html/body/div[3]/div/div[2]/p')
        for j in range(1, len(list2)+1):
            info = driver.find_element(By.XPATH, f'/html/body/div[3]/div/div[2]/p[{j}]').text
            if "graduate" in info:
                educationInfo = info
            else:
                careerInfo = careerInfo + info
        lastUpdatedAt = careerInfo.split("Last update:")[1].strip()
        print(lastUpdatedAt)
        careerInfo = careerInfo.split("Last update:")[0]
        print(educationInfo)
        print(careerInfo)
        summary = fullName + " is one of the Non-Executive Directors of HK-Securities and Futures Exchanges."
        driver.back()
        print("*"*50)
        if fullName:
            data_dict['fullName'] = fullName
        if title:
            data_dict['title'] = title
        if image:
            data_dict['image'] = image
        if educationInfo:
            data_dict['educationInfo'] = educationInfo
        if careerInfo:
            data_dict['careerInfo'] = careerInfo
        if careerInfoStartDate:
            data_dict['careerInfoStartDate'] = careerInfoStartDate
        if careerInfoEndDate:
            data_dict['careerInfoEndDate'] = careerInfoEndDate
        if lastUpdatedAt:
            data_dict['lastUpdatedAt'] = lastUpdatedAt
        if summary:
            data_dict['summary'] = summary
        data_list.append(data_dict)
    driver.quit()
    return data_list


if __name__ == '__main__':
    data_list = get_data("add_slug_name")
    to_json(data_list)



