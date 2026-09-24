
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
    url = "https://www.govtrack.us/congress/members/current"
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
    time.sleep(3)
    try:
        driver.find_element(By.XPATH, f'/html/body/div[3]/div/div/div[3]/button').click()
    except:
        pass
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        time.sleep(1)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        new_height = driver.execute_script("return document.body.scrollHeight")

        if new_height == last_height:
            break
        last_height = new_height

    list1 = driver.find_elements(By.XPATH, f'/html/body/div[1]/div[4]/div[2]/section/div/div[2]/a')
    print(len(list1))
    for i in range(1, len(list1)+1):
        try:
            data_dict = {}
            referenceUrls = ""
            website = ""
            careerInfoDesignation = ""
            careerInfoStartDate = ""
            careerInfoEndDate =""
            careerInfo = ""
            description = ""
            alias = ""
            image = ""
            twitterUrl = ""
            link = driver.find_element(By.XPATH, f'/html/body/div[1]/div[4]/div[2]/section/div/div[2]/a[{i}]').get_attribute("href")
            driver.execute_script("window.open('');")
            driver.switch_to.window(driver.window_handles[1])
            driver.get(link)
            fullName = driver.find_element(By.XPATH, f'/html/body/div[1]/div[4]/div/div[1]/h1').text
            title = fullName.split(".", 1)[0]
            fullName = fullName.split(".", 1)[1].strip()
            if '“' in fullName:
                firstName = fullName.split('“')[0].strip()
                lastName = fullName.split('” ')[1]
                alias = fullName.split('“')[1].split("”")[0].strip()
                fullName = firstName + " " + lastName
            print(fullName)
            print(alias)
            careerInfoDesignation = driver.find_element(By.XPATH, f'/html/body/div[1]/div[4]/div/div[1]/p[1]').text
            print(careerInfoDesignation)
            try:
                image = driver.find_element(By.XPATH, f'/html/body/div[1]/div[5]/div/div[2]/div/div[1]/div[3]/div[2]/img').get_attribute('src')
                print(image)
            except:
                pass
            try:
                list2 = driver.find_elements(By.XPATH, f'/html/body/div[1]/div[5]/div/div[1]/div/div[1]/div/a')
            except:
                try:
                    list2 = driver.find_elements(By.XPATH, f'/html/body/div[1]/div[5]/div/div[1]/div/div[1]/div/a')
                except:
                    pass
            for j in range(1, len(list2)+1):
                try:
                    heading = driver.find_element(By.XPATH, f'/html/body/div[1]/div[5]/div/div[1]/div/div[1]/div/a[{j}]').text
                except:
                    try:
                        heading = driver.find_element(By.XPATH, f'/html/body/div[1]/div[5]/div/div[1]/div/div[1]/div/a[{j}]').text
                    except:
                        pass
                if "Website" in heading:
                    website = driver.find_element(By.XPATH, f'/html/body/div[1]/div[5]/div/div[1]/div/div[1]/div/a[{j}]').get_attribute('href')
                    print(website)
                elif "@" in heading:
                    twitterUrl = driver.find_element(By.XPATH, f'/html/body/div[1]/div[5]/div/div[1]/div/div[1]/div/a[{j}]').get_attribute('href')
                elif "Website" not in heading or "@" not in heading:
                    referenceUrls = driver.find_element(By.XPATH, f'/html/body/div[1]/div[5]/div/div[1]/div/div[1]/div/a[{j}]').get_attribute('href') + "; " + referenceUrls
            print(referenceUrls)
            summary = driver.find_element(By.XPATH, f'/html/body/div[1]/div[5]/div/div[2]/div/div[1]/div[1]/div/p[1]').text.replace("(view map)", "")
            try:
                careerInfoStartDate = summary.split("served since")[1].split(".", 1)[0].strip()
                print(careerInfoStartDate)
            except:
                pass
            careerInfoEndDate = summary.split("serves until")[1].replace(".", "").strip()
            print(careerInfoEndDate)
            try:
                description = driver.find_element(By.XPATH, f'/html/body/div[1]/div[5]/div/div[2]/div/div[1]/div[1]/div[2]/div').text
            except:
                pass
            try:
                careerInfo = driver.find_element(By.XPATH, f'/html/body/div[1]/div[5]/div/div[2]/div/div[1]/div[1]/div/p[2]').text
            except:
                pass

            driver.close()
            driver.switch_to.window(driver.window_handles[0])
            if fullName:
                data_dict['fullName'] = fullName
            if alias:
                data_dict['alias'] = alias
            if title:
                data_dict['title'] = title
            if careerInfoDesignation:
                data_dict['careerInfoDesignation'] = careerInfoDesignation
            if description:
                data_dict['description'] = description
            if image:
                data_dict['image'] = image
            if careerInfo:
                data_dict['careerInfo'] = careerInfo
            if careerInfoStartDate:
                data_dict['careerInfoStartDate'] = careerInfoStartDate
            if careerInfoEndDate:
                data_dict['careerInfoEndDate'] = careerInfoEndDate
            if website:
                data_dict['website'] = website
            if twitterUrl:
                data_dict['twitterUrl'] = twitterUrl
            if referenceUrls:
                data_dict['referenceUrls'] = referenceUrls
            if summary:
                data_dict['summary'] = summary
            data_list.append(data_dict)
            print("*"*50)
        except Exception as e:
            print(e)
            pass
    for k in range(1, 1550):
        try:
            data_dict2 = {}
            referenceUrls = ""
            website = ""
            careerInfoDesignation = ""
            careerInfoStartDate = ""
            careerInfoEndDate =""
            careerInfo = ""
            description = ""
            alias = ""
            image = ""
            twitterUrl = ""
            link = driver.find_element(By.XPATH, f'/html/body/div[1]/div[4]/div[2]/section/div/div[2]/div[{k}]/a').get_attribute("href")
            driver.execute_script("window.open('');")
            driver.switch_to.window(driver.window_handles[1])
            driver.get(link)
            fullName = driver.find_element(By.XPATH, f'/html/body/div[1]/div[4]/div/div[1]/h1').text
            title = fullName.split(".", 1)[0]
            fullName = fullName.split(".", 1)[1].strip()
            if '“' in fullName:
                firstName = fullName.split('“')[0].strip()
                lastName = fullName.split('” ')[1]
                alias = fullName.split('“')[1].split("”")[0].strip()
                fullName = firstName + " " + lastName
            print(fullName)
            print(alias)
            careerInfoDesignation = driver.find_element(By.XPATH, f'/html/body/div[1]/div[4]/div/div[1]/p[1]').text
            print(careerInfoDesignation)
            try:
                image = driver.find_element(By.XPATH, f'/html/body/div[1]/div[5]/div/div[2]/div/div[1]/div[3]/div[2]/img').get_attribute('src')
                print(image)
            except:
                pass
            try:
                list2 = driver.find_elements(By.XPATH, f'/html/body/div[1]/div[5]/div/div[1]/div/div[1]/div/a')
            except:
                try:
                    list2 = driver.find_elements(By.XPATH, f'/html/body/div[1]/div[5]/div/div[1]/div/div[1]/div/a')
                except:
                    pass
            for j in range(1, len(list2)+1):
                try:
                    heading = driver.find_element(By.XPATH, f'/html/body/div[1]/div[5]/div/div[1]/div/div[1]/div/a[{j}]').text
                except:
                    try:
                        heading = driver.find_element(By.XPATH, f'/html/body/div[1]/div[5]/div/div[1]/div/div[1]/div/a[{j}]').text
                    except:
                        pass
                if "Website" in heading:
                    website = driver.find_element(By.XPATH, f'/html/body/div[1]/div[5]/div/div[1]/div/div[1]/div/a[{j}]').get_attribute('href')
                    print(website)
                elif "@" in heading:
                    twitterUrl = driver.find_element(By.XPATH, f'/html/body/div[1]/div[5]/div/div[1]/div/div[1]/div/a[{j}]').get_attribute('href')
                elif "Website" not in heading or "@" not in heading:
                    referenceUrls = driver.find_element(By.XPATH, f'/html/body/div[1]/div[5]/div/div[1]/div/div[1]/div/a[{j}]').get_attribute('href') + "; " + referenceUrls
            print(referenceUrls)
            summary = driver.find_element(By.XPATH, f'/html/body/div[1]/div[5]/div/div[2]/div/div[1]/div[1]/div/p[1]').text.replace("(view map)", "")
            try:
                careerInfoStartDate = summary.split("served since")[1].split(".", 1)[0].strip()
                print(careerInfoStartDate)
            except:
                pass
            careerInfoEndDate = summary.split("serves until")[1].replace(".", "").strip()
            print(careerInfoEndDate)
            try:
                description = driver.find_element(By.XPATH, f'/html/body/div[1]/div[5]/div/div[2]/div/div[1]/div[1]/div[2]/div').text
            except:
                pass
            try:
                careerInfo = driver.find_element(By.XPATH, f'/html/body/div[1]/div[5]/div/div[2]/div/div[1]/div[1]/div/p[2]').text
            except:
                pass

            driver.close()
            driver.switch_to.window(driver.window_handles[0])
            if fullName:
                data_dict2['fullName'] = fullName
            if alias:
                data_dict2['alias'] = alias
            if title:
                data_dict2['title'] = title
            if careerInfoDesignation:
                data_dict2['careerInfoDesignation'] = careerInfoDesignation
            if description:
                data_dict2['description'] = description
            if image:
                data_dict2['image'] = image
            if careerInfo:
                data_dict2['careerInfo'] = careerInfo
            if careerInfoStartDate:
                data_dict2['careerInfoStartDate'] = careerInfoStartDate
            if careerInfoEndDate:
                data_dict2['careerInfoEndDate'] = careerInfoEndDate
            if website:
                data_dict2['website'] = website
            if twitterUrl:
                data_dict2['twitterUrl'] = twitterUrl
            if referenceUrls:
                data_dict2['referenceUrls'] = referenceUrls
            if summary:
                data_dict2['summary'] = summary
            data_list.append(data_dict2)
        except:
            pass
    driver.quit()
    return data_list
    


if __name__ == '__main__':
    data_list = get_data("add_slug_name")
    to_json(data_list)



