
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
    url = "https://www.state.gov/narcotics-rewards-program/target-information/wanted/"
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized") 
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--log-level=3")
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    translator = GoogleTranslator(target='english')
    driver = webdriver.Chrome(options=options)
    driver.maximize_window()
    driver.get(url)
    list1 = driver.find_elements(By.XPATH, f'/html/body/div[1]/div[2]/main/article/div/div[2]/div/ul/li/a')
    for i in range(1, len(list1)+1):
        link = driver.find_element(By.XPATH, f'/html/body/div[1]/div[2]/main/article/div/div[2]/div/ul/li[{i}]/a').get_attribute("href")
        driver.execute_script("window.open('');")
        driver.switch_to.window(driver.window_handles[1])
        driver.get(link)
        try:
            search = driver.find_element(By.XPATH, f'/html/body/div[1]/div[2]/main/article/div/div[2]/div/div/div[2]/form/div[1]/select')
            search.send_keys("30")
            search.send_keys(Keys.RETURN)
        except:
            pass
        list2 = driver.find_elements(By.XPATH, f'/html/body/div[1]/div[2]/main/article/div/div[2]/div/ul/li/a')
    #     print(len(list2))
        for j in range(1, len(list2)+1):
            image = ""
            driver.find_element(By.XPATH, f'/html/body/div[1]/div[2]/main/article/div/div[2]/div/ul/li[{j}]/a').click()
            data_dict = {}
            status = "Wanted"
            description =""
            reward = ""
            charges =""
            identifierType = ""
            distinguishMarks = ""
            identifierID = ""
            fullName = driver.find_element(By.XPATH, f'/html/body/div[1]/div[2]/main/article/section/div[2]/div/h1').text
            fullName = fullName.replace("– New Target", "").replace("— New Target", "")
            print(fullName)
            try:
                image = driver.find_element(By.XPATH, f'/html/body/div[1]/div[2]/main/article/div[2]/div/figure/strong/img').get_attribute('src')
            except:
                try:
                    image = driver.find_element(By.XPATH, f'/html/body/div[1]/div[2]/main/article/div[2]/div/figure/b/img').get_attribute('src')
                except:
                    try:
                        image = driver.find_element(By.XPATH, f'/html/body/div[1]/div[2]/main/article/div[2]/div/figure/img').get_attribute('src')
                    except:
                        try:
                            image = driver.find_element(By.XPATH, f'/html/body/div[1]/div[2]/main/article/div[2]/div/p[2]/span/img').get_attribute('src')
                        except:
                            pass

            print(image)
            try:
                driver.find_element(By.XPATH, f'/html/body/div[5]/div/div/button').click()
            except:
                pass
            try:
                lastUpdatedAt = driver.find_element(By.XPATH, f'/html/body/div[1]/div[2]/main/article/section/div[2]/div/div[1]/p[3]').text
            except:
                pass
            bioInfo = driver.find_element(By.XPATH, f'/html/body/div[1]/div[2]/main/article/div[2]/div/p[4]').text
            if "NAME" not in bioInfo:
                bioInfo = driver.find_element(By.XPATH, f'/html/body/div[1]/div[2]/main/article/div[2]/div/p[2]').text
                if "NAME" not in bioInfo:
                    bioInfo = driver.find_element(By.XPATH, f'/html/body/div[1]/div[2]/main/article/div[2]/div/p[1]').text
                    if "NAME" not in bioInfo:
                        bioInfo = driver.find_element(By.XPATH, f'/html/body/div[1]/div[2]/main/article/div[2]/div/p[3]').text
            try:
                alias = bioInfo.split("ALIASES:")[1].split("\n")[0].replace("\n", "").strip().replace("N/A", "").replace("Unknown", "")
            except:
                alias = driver.find_element(By.XPATH, f'/html/body/div[1]/div[2]/main/article/div[2]/div/p[2]/span[3]').text.strip().replace("N/A", "").replace("Unknown", "")
            print(alias)
            dob = bioInfo.split("DOB:")[1].split("POB:")[0].replace("\n", "").strip().replace("UNKNOWN", "").replace("Unknown", "")
            print(dob)
            placeOfBirthCity = bioInfo.split("POB:")[1].split("NATIONALITY:")[0].replace("\n", "").strip().replace("UNKNOWN", "").replace("Unknown", "")
            print(placeOfBirthCity)
            nationality = bioInfo.split("NATIONALITY:")[1].split("CITIZENSHIP:")[0].replace("\n", "").strip().replace("UNKNOWN", "").replace("Unknown", "")
            print(nationality)
            height = bioInfo.split("HEIGHT:")[1].split("WEIGHT:")[0].replace("\n", "").strip().replace("UNKNOWN", "").replace("Unknown", "")
            print(height)
            weight = bioInfo.split("WEIGHT:")[1].split("HAIR")[0].replace("\n", "").strip().replace("UNKNOWN", "").replace("Unknown", "")
            print(weight)
            hair = bioInfo.split("HAIR COLOR:")[1].split("EYE COLOR:")[0].replace("\n", "").strip().replace("UNKNOWN", "").replace("Unknown", "")
            print(hair)
            eyes = bioInfo.split("EYE COLOR:")[1].split("\n")[0].strip().replace("UNKNOWN", "").replace("Unknown", "")
            print(eyes)
            if fullName == "Luciano Marín Arango":
                identifierType = "COLOMBIAN CEDULA"
                identifierID = bioInfo.split("COLOMBIAN CEDULA:")[1].split("MARKS")[0].strip()
            if "MARKS" in bioInfo:
                distinguishMarks = bioInfo.split("MARKS:")[1].split("\n")[0].strip().replace("UNKNOWN", "").replace("Unknown", "")
            list3 = driver.find_elements(By.XPATH, f'/html/body/div[1]/div[2]/main/article/div[2]/div/p')
            for k in range(1, len(list3)+1):
                info = driver.find_element(By.XPATH, f'/html/body/div[1]/div[2]/main/article/div[2]/div/p[{k}]').text
                if "[Wanted" in info:
                    info = ""
                elif "Poster" in info:
                    info = ""
                elif "NAME" in info:
                    info = ""
                elif "ALL IDENTITIES" in info:
                    info = ""
                elif "charge" in info:
                    charges = info
                elif fullName in info:
                    description = description + info
                else:
                    description = description + info

            description = description.replace("\n", "")
            try:
                reward = description.split("reward of")[1].split("for", 1)[0].strip()
            except:
                try:
                    reward = description.split("REWARD OF")[1].split("for", 1)[0].strip()
                except:
                    pass
            reward = reward.title()
            reward = reward[0:reward.index("Million")+7]
            print(reward)
            print(charges)
            print(description)
            summary = fullName + " is one of the Wanted: Narcotics Rewards Program Targets and has a reward of: " + reward + " for any information provided."
            if fullName:
                data_dict['fullName'] = fullName
            if identifierID:
                data_dict['identifierID'] = identifierID
            if identifierType:
                data_dict['identifierType'] = identifierType
            if status:
                data_dict['status'] = status
            if image:
                data_dict['image'] = image
            if alias:
                data_dict['alias'] = alias
            if dob:
                data_dict['dob'] = dob
            if placeOfBirthCity:
                data_dict['placeOfBirthCity'] = placeOfBirthCity
            if nationality:
                data_dict['nationality'] = nationality
            if height:
                data_dict['height'] = height
            if weight:
                data_dict['weight'] = weight
            if hair:
                data_dict['hair'] = hair
            if eyes:
                data_dict['eyes'] = eyes
            if distinguishMarks:
                data_dict['distinguishMarks'] = distinguishMarks
            if charges:
                data_dict['charges'] = charges
            if description:
                data_dict['description'] = description
            if reward:
                data_dict['reward'] = reward
            if lastUpdatedAt:
                data_dict['lastUpdatedAt'] = lastUpdatedAt
            if summary:
                data_dict['summary'] = summary
            data_list.append(data_dict)
            driver.back()
        try:
            driver.find_element(By.XPATH, f'/html/body/div[5]/div/div/button').click()
        except:
            pass
        driver.close()
        driver.switch_to.window(driver.window_handles[0])
    driver.quit()
    return data_list

if __name__ == '__main__':
    data_list = get_data("add_slug_name")
    to_json(data_list)


