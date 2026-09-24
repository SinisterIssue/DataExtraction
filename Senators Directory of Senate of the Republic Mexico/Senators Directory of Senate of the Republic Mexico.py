
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
    url = "https://www.senado.gob.mx/64/senadores/directorio_de_senadores"
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized") 
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--log-level=3")
    translator = GoogleTranslator(target='english')
    driver = webdriver.Chrome(options=options)
    driver.get(url)
    list1 = driver.find_elements(By.XPATH, f'/html/body/div[3]/div/div[2]/table/tbody/tr/td[2]')
    for i in range (1, len(list1)+1):
        alias=""
        youtubeUrl  =""
        facebookUrl = ""
        twitterUrl = ""
        instagramUrl = ""
        image = ""
        careerInfoDesignation = ""
        state = ""
        additionalInfo =""
        educationInfo =""
        careerInfo =""
        fullAddress = ""
        data_dict = {}
        list2 = driver.find_elements(By.XPATH, f'/html/body/div[3]/div/div[2]/table/tbody/tr[{i}]/td')
        for j in range(2, len(list2)+1):
            if j==2:
                lastName = driver.find_element(By.XPATH, f'/html/body/div[3]/div/div[2]/table/tbody/tr[{i}]/td[{j}]').text
            elif j==3:
                firstName = driver.find_element(By.XPATH, f'/html/body/div[3]/div/div[2]/table/tbody/tr[{i}]/td[{j}]').text
            elif j==4:
                politicalParty = driver.find_element(By.XPATH, f'/html/body/div[3]/div/div[2]/table/tbody/tr[{i}]/td[{j}]').text
            elif j==5:
                telephoneNos = driver.find_element(By.XPATH, f'/html/body/div[3]/div/div[2]/table/tbody/tr[{i}]/td[{j}]').text
                telephoneNos = telephoneNos.replace("\n", " ")
            elif j==6:
                emails = driver.find_element(By.XPATH, f'/html/body/div[3]/div/div[2]/table/tbody/tr[{i}]/td[{j}]').text
        fullName = firstName + " " + lastName
        print(fullName)
        link = driver.find_element(By.XPATH, f'/html/body/div[3]/div/div[2]/table/tbody/tr[{i}]/td/a').get_attribute("href")        
        driver.execute_script("window.open('');")
        driver.switch_to.window(driver.window_handles[1])
        driver.get(link)
        try:
            image = driver.find_element(By.XPATH, f'/html/body/div[3]/div[1]/div[1]/div/div[2]/img').get_attribute("src")
            print(image)
        except:
            pass
        try:
            fullAddress = driver.find_element(By.XPATH, f'/html/body/div[3]/div[1]/div[2]/div/table/tbody/tr[3]/td').text
        except:
            pass
        try:
            facebookUrl = driver.find_element(By.XPATH, f'/html/body/div[3]/div[1]/div[1]/div/div[3]/ul/li[1]/a[@class="btn btn-facebook"]').get_attribute("href")
    #         print(facebookUrl)
        except:
            pass
        try:
            instagramUrl = driver.find_element(By.XPATH, f'/html/body/div[3]/div[1]/div[1]/div/div[3]/ul/li[1]/a[@class="btn btn-instagram"]').get_attribute("href")
    #         print(instagramUrl)
        except:
            pass
        try:
            twitterUrl = driver.find_element(By.XPATH, f'/html/body/div[3]/div[1]/div[1]/div/div[3]/ul/li[1]/a[@class="btn btn-twitter"]').get_attribute("href")
    #         print(twitterUrl)
        except:
            pass
        try:
            youtubeUrl = driver.find_element(By.XPATH, f'/html/body/div[3]/div[1]/div[1]/div/div[3]/ul/li[1]/a[@class="btn btn-youtube"]').get_attribute("href")
        except:
            pass
        try:
            alias = driver.find_element(By.XPATH, f'/html/body/div[3]/div[1]/div[2]/div/table/tbody/tr[2]/td').text
        except:
            pass
        try:
            careerInfoDesignation = driver.find_element(By.XPATH, f'/html/body/div[3]/div[1]/div[2]/div/table/tbody/tr[1]/td').text
            careerInfoDesignation = translator.translate(careerInfoDesignation)
            state = careerInfoDesignation.split("\n")[0]
            careerInfoDesignation = careerInfoDesignation.split("\n")[1]
        except:
            pass
        try:
            list3 = driver.find_elements(By.XPATH, f'/html/body/div[3]/div[1]/div[2]/div/table/tbody/tr')
            for k in range(7, len(list3)+1):
                additionalInfo = driver.find_element(By.XPATH, f'/html/body/div[3]/div[1]/div[2]/div/table/tbody/tr[{k}]').text + additionalInfo
            additionalInfo = translator.translate(additionalInfo)
            additionalInfo = additionalInfo.replace("\n", " ")
        except:
            pass
        try:
            driver.find_element(By.XPATH, f'/html/body/div[3]/div[2]/div/ul/li[7]').click()
        except:
            pass
        try:
            list4  = driver.find_elements(By.XPATH, f'/html/body/div[3]/div[2]/div/div[2]/section[7]/p')
            for l in range(1, len(list4)+1):
                heading = driver.find_element(By.XPATH, f'/html/body/div[3]/div[2]/div/div[2]/section[7]/p[{l}]').text
                heading = translator.translate(heading)
                if "Academic training:" in heading or "Academic training:" in heading:
                    educationInfo = driver.find_element(By.XPATH, f'/html/body/div[3]/div[2]/div/div[2]/section[7]/ul[1]').text
                elif "academic career" in heading:
                    educationInfo = driver.find_element(By.XPATH, f'/html/body/div[3]/div[2]/div/div[2]/section[7]/ul[6]').text
            educationInfo = translator.translate(educationInfo)
            educationInfo = educationInfo.replace("\n", "; ")
            print(educationInfo)
        except:
            pass
        try:
            careerInfo = driver.find_element(By.XPATH, f'/html/body/div[3]/div[2]/div/div[2]/section[7]').text
            careerInfo = translator.translate(careerInfo)
            careerInfo = careerInfo.replace("\n", " ")
        except:
            pass
        try:
            summary = fullName + " is the " + careerInfoDesignation + " of Republic Mexico and also known as " + alias
        except:
            summary = fullName + " is one of the Senators in the Directory of Senate list of the Republic Mexico"

        print("*"*50)
        driver.close()
        driver.switch_to.window(driver.window_handles[0])
        if fullName:
            data_dict['fullName'] = fullName
        if firstName:
            data_dict['firstName'] = firstName
        if lastName:
            data_dict['lastName'] = lastName
        if alias:
            data_dict['alias'] = alias
        if image:
            data_dict['image'] = image
        if politicalParty:
            data_dict['politicalParty'] = politicalParty
        if telephoneNos:
            data_dict['telephoneNos'] = telephoneNos
        if emails:
            data_dict['emails'] = emails
        if careerInfoDesignation:
            data_dict['careerInfoDesignation'] = careerInfoDesignation
        if state:
            data_dict['state'] = state
        if educationInfo:
            data_dict['educationInfo'] = educationInfo
        if careerInfo:
            data_dict['careerInfo'] = careerInfo
        if additionalInfo:
            data_dict['additionalInfo'] = additionalInfo
        if fullAddress:
            data_dict['fullAddress'] = fullAddress
        if facebookUrl:
            data_dict['facebookUrl'] = facebookUrl
        if instagramUrl:
            data_dict['instagramUrl'] = instagramUrl
        if youtubeUrl:
            data_dict['youtubeUrl'] = youtubeUrl
        if twitterUrl:
            data_dict['twitterUrl'] = twitterUrl
        if summary:
            data_dict['summary'] = summary
        data_list.append(data_dict)
    driver.quit()
    return data_list

if __name__ == '__main__':
    data_list = get_data("add_slug_name")
    to_json(data_list)




