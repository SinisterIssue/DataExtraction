
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
    url = "https://www.govtrack.us/congress/members/CA#senators"
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized") 
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--log-level=3")
    translator = GoogleTranslator(target='english')
    driver = webdriver.Chrome(options=options)
    driver.get(url)
    list1 = driver.find_elements(By.XPATH, f'/html/body/div[1]/div[5]/div/div[2]/div/div[1]/div[1]/div/div/p/a')
    for i in range(1, len(list1)+1):
        data_dict = {}
        referenceUrls = ""
        alias = ""
        twitterUrl = ""
        website = ""
        title = "Sen."
        fullName = driver.find_element(By.XPATH, f'/html/body/div[1]/div[5]/div/div[2]/div/div[1]/div[1]/div/div[{i}]/p/a').text
        if '“' in fullName:
            firstName = fullName.split('“')[0].strip()
            lastName = fullName.split('” ')[1]
            alias = fullName.split('“')[1].split("”")[0].strip()
            fullName = firstName + " " + lastName
        print(fullName)
        print(alias)
        try:
            driver.find_element(By.XPATH, f'/html/body/div[3]/div/div/div[3]/button').click()
        except:
            pass
        driver.find_element(By.XPATH, f'/html/body/div[1]/div[5]/div/div[2]/div/div[1]/div[1]/div/div[{i}]/p/a').click()
        time.sleep(4)
        careerInfoDesignation = driver.find_element(By.XPATH, f'/html/body/div[1]/div[4]/div/div[1]/p[1]').text
        print(careerInfoDesignation)
        image = driver.find_element(By.XPATH, f'/html/body/div[1]/div[5]/div/div[2]/div/div[1]/div[3]/div[2]/img').get_attribute('src')
        print(image)
        summary = driver.find_element(By.XPATH, f'/html/body/div[1]/div[5]/div/div[2]/div/div[1]/div[1]/div/p').text
        careerInfoEndDate = summary.split("serves until")[1].replace(".", "").strip()
        print(careerInfoEndDate)
        list2 = driver.find_elements(By.XPATH, f'/html/body/div[1]/div[5]/div/div[1]/div/div[1]/div/a')
        print(len(list2))
        for j in range(1, len(list2)+1):
            heading = driver.find_element(By.XPATH, f'/html/body/div[1]/div[5]/div/div[1]/div/div[1]/div/a[{j}]').text
            if "Website" in heading:
                website = driver.find_element(By.XPATH, f'/html/body/div[1]/div[5]/div/div[1]/div/div[1]/div/a[{j}]').get_attribute('href')
                print(website)
            elif "@" in heading:
                twitterUrl = driver.find_element(By.XPATH, f'/html/body/div[1]/div[5]/div/div[1]/div/div[1]/div/a[{j}]').get_attribute('href')
            elif "Website" not in heading or "@" not in heading:
                referenceUrls = driver.find_element(By.XPATH, f'/html/body/div[1]/div[5]/div/div[1]/div/div[1]/div/a[{j}]').get_attribute('href') + "; " + referenceUrls
        print(referenceUrls)
        listOfCommitteeInfo = driver.find_element(By.XPATH, f'/html/body/div[1]/div[5]/div/div[2]/div/div[2]/section[2]/ul').text.replace("\n", ", ")
        driver.back()
        if fullName:
            data_dict['fullName'] = fullName
        if alias:
            data_dict['alias'] = alias
        if title:
            data_dict['title'] = title
        if careerInfoDesignation:
            data_dict['careerInfoDesignation'] = careerInfoDesignation
        if image:
            data_dict['image'] = image
        if careerInfoEndDate:
            data_dict['careerInfoEndDate'] = careerInfoEndDate
        if website:
            data_dict['website'] = website
        if twitterUrl:
            data_dict['twitterUrl'] = twitterUrl
        if referenceUrls:
            data_dict['referenceUrls'] = referenceUrls
        if listOfCommitteeInfo:
            data_dict['listOfCommitteeInfo'] = listOfCommitteeInfo
        if summary:
            data_dict['summary'] = summary
        data_list.append(data_dict)
    driver.find_element(By.XPATH, f'/html/body/div[1]/div[5]/div/div[2]/div/ul/li[2]/a').click()
    list1 = driver.find_elements(By.XPATH, f'/html/body/div[1]/div[5]/div/div[2]/div/div[1]/div[2]/div[2]/div/p/a')
    print(len(list1))
    for i in range(5, 3*len(list1)):
        try:
            driver.find_element(By.XPATH, f'/html/body/div[3]/div/div/div[3]/button').click()
        except:
            pass
        try:
            description = ""
            data_dict = {}
            referenceUrls = ""
            alias = ""
            twitterUrl = ""
            website = ""
            listOfCommitteeInfo = ""
            image = ""
            title = "Rep."
            fullName = driver.find_element(By.XPATH, f'/html/body/div[1]/div[5]/div/div[2]/div/div[1]/div[2]/div[2]/div[{i}]/p/a').text
            if '“' in fullName:
                firstName = fullName.split('“')[0].strip()
                lastName = fullName.split('” ')[1]
                alias = fullName.split('“')[1].split("”")[0].strip()
                fullName = firstName + " " + lastName
            print(fullName)
            print(alias)

            driver.find_element(By.XPATH, f'/html/body/div[1]/div[5]/div/div[2]/div/div[1]/div[2]/div[2]/div[{i}]/p/a').click()
            time.sleep(4)
            careerInfoDesignation = driver.find_element(By.XPATH, f'/html/body/div[1]/div[4]/div/div[1]/p[1]').text
            print(careerInfoDesignation)
            try:
                image = driver.find_element(By.XPATH, f'/html/body/div[1]/div[5]/div/div[2]/div/div[1]/div[3]/div[2]/img').get_attribute('src')
                print(image)
            except:
                pass
            summary = driver.find_element(By.XPATH, f'/html/body/div[1]/div[5]/div/div[2]/div/div[1]/div[1]/div/p').text
            careerInfoEndDate = summary.split("serves until")[1].replace(".", "").strip()
            print(careerInfoEndDate)
            try:
                list2 = driver.find_elements(By.XPATH, f'/html/body/div[1]/div[5]/div/div[1]/div/div[1]/div/a')
                print(len(list2))
                for j in range(1, len(list2)+1):
                    heading = driver.find_element(By.XPATH, f'/html/body/div[1]/div[5]/div/div[1]/div/div[1]/div/a[{j}]').text
                    if "Website" in heading:
                        website = driver.find_element(By.XPATH, f'/html/body/div[1]/div[5]/div/div[1]/div/div[1]/div/a[{j}]').get_attribute('href')
                        print(website)
                    elif "@" in heading:
                        twitterUrl = driver.find_element(By.XPATH, f'/html/body/div[1]/div[5]/div/div[1]/div/div[1]/div/a[{j}]').get_attribute('href')
                    elif "Website" not in heading or "@" not in heading:
                        referenceUrls = driver.find_element(By.XPATH, f'/html/body/div[1]/div[5]/div/div[1]/div/div[1]/div/a[{j}]').get_attribute('href') + "; " + referenceUrls
                print(referenceUrls)
            except:
                pass
            try:
                listOfCommitteeInfo = driver.find_element(By.XPATH, f'/html/body/div[1]/div[5]/div/div[2]/div/div[2]/section[2]/ul').text.replace("\n", ", ")
            except:
                pass
            try:
                description = driver.find_element(By.XPATH, f'/html/body/div[1]/div[5]/div/div[2]/div/div[1]/div[1]/div[2]').text
            except:
                pass
            print("*"*50)
            driver.back()
            if fullName:
                data_dict['fullName'] = fullName
            if alias:
                data_dict['alias'] = alias
            if title:
                data_dict['title'] = title
            if careerInfoDesignation:
                data_dict['careerInfoDesignation'] = careerInfoDesignation
            if image:
                data_dict['image'] = image
            if description:
                data_dict['description'] = description
            if careerInfoEndDate:
                data_dict['careerInfoEndDate'] = careerInfoEndDate
            if website:
                data_dict['website'] = website
            if twitterUrl:
                data_dict['twitterUrl'] = twitterUrl
            if referenceUrls:
                data_dict['referenceUrls'] = referenceUrls
            if listOfCommitteeInfo:
                data_dict['listOfCommitteeInfo'] = listOfCommitteeInfo
            if summary:
                data_dict['summary'] = summary
            data_list.append(data_dict)
        except:
            pass
    driver.quit()
    return data_list

if __name__ == '__main__':
    data_list = get_data("add_slug_name")
    to_json(data_list)



