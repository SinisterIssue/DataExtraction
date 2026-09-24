# Importing necessary libraies
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import json
from datetime import datetime


def to_json(data):
    with open("data_dict.json", "w") as outfile:
        json.dump(data, outfile,indent=4)
        outfile.close()


def get_data(slug_name):
    url = 'https://www.fcso.ar.gov/warrants.php'
    data_list = []

    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized") 
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--log-level=3")
    data_list=[]
    # temp_list will be used to remove duplicate entries of entity details as data source have multiple entries for some entities with same details
    temp_list = []
    driver = webdriver.Chrome(options=options)

    try:
        driver.get(url)
        
        while True:
            try:               
                # There are 2 entities inside one div tag and one single full page contains 10 div tags and 20 entities
                total_groups = len(driver.find_elements(By.XPATH, f'//*[@id="warrantsDiv"]/div'))
                try:
                    for i in range(1,total_groups+1):
                        # as sub-div tag is present at either 1 or 3 div tag
                        for j in [1,3]:
                            data_dict={}
                            # temp_dict will be used to store entity details like name, image_url, age, charges, additionalInfo and summary
                            temp_dict = {} 
                                                        
                            try:
                                name = driver.find_element(By.XPATH, f'//*[@id="warrantsDiv"]/div[{i}]/div[{j}]/div[1]/span').text
                                name = name.split(",")[::-1]
                                name = name[0] + ' ' + name[1].strip()
                            except:
                                name = ""
                            try:
                                image = driver.find_element(By.XPATH, f'//*[@id="warrantsDiv"]/div[{i}]/div[{j}]//img[2]').get_attribute('src')
                            except:
                                image = ''
                            try:    
                                age = driver.find_element(By.XPATH, f'//*[@id="warrantsDiv"]/div[{i}]/div[{j}]/div[2]').text
                                age = age.split(":")[-1].strip()
                            except:
                                age = ''
                            try:
                                date = driver.find_element(By.XPATH, f'//*[@id="warrantsDiv"]/div[{i}]/div[{j}]/div[3]').text
                                date = date.split(":")[1].strip()
                                date = datetime.strptime(date, "%m/%d/%Y").strftime("%d/%m/%Y")
                                
                            except:
                                date = ""
                            try:
                                charges = driver.find_element(By.XPATH, f'//*[@id="warrantsDiv"]/div[{i}]/div[{j}]//*[@class="charge_desc"]').text
                                charges = charges.replace('\n',' , ').title()
                            except:
                                charges = ""
                            try:
                                is_bond = driver.find_element(By.XPATH, f'//*[@id="warrantsDiv"]/div[{i}]/div[{j}]/div[4]/span[@class="tbold warrant_data"]').text
                                if is_bond.lower() == "bond:":
                                    bond = driver.find_element(By.XPATH, f'//*[@id="warrantsDiv"]/div[{i}]/div[{j}]/div[4]').text
                                    bond = bond.split(":")[-1].strip()
                                else:
                                    bond = ''
                            except:
                                bond = ''

                            if len(date.strip()) and len(bond.strip()):
                                additionalInfo = f"'ChargeDate': {date}, 'Bond': {bond}"
                            elif len(date.strip()):
                                additionalInfo = f"'ChargeDate': {date}"
                            elif len(bond.strip()):
                                additionalInfo = f"'Bond': {bond}"
                            else:
                                additionalInfo = ''

                            if len(name.strip()) and len(age.strip()) and len(charges.strip()) and len(date.strip()):
                                summary = f'{name}, aged {age}, has been charged for {charges} on {date}.'
                            elif len(name.strip()) and len(age.strip()) and len(charges.strip()) :
                                summary = f'{name}, aged {age}, has been charged for {charges}.'
                            elif len(name.strip()):
                                summary = f"Name of {name} is present on the list of warrants released by the Faulkner County Sheriff's Office"
                            else:
                                summary = ''

                            if len(name.strip()):
                                # temp_dict and temp_list will be used to remove dulicate entries for each entity
                                temp_dict['fullName'] = name
                                temp_dict['image'] = image
                                temp_dict['age'] = age
                                temp_dict['additionalInfo'] = additionalInfo
                                temp_dict['charges'] = charges
                                temp_dict['summary'] = summary
                                if temp_dict not in temp_list:
                                    temp_list.append(temp_dict)
                            
                                    if len(name.strip()):
                                        data_dict['fullName'] = name
                                        if len(image.strip()):
                                            data_dict['image'] = image
                                        if len(age.strip()):
                                            data_dict['age'] = age
                                        if len(additionalInfo.strip()):
                                            data_dict['additionalInfo'] = additionalInfo
                                        if len(charges.strip()):
                                            data_dict['charges'] = charges
                                        if len(summary.strip()):
                                            data_dict['summary'] = summary
                                       
                                        
                                        data_list.append(data_dict)
                                            
                            else:
                                pass

                except Exception as error:
                    pass
                
                try:
                    driver.get(url)
                    url = driver.find_element(By.LINK_TEXT, ">").get_attribute('href')  
                    driver.find_element(By.LINK_TEXT, ">").click()                             
                    time.sleep(2)
                    
                except Exception as error:
                    break

            except Exception as error:
                pass

        return data_list

    except Exception as error:
        return f"Error occured while loading the given url and occured error is:\n{error}"

    finally:
        # Always use driver.quit() in finally block if you are using selenium
        driver.quit()


if __name__ == '__main__':
    data_list = get_data("add_slug_name")
    to_json(data_list)
    # print(data_list) 