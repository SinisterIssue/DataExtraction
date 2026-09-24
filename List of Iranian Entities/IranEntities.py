
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import json
import re





def to_json(data):
    """
    This function takes list of dictionary as Input and 
    then Creates a JSON file in which Input data is stored
    """
    with open("data_dict.json", "w") as outfile:
        json.dump(data, outfile,indent=4)
        outfile.close()




data_list = []
url = "https://www.iranwatch.org/iranian-entities"
options = webdriver.ChromeOptions()
options.add_argument("--start-maximized") 
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument("--log-level=3")




def get_data(slug_name):
    driver = webdriver.Chrome(options=options)
    driver.get(url)
    p=0
    while True:
        try:
            list1 = driver.find_elements(By.XPATH, f'//div/div[2]/div/div/span/a')
            for i in range(1, len(list1)+1):
                data_dict = {}
                fullName = driver.find_element(By.XPATH, f'//div/div[2]/div[{i}]/div/span/a').text
                print(fullName)
                referenceUrls = driver.find_element(By.XPATH, f'//div/div[2]/div[{i}]/div/span/a').get_attribute("href")
                driver.find_element(By.XPATH, f'//div/div[2]/div[{i}]/div/span/a').click()
                try:
                    additionalInfo = driver.find_element(By.XPATH, f'//div/div/article/div/div[2]/div/div[@class="field-item even"]').text.replace("\n", "; ")
    #                 print(additionalInfo)
                except:
                    try:
                        additionalInfo = driver.find_element(By.XPATH, f'//div/div/article/div/div[3]/div/div[@class="field-item even"]').text.replace("\n", "; ")
    #                     print(additionalInfo)
                    except:
                        pass

                try:
                    image = driver.find_element(By.XPATH, f'//div/div/article/div/div[2]/div/figure/a/img').get_attribute("src")
                    print(image)
                except:
                    try:
                        image = driver.find_element(By.XPATH, f'//div/div/article/div/div[3]/div/figure/a/img').get_attribute("src")
                        print(image)
                    except:
                        pass
                try:
                    list2 = driver.find_elements(By.XPATH, f'//div/article/div/div[1]/section')
                    listOfAlias = ""
                    weapon = ""
                    telephoneNos = ""
                    listOfAddress = ""
                    fax = ""
                    website = ""
                    emails = ""
                    image = ""
                    for j in range(1, len(list2)+1):
                        headings = driver.find_element(By.XPATH, f'//div/article/div/div[1]/section[{j}]').text
                        if "Also Known As: " in headings:
                            listOfAlias = driver.find_element(By.XPATH, f'//div/article/div/div[1]/section[{j}]/div/div').text.replace("\n", ", ")
                            print(listOfAlias)
                        elif "Weapon Program: " in headings:
                            weapon = driver.find_element(By.XPATH, f'//div/article/div/div[1]/section[{j}]/ul').text.replace("\n", "; ")
                            print(weapon)
                        elif "Address: " in headings:
                            listOfAddress = driver.find_element(By.XPATH, f'//div/article/div/div[1]/section[{j}]/div/div').text.replace("\n", "; ").replace("-", "")
                            print(listOfAddress)
                        elif "Phone: " in headings:
                            telephoneNos = driver.find_element(By.XPATH, f'//div/article/div/div[1]/section[{j}]/div/div').text.replace("\n", "; ")
                            print(telephoneNos)
                        elif "Fax: " in headings:
                            fax = driver.find_element(By.XPATH, f'//div/article/div/div[1]/section[{j}]/div/div').text.replace("\n", "; ")
                            print(fax)
                        elif "Entity Web Site: " in headings:
                            website = driver.find_element(By.XPATH, f'//div/article/div/div[1]/section[{j}]/div/div').text.replace("\n", "; ")
                            print(website)
                        elif "E-Mail: " in headings:
                            emails = driver.find_element(By.XPATH, f'//div/article/div/div[1]/section[{j}]/div/div').text.replace("\n", "; ")
                            print(emails)
                except:
                    pass
                try:
                    dateEntered = driver.find_element(By.XPATH, f'//div/section/div/div/article/div/section[2]/div').text
                    lastModified = driver.find_element(By.XPATH, f'//div/section/div/div/article/div/section[3]/div/div').text
                    importantDates = "Date Entered: " + dateEntered + ", Last Modified On: " + lastModified
                    print(importantDates)
                except:
                    try:
                        dateEntered = driver.find_element(By.XPATH, f'//div/section/div/div/article/div/section[1]/div').text
                        lastModified = driver.find_element(By.XPATH, f'//div/section/div/div/article/div/section[2]/div/div').text
                        importantDates = "Date Entered: " + dateEntered + ", Last Modified On: " + lastModified
                        print(importantDates)
                    except:
                        pass
                try:
                    list3 = driver.find_elements(By.XPATH, f'//div/section/div/div/article/div/section[1]/div/div')
                    listOfSuspectEntities = ""
                    for k in range(1, len(list3)+1):
                        suspectEntities = driver.find_element(By.XPATH, f'//div/section/div/div/article/div/section[1]/div/div[{k}]').text
                        listOfSuspectEntities = listOfSuspectEntities + ", "+ suspectEntities
                        suspectEntitiesUrl = driver.find_element(By.XPATH, f'//div/section/div/div/article/div/section[1]/div/div[{k}]/a').get_attribute("href")
                        referenceUrls = referenceUrls + ", " + suspectEntitiesUrl
                    additionalInfo = additionalInfo + "; Suspect Entities & Suppliers: " + listOfSuspectEntities + " ; Weapon Program: " + weapon
                    print(referenceUrls)
                except:
                    pass
                summary = fullName + " is one of the United Nations and European Union sanctions targeting Iran's military and missile programs remain in place until 2020 and 2023 targeted firms and individuals involved in the programs. The sanctions target firms and individuals involved in these programs, including entities connected to the Islamic Revolutionary Guard Corp (IRGC)."
                print(summary)
                print("*"*50)        
                driver.back()
                if fullName:
                    data_dict['fullName'] = fullName
                if image:
                    data_dict['image'] = image
                if listOfAlias:
                    data_dict['listOfAlias'] = listOfAlias
                if listOfAddress:
                    data_dict['listOfAddress'] = listOfAddress
                if telephoneNos:
                    data_dict['telephoneNos'] = telephoneNos
                if fax:
                    data_dict['fax'] = fax
                if website:
                    data_dict['website'] = website
                if emails:
                    data_dict['emails'] = emails
                if importantDates:
                    data_dict['importantDates'] = importantDates
                if additionalInfo:
                    data_dict['additionalInfo'] = additionalInfo
                if referenceUrls:
                    data_dict['referenceUrls'] = referenceUrls
                if summary:
                    data_dict['summary'] = summary
                data_list.append(data_dict)
            driver.find_element(By.LINK_TEXT, f'next ›').click()
            time.sleep(2)

        except:
            break
    return data_list



if __name__ == '__main__':
    data_list = get_data("add_slug_name")
    to_json(data_list)



