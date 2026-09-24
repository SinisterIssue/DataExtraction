
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import json



def to_json(data):
    """
    This function takes list of dictionary as Input and 
    then Creates a JSON file in which Input data is stored
    """
    with open("data_dict.json", "w") as outfile:
        json.dump(data, outfile,indent=4)
        outfile.close()


data_list = []
url = "https://www.scottcountyiowa.us/sheriff/warrants.php?page=updates"
options = webdriver.ChromeOptions()
options.add_argument("--start-maximized") 
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument("--log-level=3")



def get_data(slug_name):
    driver = webdriver.Chrome(options=options)
    driver.get(url)
    # button = driver.find_element(By.LINK_TEXT, f'Next')
    p=0
    
    while True:
        data_dict = {
                        "fullName" : "",
                        "additionalInfo" : [],
                        "importantDates" :[],
                        "charges" : [],
                        "summary" : ""
            }
        previousName = ""
        try:
            list1 = driver.find_elements(By.XPATH, f'/html/body/div/div/div[2]/div/main/div/div/div[2]/table/tbody/tr')
            for j in range(1, len(list1)+1):
                try:        
                    driver.find_element(By.XPATH, f'/html/body/div/div/div[2]/div/main/div/div/div[2]/table/tbody/tr[{j}]/td[1]/a').click()
                    time.sleep(2)
                    dt = driver.find_elements(By.XPATH, f'/html/body/div/div/div[2]/div/main/div/div/div[2]/div[2]/div[2]/div[1]/dl/dt')
                    for i in range(1, len(dt)+1):
                        headings = driver.find_element(By.XPATH, f'/html/body/div/div/div[2]/div/main/div/div/div[2]/div[2]/div[2]/div[1]/dl/dt[{i}]').text
                        if "First:" in headings:
                            firstName = driver.find_element(By.XPATH, f'/html/body/div/div/div[2]/div/main/div/div/div[2]/div[2]/div[2]/div[1]/dl/dd[{i}]').text
#                             print(firstName)
                        if "Middle:" in headings:
                            middleName = driver.find_element(By.XPATH, f'/html/body/div/div/div[2]/div/main/div/div/div[2]/div[2]/div[2]/div[1]/dl/dd[{i}]').text
#                             print(middleName)
                        if "Last:" in headings:
                            lastName = driver.find_element(By.XPATH, f'/html/body/div/div/div[2]/div/main/div/div/div[2]/div[2]/div[2]/div[1]/dl/dd[{i}]').text
                        if "Suffix:" in headings:
                            suffix = driver.find_element(By.XPATH, f'/html/body/div/div/div[2]/div/main/div/div/div[2]/div[2]/div[2]/div[1]/dl/dd[{i}]').text
                        if "Sex:" in headings:
                            sex = driver.find_element(By.XPATH, f'/html/body/div/div/div[2]/div/main/div/div/div[2]/div[2]/div[2]/div[1]/dl/dd[{i}]').text
                        if "Race:" in headings:
                            race = driver.find_element(By.XPATH, f'/html/body/div/div/div[2]/div/main/div/div/div[2]/div[2]/div[2]/div[1]/dl/dd[{i}]').text
#                             print(race)
                        if "Date of Birth:" in headings:
                            dob = driver.find_element(By.XPATH, f'/html/body/div/div/div[2]/div/main/div/div/div[2]/div[2]/div[2]/div[1]/dl/dd[{i}]').text
                            dob_dmy = dob.split(" ")[0]
                            d = dob_dmy.split("/")[1]
                            m = dob_dmy.split("/")[0]
                            y = dob_dmy.split("/")[2]
                            dob_dmy = d + "/" + m + "/" + y
#                             print(dob_dmy)
                        if "Age:" in headings:
                            age = driver.find_element(By.XPATH, f'/html/body/div/div/div[2]/div/main/div/div/div[2]/div[2]/div[2]/div[1]/dl/dd[{i}]').text
                        if "Weight:" in headings:
                            weight = driver.find_element(By.XPATH, f'/html/body/div/div/div[2]/div/main/div/div/div[2]/div[2]/div[2]/div[1]/dl/dd[{i}]').text
                        if "Height:" in headings:
                            height = driver.find_element(By.XPATH, f'/html/body/div/div/div[2]/div/main/div/div/div[2]/div[2]/div[2]/div[1]/dl/dd[{i}]').text
                        if "Hair Color" in headings:
                            hair = driver.find_element(By.XPATH, f'/html/body/div/div/div[2]/div/main/div/div/div[2]/div[2]/div[2]/div[1]/dl/dd[{i}]').text
#                             print(hair)
                        if "Eye Color" in headings:
                            eyes = driver.find_element(By.XPATH, f'/html/body/div/div/div[2]/div/main/div/div/div[2]/div[2]/div[2]/div[1]/dl/dd[{i}]').text
