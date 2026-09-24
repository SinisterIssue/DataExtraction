import json


def to_json(data):
    """
    This function takes list of dictionary as Input and
    then Creates a JSON file in which Input data is stored
    """
    with open("data_dict.json", "w") as outfile:
        json.dump(data, outfile, indent=4)
        outfile.close()


def get_data(slug_name):
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    import time

    data_list = []
    url = "http://www.mca.gov.in/MinistryV2/minister_ca_state.html"
    # from pyvirtualdisplay import Display
    # display = Display(visible=0, size=(1366, 768))
    # display.start()

    # PATH = "C:\\Users\\gangu\\Downloads\\chromedriver_win32\\chromedriver.exe"
    options = webdriver.ChromeOptions()
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(options=options)
    driver.get(url)
    total_links = driver.find_elements(By.XPATH, f'//div/div/ul/li/a')

    for i in range(2, 4):
        driver.find_element(By.XPATH, f'//div/div/ul/li[{i}]/a').click()
        time.sleep(3)
        data_dict = {}
        try:
            name = driver.find_element(By.XPATH, f'//div/div[1]/div[2]//*[@class="profileHeader row"]').text
            name = name.strip()
            if name:
                data_dict['fullName'] = name
        except:
            pass
        try:
            designation = driver.find_element(By.XPATH,
                                              f'//div/div/div[1]/div[2]/p[2]//*[@class="contentdata col-9"]').text
            designation = designation.strip()
            if designation:
                data_dict['careerInfoDesignation'] = designation
        except:
            try:
                designation = driver.find_element(By.XPATH,
                                                  f'//div/div/div[2]/p[1]//*[@class="contentdata col-8"]').text
                designation = designation.strip()
                if designation:
                    data_dict['careerInfoDesignation'] = designation
            except:
                pass
        try:
            image = driver.find_element(By.XPATH,
                                        f'//div/div/div[1]/div[1]//*[@class="profilecard-img"]').get_attribute("src")
            if image:
                data_dict['image'] = image
        except:
            try:
                image = driver.find_element(By.XPATH,
                                            f'//div/div/div/div[1]//*[@class="profile-pic-image"]').get_attribute("src")
                if image:
                    data_dict['image'] = image
            except:
                pass
        try:
            driver.find_element(By.XPATH, '//div/div/div[1]/div[2]/div//*[@id="show_all_details"]').click()
            time.sleep(3)
        except:
            pass

        spans = len(driver.find_elements(By.XPATH, f"//p[@class='profileSummary row']/span[@class='labeldata col-3']"))
        additionalInfo = ""
        familyInfo = ""
        for j in range(1, spans + 1):
            try:
                headings = driver.find_element(By.XPATH,
                                               f"//p[@class='profileSummary row'][{j}]/span[@class='labeldata col-3']").text
                #             print(headings)
                #             body = driver.find_element(By.XPATH, f"//p[@class='profileSummary row'][{j}]/span[@class='contentdata col-9']").text
                #             print(body)
                if "Party :" in headings:
                    party = driver.find_element(By.XPATH,
                                                f"//p[@class='profileSummary row'][{j}]/span[@class='contentdata col-9']").text

                elif "Father's\nName :" in headings:
                    father = driver.find_element(By.XPATH,
                                                 f"//p[@class='profileSummary row'][{j}]/span[@class='contentdata col-9']").text.split(
                        ",", 1)[0]
                    familyInfo = familyInfo + "Fathers Name:" + father + "; "

                elif "Father's Name :" in headings:
                    father = driver.find_element(By.XPATH,
                                                 f"//p[@class='profileSummary row'][{j}]/span[@class='contentdata col-9']").text.split(
                        ",", 1)[0]
                    familyInfo = familyInfo + "Fathers Name:" + father + "; "

                elif "Mother's Name :" in headings:
                    mother = driver.find_element(By.XPATH,
                                                 f"//p[@class='profileSummary row'][{j}]/span[@class='contentdata col-9']").text
                    familyInfo = familyInfo + "Mothers Name:" + mother + "; "

                elif "Mother's\nName :" in headings:
                    mother = driver.find_element(By.XPATH,
                                                 f"//p[@class='profileSummary row'][{j}]/span[@class='contentdata col-9']").text
                    familyInfo = familyInfo + "Mothers Name:" + mother + "; "

                elif "Date of Birth :" in headings:
                    dob = driver.find_element(By.XPATH,
                                              f"//p[@class='profileSummary row'][{j}]/span[@class='contentdata col-9']").text

                elif "Place of Birth :" in headings:
                    placeofBirthCity = driver.find_element(By.XPATH,
                                                           f"//p[@class='profileSummary row'][{j}]/span[@class='contentdata col-9']").text
                    if '(' in placeofBirthCity:
                        placeofBirthCity = placeofBirthCity.replace('(', '').split(')')[0]
                elif "Marital Status :" in headings:
                    maritalStatus = driver.find_element(By.XPATH,
                                                        f"//p[@class='profileSummary row'][{j}]/span[@class='contentdata col-9']").text

                elif "Date of Marriage :" in headings:
                    marriageDate = driver.find_element(By.XPATH,
                                                       f"//p[@class='profileSummary row'][{j}]/span[@class='contentdata col-9']").text
                    importantDates = "Date of Marriage:" + " " + marriageDate

                elif "Spouse's\nName :" in headings:
                    spouse = driver.find_element(By.XPATH,
                                                 f"//p[@class='profileSummary row'][{j}]/span[@class='contentdata col-9']").text
                    familyInfo = familyInfo + "Spouse Name:" + spouse + "; "

                elif "Spouse's Name :" in headings:
                    spouse = driver.find_element(By.XPATH,
                                                 f"//p[@class='profileSummary row'][{j}]/span[@class='contentdata col-9']").text
                    familyInfo = familyInfo + "Spouse Name:" + spouse + "; "

                elif "No. of Daughters :" in headings:
                    daughters = driver.find_element(By.XPATH,
                                                    f"//p[@class='profileSummary row'][{j}]/span[@class='contentdata col-9']").text
                    familyInfo = familyInfo + "Children:" + daughters

                elif "Childern :" in headings:
                    daughters = driver.find_element(By.XPATH,
                                                    f"//p[@class='profileSummary row'][{j}]/span[@class='contentdata col-9']").text
                    familyInfo = familyInfo + "Children:" + daughters

                elif "Educational Qualifications :" in headings:
                    educationInfo = driver.find_element(By.XPATH,
                                                        f"//p[@class='profileSummary row'][{j}]/span[@class='contentdata col-9']").text.replace("\n", "")

                elif "Profession :" in headings:
                    profession = driver.find_element(By.XPATH,
                                                     f"//p[@class='profileSummary row'][{j}]/span[@class='contentdata col-9']").text
                    additionalInfo = additionalInfo + "Profession:" + profession + "; "

                elif "Permanent Address :" in headings:
                    fullAddress = driver.find_element(By.XPATH,
                                                      f"//p[@class='profileSummary row'][{j}]/span[@class='contentdata col-9']").text

                elif "Present  Address :" in headings:
                    fullAddress1 = driver.find_element(By.XPATH,
                                                       f"//p[@class='profileSummary row'][{j}]/span[@class='contentdata col-9']").text

                elif "Present\nAddress :" in headings:
                    fullAddress1 = driver.find_element(By.XPATH,
                                                       f"//p[@class='profileSummary row'][{j}]/span[@class='contentdata col-9']").text

                elif "Official Address :" in headings:
                    contactPersonAddress = driver.find_element(By.XPATH,
                                                               f"//p[@class='profileSummary row'][{j}]/span[@class='contentdata col-9']").text

                elif "Official\nAddress :" in headings:
                    contactPersonAddress = driver.find_element(By.XPATH,
                                                               f"//p[@class='profileSummary row'][{j}]/span[@class='contentdata col-9']").text
                    contactPersonAddress = contactPersonAddress.replace("\n", " ")
                elif "Interests :" in headings:
                    interests = driver.find_element(By.XPATH,
                                                    f"//p[@class='profileSummary row'][{j}]/span[@class='contentdata col-9']").text
                    additionalInfo = additionalInfo + "Interests:" + interests + "; "

                elif "Countries Visited :" in headings:
                    countryVisited = driver.find_element(By.XPATH,
                                                         f"//p[@class='profileSummary row'][{j}]/span[@class='contentdata col-9']").text
                    additionalInfo = additionalInfo + "Country Visited:" + countryVisited + "; "

                elif "Social And Cultural Activities :" in headings:
                    social = driver.find_element(By.XPATH,
                                                 f"//p[@class='profileSummary row'][{j}]/span[@class='contentdata col-9']").text
                    additionalInfo = additionalInfo + "Social and Cultural Activities:" + social + "; "

                elif "Favourite Pastime and Recreation :" in headings:
                    pastTime = driver.find_element(By.XPATH,
                                                   f"//p[@class='profileSummary row'][{j}]/span[@class='contentdata col-9']").text
                    additionalInfo = additionalInfo + "Past Time:" + pastTime + "; "

                elif "Sports & Clubs:" in headings:
                    sports = driver.find_element(By.XPATH,
                                                 f"//p[@class='profileSummary row'][{j}]/span[@class='contentdata col-9']").text
                    additionalInfo = additionalInfo + "Sports & Clubs:" + sports + "; "

                elif "Other Information :" in headings:
                    otherInfo = driver.find_element(By.XPATH,
                                                    f"//p[@class='profileSummary row'][{j}]/span[@class='contentdata col-9']").text
                    additionalInfo = additionalInfo + "Other Information:" + otherInfo + "; "
                    additionalInfo = additionalInfo.replace("\n", " ")

                if familyInfo:
                    data_dict['familyInfo'] = familyInfo
                if party:
                    data_dict['politicalParty'] = party
                if dob:
                    data_dict['dob'] = dob
                if placeofBirthCity:
                    data_dict['placeOfBirthCity'] = placeofBirthCity
                if maritalStatus:
                    data_dict['maritalStatus'] = maritalStatus
                if importantDates:
                    data_dict['importantDates'] = importantDates
                if educationInfo:
                    data_dict['educationInfo'] = educationInfo
                if fullAddress:
                    data_dict['fullAddress'] = fullAddress
                if fullAddress1:
                    data_dict['fullAddress1'] = fullAddress1
                if contactPersonAddress:
                    data_dict['contactPersonAddress'] = contactPersonAddress
            except:
                pass
        if i == 2:
            careerInfo = ""
            for k in range(18, 24):
                Info = driver.find_element(By.XPATH, f'//div[2]/div[1]/p[{k}]/span[2]').text
                careerInfo += Info
            careerInfo = careerInfo.replace("\n", ". ")
        if i == 3:
            careerInfo = ""
            for k in range(21, 40):
                try:
                    Info = driver.find_element(By.XPATH, f'//div[2]/div[1]/p[{k}]/span[2]').text
                    careerInfo += Info
                except:
                    pass
            careerInfo = careerInfo.replace("\n", ". ")
        summary = name + " is the " + designation + " and is a part of " + party

        additionalInfo = additionalInfo.strip()
        if additionalInfo:
            data_dict['additionalInfo'] = additionalInfo
        if careerInfo:
            data_dict['careerInfo'] = careerInfo
        if summary:
            data_dict['summary'] = summary
        list1 = driver.find_elements(By.XPATH, f'//div/table/tbody/tr')
        for j in range(1, len(list1) + 1, 2):
            data_dict2 = {}
            list2 = driver.find_elements(By.XPATH, f'//div/table/tbody/tr[{j}]/td')
            for k in range(1, len(list2) + 1):
                if k == 1:
                    name = driver.find_element(By.XPATH, f'//div/table/tbody/tr[{j}]/td[{k}]').text
                    if "," not in name:
                        pass
                        # print(name)
                elif k == 2:
                    designation = driver.find_element(By.XPATH, f'//div/table/tbody/tr[{j}]/td[{k}]').text
                # print(designation)
                elif k == 3:
                    contactDetails = driver.find_element(By.XPATH, f'//div/table/tbody/tr[{j}]/td[{k}]').text
                    if i==2:
                        contactDetails = contactDetails.replace("\n", ", ")
                    if i==3:
                        contactDetails = contactDetails.split("\n")
                        fax = contactDetails[1] + ", " + contactDetails[4] + ", " + contactDetails[7]
                        contactDetails = contactDetails[0] + ", " + contactDetails[3] + ", " + contactDetails[6]
                elif k == 4:
                    emails = driver.find_element(By.XPATH, f'//div/table/tbody/tr[{j}]/td[{k}]').text
                    emails = emails.replace("[dot]", ".").replace("[at]", "@")
            summary = name + " is the part of " + " Office of Minister of Corporate Affairs"
            if '/' in contactDetails:
                contactDetails = contactDetails.replace('/', '')

            if name and "," not in name:
                data_dict2['fullName'] = name
                if designation:
                    data_dict2['careerInfoDesignation'] = designation
                if contactDetails:
                    data_dict2['telephoneNos'] = contactDetails
                if fax:
                    data_dict2['fax'] = fax
                if emails:
                    data_dict2['emails'] = emails
                if summary:
                    data_dict2['summary'] = summary
            if data_dict2:
                data_list.append(data_dict2)
        if data_dict:
            data_list.append(data_dict)
    driver.quit()
    # display.stop()
    return data_list


if __name__ == '__main__':
    data_list = get_data("add_slug_name")
    to_json(data_list)







