from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import json
import requests
import hashlib
import re
from PyPDF2 import PdfFileReader
from six.moves.urllib.request import urlopen
import io
# from ..general_utility import get_hash_of_html
# from ..s3_upload import hash_check

def get_hash_of_html(html_string):
    hash_object = hashlib.md5(html_string.encode('utf-8'))
    hash_of_html = hash_object.hexdigest()
    return hash_of_html

def to_json(dictionary):
   hash_obj = json.dumps(dictionary)
   with open("dictionary.json", "w") as ts:
       ts.write(hash_obj)

def get_data(slug_name):
    data_list = []
    url = 'https://www.usmarshals.gov/district/me/fugitives/index.html'
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.63 Safari/537.36'}
    res = requests.get(url, headers=headers)
    raw_html_text = res.text

    last_updated_dev = int(time.time())
    update_label_ts = int(time.time())
    html_hash = get_hash_of_html(str(raw_html_text))

    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--log-level=3")
    options.headless = True

    driver = webdriver.Chrome(options=options)
    driver.get(url)
    
    try:
        entitiesXpath = "//div[@id='content']/div/table/tbody/tr"
        entities = WebDriverWait(driver,30).until(EC.presence_of_all_elements_located((By.XPATH, entitiesXpath)))
        for i in range(1, len(entities)+1):
            name = ''
            gender = ''
            race = ''
            height = ''
            weight = ''
            eyes = ''
            hair = ''
            wantedBy = ''
            img = ''
            charges = ''
            additionalInfo = ''
            data_dict = {}

            try:
                link = driver.find_element(by=By.XPATH, value=f"{entitiesXpath}[{i}]/td[1]//a").get_attribute('href')
                if 'pdf' in link:
                    img = driver.find_element(by=By.XPATH, value=f"{entitiesXpath}[{i}]/td[1]//img").get_attribute('src')
                    
                    info = driver.find_element(by=By.XPATH, value=f"{entitiesXpath}[{i}]/td[2]").text
                    for data in info.split('\n'):
                        if data.strip()!='':
                            if 'Name:' in data:
                                name = data.split("Name:")[1].strip()
                                if ',' in name:
                                    t_n = name.split(',')
                                    name = t_n[1].strip() + " " + t_n[0].strip()
                                    name = name.title()
                            elif 'Offense(s):' in data:
                                charges = data.split("Offense(s):")[1].strip()
                    
                    remoteFile = urlopen(link).read()
                    memoryFile = io.BytesIO(remoteFile)
                    pdfFile = PdfFileReader(memoryFile)
                    for pageNum in range(pdfFile.getNumPages()):
                        currentPage = pdfFile.getPage(pageNum)
                        l = currentPage.extractText().split('\n')
                        print(l)
                        for l_data in l:
                            if len(re.findall('Sex\.+MALE', l_data))>0 or len(re.findall('Sex\.+FEMALE', l_data))>0:
                                if len(re.findall(r'Sex\.+MALE', l_data))>0:
                                    gender = 'Male'
                                elif len(re.findall(r'Sex\.+FEMALE', l_data))>0:
                                    gender = 'Female'
                            if len(re.findall(r'Race\.+[A-Z]+', l_data))>0:
                                race = re.findall(r'Race\.+[A-Z]+', l_data)[0]
                                race = re.sub(r'Race\.+', '', race).title()
                            if len(re.findall(r"Height\.+[0-9]\'[0-9]+", l_data))>0:
                                height = re.findall(r"Height\.+[0-9]\'[0-9]+", l_data)[0]
                                height = re.sub(r"Height\.+", '', height)
                                if height.strip()!='':
                                    height += '"'
                            if len(re.findall(r"Weight\.+[0-9]+ pounds", l_data))>0:
                                weight = re.findall(r"Weight\.+[0-9]+", l_data)[0]
                                weight = re.sub(r"Weight\.+", "", weight)
                                weight = weight.replace("pounds", "lbs")
                            if len(re.findall(r"Eyes\.+[A-Za-z]+", l_data))>0:
                                eyes = re.findall(r"Eyes\.+[A-Za-z]+", l_data)[0]
                                eyes = re.sub(r"Eyes\.+", "", eyes)
                            if len(re.findall(r"Hair\.+[A-Za-z]+", l_data))>0:
                                hair = re.findall(r"Hair\.+[A-Za-z]+", l_data)[0]
                                hair = re.sub(r"Hair\.+", "", hair)
                            
                            if l_data!='' and len(re.findall('Sex\.+MALE', l_data))==0 and len(re.findall('Sex\.+FEMALE', l_data))==0 and len(re.findall(r'Race\.+[A-Z]+', l_data))==0 and len(re.findall(r"Height\.+[0-9]\'[0-9]+", l_data))==0 and len(re.findall(r"Height\.+[0-9]\'[0-9]+", l_data))==0 and len(re.findall(r"Weight\.+[0-9]+ pounds", l_data))==0 and len(re.findall(r"Eyes\.+[A-Za-z]+", l_data))==0 and len(re.findall(r"Hair\.+[A-Za-z]+", l_data))==0:
                                if 'wanted by' in l_data.lower():
                                    wantedBy = l_data.lower().split('wanted by')[1].strip().title()
                                    wantedBy = wantedBy.replace(".", "")
                                elif 'subject' in l_data.lower():
                                    if additionalInfo.strip()!='':
                                        additionalInfo += f" {l_data.strip()}"
                                    else:
                                        additionalInfo += l_data.strip()

                    if name.strip()!='':
                        data_dict['fullName'] = name
                        if gender.strip()!='':
                            data_dict['gender'] = gender
                        if race.strip()!='':
                            data_dict['race'] = race
                        if height.strip()!='':
                            data_dict['height'] = height
                        if weight.strip()!='':
                            data_dict['weight'] = weight
                        if eyes.strip()!='':
                            data_dict['eyes'] = eyes
                        if hair.strip()!='':
                            data_dict['hair'] = hair
                        if charges.strip()!='':
                            if ',' in charges:
                                data_dict['charges'] = charges.replace(",", ";")
                            else:
                                data_dict['charges'] = charges
                        if wantedBy.strip()!='':
                            data_dict['wantedBy'] = wantedBy
                        if additionalInfo.strip()!='':
                            data_dict['additionalInfo'] = additionalInfo
                        if img.strip()!='':
                            data_dict['image'] = img
                        if wantedBy.strip()!='':
                            if charges.strip()!='':
                                if gender.strip()!='':
                                    if race.strip()!='':
                                        data_dict['summary'] = f"{data_dict['fullName']} is a {data_dict['race']} {data_dict['gender']} wanted by {data_dict['wantedBy']} for the charges of {data_dict['charges'].replace(';', ',')}."
                                    else:
                                        data_dict['summary'] = f"{data_dict['fullName']} is a wanted {data_dict['gender']} by {data_dict['wantedBy']} for the charges of {data_dict['charges'].replace(';', ',')}."
                                else:
                                    data_dict['summary'] = f"{data_dict['fullName']} is wanted by {data_dict['wantedBy']} for the charges of {data_dict['charges'].replace(';', ',')}."
                            else:
                                data_dict['summary'] = f"{data_dict['fullName']} is wanted by {data_dict['wantedBy']}."
                        else:
                            data_dict['summary'] = f"{data_dict['fullName']} is wanted by The United States Marshal Service District Of Maine."
                        data_list.append(data_dict)
            except:
                pass
    except:
        pass
    driver.quit()
    return data_list

if __name__ == "__main__":
   data_list = get_data('add-slug-here')
   to_json(data_list)