#                             print(eyes)
                    fullName = firstName+ " " + middleName + " " + lastName 
                    dt2 = driver.find_elements(By.XPATH, f'/html/body/div/div/div[2]/div/main/div/div/div[2]/div[2]/div[2]/div[3]/dl/dt')
                    additionalInfo = ""
                    importantDates = ""
                    for k in range (1, len(dt2)+1):
                        headings2 = driver.find_element(By.XPATH, f'/html/body/div/div/div[2]/div/main/div/div/div[2]/div[2]/div[2]/div[3]/dl/dt[{k}]').text
                        if "Warrant Number:" in headings2:
                            warrantNos = driver.find_element(By.XPATH, f'/html/body/div/div/div[2]/div/main/div/div/div[2]/div[2]/div[2]/div[3]/dl/dd[{k}]').text
                            additionalInfo = additionalInfo + "Warrant Number: " + warrantNos + ", "
                        if "Warrant Date:" in headings2:
                            warrantDate = driver.find_element(By.XPATH, f'/html/body/div/div/div[2]/div/main/div/div/div[2]/div[2]/div[2]/div[3]/dl/dd[{k}]').text
                            warrantDate_dmy = warrantDate.split(" ")[0]
                            d = warrantDate_dmy.split("/")[1]
                            m = warrantDate_dmy.split("/")[0]
                            y = warrantDate_dmy.split("/")[2]
                            warrantDate_dmy = d + "/" + m + "/" + y
                            importantDates = importantDates + "Warrant Date: " + warrantDate_dmy + ", "
                        if "Warrant Held By:" in headings2:
                            warrantHeld = driver.find_element(By.XPATH, f'/html/body/div/div/div[2]/div/main/div/div/div[2]/div[2]/div[2]/div[3]/dl/dd[{k}]').text
                            additionalInfo = additionalInfo + "Warrant Held By: " + warrantHeld + ", "
                        if "Warrant Status:" in headings2:
                            status = driver.find_element(By.XPATH, f'/html/body/div/div/div[2]/div/main/div/div/div[2]/div[2]/div[2]/div[3]/dl/dd[{k}]').text
                        if "Warrant Status Date/Time:" in headings2:
                            warrantStatusDate = driver.find_element(By.XPATH, f'/html/body/div/div/div[2]/div/main/div/div/div[2]/div[2]/div[2]/div[3]/dl/dd[{k}]').text
                            warrantStatusDate_dmy = warrantStatusDate.split(" ")[0]
                            d = warrantStatusDate_dmy.split("/")[1]
                            m = warrantStatusDate.split("/")[0]
                            y = warrantStatusDate.split("/")[2]
                            warrantStatusDate_dmy = d + "/" + m + "/" + y
                            importantDates = importantDates + "Warrant Status Date/Time:" + warrantStatusDate_dmy + ", "
                        if "Charges | Bond:" in headings2:
                            charges = driver.find_element(By.XPATH, f'/html/body/div/div/div[2]/div/main/div/div/div[2]/div[2]/div[2]/div[3]/dl/dd[{k}]').text.replace("|", ",").replace("\n", ";")
#                             print(charges)
                    
                    image = ""
                    try:
                        images = driver.find_elements(By.XPATH, f'/html/body/div/div/div[2]/div/main/div/div/div[2]/div[2]/div[1]/div')
                        for l in range (1, len(images)+1):
                            new_image = driver.find_element(By.XPATH, f'/html/body/div/div/div[2]/div/main/div/div/div[2]/div[2]/div[1]/div[{l}]/a/img').get_attribute("src")
                            image = image + new_image + ", "
                    except:
                        pass
                    if fullName != previousName and len(data_dict['fullName'])>0:
#                         print("if 1")
                        data_dict['additionalInfo'] = ", ".join(data_dict['additionalInfo'])
                        data_dict['importantDates'] = ", ".join(data_dict['importantDates'])
                        data_dict['charges'] = ", ".join(data_dict['charges'])
                        summary = data_dict['fullName'] + " is charged with " + (data_dict['charges']) + " and the warrant is holded by " + warrantHeld
                        data_dict['summary'] = summary
                        print(summary)
                        data_list.append(data_dict)
                        data_dict = {
                        "fullName" : "",
                        "additionalInfo" : [],
                        "importantDates" :[],
                        "charges" : [],
                        "summary" : ""
            }
                    if fullName and fullName == previousName:
#                         print("if 2")
                        if charges:
#                             print("here")
                            data_dict['charges'].append(charges)
                        if importantDates:
                            data_dict['importantDates'].append(importantDates)
                        if additionalInfo:
                            data_dict['additionalInfo'].append(additionalInfo)
                        
                    else:
#                         print("if 3")
                        if fullName:
                            data_dict['fullName'] = fullName
                        if firstName:
                            data_dict['firstName'] = firstName
                        if middleName:
                            data_dict['middleName'] = middleName
                        if lastName:
                            data_dict['lastName'] = lastName
                        if suffix:
                            print("here")
                            data_dict['suffix'] = suffix
                        if image:
                            data_dict['image'] = image
                        if sex:
                            data_dict['sex'] = sex
                        if race:
                            data_dict['race'] = race
                        if dob:
                            data_dict['dob'] = dob_dmy
                        if age:
                            data_dict['age'] = age
                        if weight:
                            data_dict['weight'] = weight
                        if height:
                            data_dict['height'] = height
                        if hair:
                            data_dict['hair'] = hair
                        if eyes:
                            data_dict['eyes'] = eyes
                        if charges:
                            data_dict['charges'].append(charges)
                        if status:
                            data_dict['status'] = status
                        if additionalInfo:
                            data_dict['additionalInfo'].append(additionalInfo)
                        if importantDates:
                            data_dict['importantDates'].append(importantDates)
    #                     print("here")
                    if len(list1) == i:
                        data_dict['additionalInfo'] = ", ".join(data_dict['additionalInfo'])
                        data_dict['importantDates'] = ", ".join(data_dict['importantDates'])
                        data_dict['charges'] = ", ".join(data_dict['charges'])
                        summary = data_dict['fullName'] + " is charged with " + (data_dict['charges']) + " and the warrant is holded by " + warrantHeld
                        data_dict['summary'] = summary
                        print(summary)
                        data_list.append(data_dict)
                    previousName = fullName
                    driver.back()
                except Exception as e:
                    print(e)
                    pass
                
            driver.find_element(By.LINK_TEXT, f'Next').click()
            time.sleep(2)
        except:
            break
    return data_list


if __name__ == '__main__':
    data_list = get_data("add_slug_name")
    to_json(data_list)






