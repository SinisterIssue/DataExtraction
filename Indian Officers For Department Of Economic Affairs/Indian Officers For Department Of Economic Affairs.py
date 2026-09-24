
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
    url = "https://dea.gov.in/whos-who?field_whos_who_category_tid=All&title=&field_email_feedback_email=&page="
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
    while True:
        try:
            time.sleep(2)
            list1 = driver.find_elements(By.XPATH, f'/html/body/section[3]/div/div/div[2]/div[1]/div[2]/div/div/div[2]/div[2]/div[1]/div/table/tr')
            print(len(list1))
            for i in range(3, len(list1)+1):
                list2 = driver.find_elements(By.XPATH, f'/html/body/section[3]/div/div/div[2]/div[1]/div[2]/div/div/div[2]/div[2]/div[1]/div/table/tr[{i}]/td')
                data_dict = {}
                careerInfoDesignation = ""
                emails = ""
                fax = ""
                telephoneNos = ""
                fullAddress = ""
                additionalInfo = ""
                
                for j in range(1, len(list2)+1):
                    if j==1:
                        fullName = driver.find_element(By.XPATH, f'/html/body/section[3]/div/div/div[2]/div[1]/div[2]/div/div/div[2]/div[2]/div[1]/div/table/tr[{i}]/td[{j}]').text
                        print(fullName)
                        if fullName == "Vacant" or fullName == "vacant":
                            fullName = ""
                    if j==2:
                        careerInfoDesignation = driver.find_element(By.XPATH, f'/html/body/section[3]/div/div/div[2]/div[1]/div[2]/div/div/div[2]/div[2]/div[1]/div/table/tr[{i}]/td[{j}]').text
                        print(careerInfoDesignation)
                    if j==3:
                        emails = driver.find_element(By.XPATH, f'/html/body/section[3]/div/div/div[2]/div[1]/div[2]/div/div/div[2]/div[2]/div[1]/div/table/tr[{i}]/td[{j}]').text
                        emails = emails.replace("[at]", "@").replace("[dot]", ".")
                        print(emails)
                    if j==4:
                        telephoneNos = driver.find_element(By.XPATH, f'/html/body/section[3]/div/div/div[2]/div[1]/div[2]/div/div/div[2]/div[2]/div[1]/div/table/tr[{i}]/td[{j}]').text
                        if "FAX:" in telephoneNos:
                            fax = telephoneNos.split("FAX:")[1].strip()
                            telephoneNos = telephoneNos.split("FAX:")[0].strip()
                            print(fax)
                        if " FAX" in telephoneNos:
                            fax = telephoneNos.split("\n")[1].strip()
                            telephoneNos = telephoneNos.split("\n")[0].strip()
                        if "(" in telephoneNos:
                            telephoneNos = telephoneNos.split("(")[0]
                            fax = telephoneNos.split("\n", 1)[-1]
                            telephoneNos = telephoneNos.replace(fax, "")
                        telephoneNos = telephoneNos.replace("\n", ", ")
                    if j==5:
                        inter = driver.find_element(By.XPATH, f'/html/body/section[3]/div/div/div[2]/div[1]/div[2]/div/div/div[2]/div[2]/div[1]/div/table/tr[{i}]/td[{j}]').text
                        inter = inter.replace("\n", ", ")
                    if j==6:
                        telephoneNos = telephoneNos + ", " + driver.find_element(By.XPATH, f'/html/body/section[3]/div/div/div[2]/div[1]/div[2]/div/div/div[2]/div[2]/div[1]/div/table/tr[{i}]/td[{j}]').text.replace("\n", ", ")
                        print(telephoneNos)
                    if j==7:
                        room = driver.find_element(By.XPATH, f'/html/body/section[3]/div/div/div[2]/div[1]/div[2]/div/div/div[2]/div[2]/div[1]/div/table/tr[{i}]/td[{j}]').text
                    if j==8:
                        fullAddress = driver.find_element(By.XPATH, f'/html/body/section[3]/div/div/div[2]/div[1]/div[2]/div/div/div[2]/div[2]/div[1]/div/table/tr[{i}]/td[{j}]').text
                        print(fullAddress)
                if telephoneNos.strip() == ",":
                    telephoneNos = ""
                summary = fullName + " is the " + careerInfoDesignation
                if inter.strip() != "" and room.strip() !="":
                    additionalInfo = "Intercom No: " + inter + "; Room No: " + room
                if inter.strip() == "" and room.strip() == "":
                    additionalInfo = ""
                if inter.strip() =="" and room.strip() != "":
                    additionalInfo = "Room No: " + room
                if inter.strip() !="" and room.strip() == "":
                    additionalInfo = "Intercom No: " + inter


                print("*"*50)
                if fullName:
                    data_dict['fullName'] = fullName
                if careerInfoDesignation:
                    data_dict['careerInfoDesignation'] = careerInfoDesignation
                if emails:
                    data_dict['emails'] = emails
                if telephoneNos:
                    data_dict['telephoneNos'] = telephoneNos
                if fax:
                    data_dict['fax'] = fax
                if fullAddress:
                    data_dict['fullAddress'] = fullAddress
                if additionalInfo:
                    data_dict['additionalInfo'] = additionalInfo
                if summary:
                    data_dict['summary'] = summary
                if fullName != "" and careerInfoDesignation != "":
                    data_list.append(data_dict)
            driver.find_element(By.LINK_TEXT, f'next ›').click()
        except:
            break
    driver.quit()
    return data_list



if __name__ == '__main__':
    data_list = get_data("add_slug_name")
    to_json(data_list)


