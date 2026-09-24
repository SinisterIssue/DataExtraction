
from ctypes import pointer
import time
import json
import re
from datetime import datetime


def to_json(data_list):
    hash_obj = json.dumps(data_list,indent=4)
    with open("s26-14 members of past parliaments.json", "w") as ts:
        ts.write(hash_obj)


def get_data(slug="slugName"):
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from selenium import webdriver
    from selenium.webdriver.common.by import By

    data_list = []
    url = "http://www.ttparliament.org/members.php?mid=26"
    options = webdriver.ChromeOptions()
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    driver = webdriver.Chrome(options=options)
    options = webdriver.ChromeOptions()
    options.add_argument("start-maximized")
    driver.get(url)
    driver.find_element(By.XPATH,"/html/body/div/div[3]/div[4]/div/div/main/div/div/section/div/div/div/section/div/div/div/div/div/div/section[2]/div/div/div/section[1]/div/div[1]/div/div/div/div/div/a").click()
    time.sleep(3)
    rowsXpath = '/html/body/div/div[3]/div[4]/div/div/main/div/div/section/div/div/div/section/div/div/div/div/div/div/section/div/div/div/div/div/div/div/div/a'
    rows = WebDriverWait(driver, 30).until(EC.presence_of_all_elements_located((By.XPATH, rowsXpath)))
    rows = [i.get_attribute('href') for i in rows]
    for row in rows:
        
        
        dict = {}
        fullName = ''
        prefix = ''
        politicalParty = ''
        constituency =''
        careerInfoDesignation = ''
        careerInfoStartDate = ''
        careerInfoEndDate = ''
        committeeName = ''
        fullAddress = ''
        telephoneNos = ''
        fax = ''
        emails = ''
        additionalInfo = ''
        description = ''
        careerInfo = ''
        image = ''
        summary = ''
        
        listOfCareerInfo = []
        
        driver.get(row)
        
        fullNamedata = driver.find_element(By.XPATH,"/html/body/div/div[3]/div[4]/div/div/main/div/div/section[1]/div/div/div/section/div/div[2]/div/div[1]/div/div/h2").text
        fullNamedata = fullNamedata.replace('The Honourable ','').strip().replace('Senator the Honourable ','').strip().replace('Senator','').strip()
        #print(fullNamedata)
        if 'Mr.' in fullNamedata or 'Dr.' in fullNamedata or 'Ms.' in fullNamedata :
            fullName1 = fullNamedata.split('.')
            prefix = fullName1[0]
            fullName = fullName1[1].strip()
        else:
            fullName = fullNamedata
        print(fullName)
        
        image = driver.find_element(By.XPATH,"/html/body/div/div[3]/div[4]/div/div/main/div/div/section[1]/div/div/div/section/div/div[1]/div/div/div/div/div/img").get_attribute('src')
        #print(image)
        
        politicalParty = driver.find_element(By.XPATH,"/html/body/div/div[3]/div[4]/div/div/main/div/div/section[1]/div/div/div/section/div/div[2]/div/div[2]/div/div/div").text
        if politicalParty == 'UNC':
            politicalParty = 'United National Congress'
        if politicalParty =='PNM':
            politicalParty = "People's National Movement"
        #print(politicalParty)
        try:
            careerInfoDesignation = driver.find_element(By.XPATH,"/html/body/div/div[3]/div[4]/div/div/main/div/div/section[1]/div/div/div/section/div/div[2]/div/div[4]/div/div/div").text
            constituency = driver.find_element(By.XPATH,"/html/body/div/div[3]/div[4]/div/div/main/div/div/section[1]/div/div/div/section/div/div[2]/div/div[3]/div/div/div").text
            constituency = constituency.replace('SPEAKER OF THE HOUSE','').strip()
            #print(constituency)
            
        except : 
            careerInfoDesignation = driver.find_element(By.XPATH,"/html/body/div/div[3]/div[4]/div/div/main/div/div/section[1]/div/div/div/section/div/div[2]/div/div[3]/div/div/div").text
            pass    
        
        
    
        careerparadata = driver.find_element(By.XPATH,"/html/body/div/div[3]/div[4]/div/div/main/div/div/section[2]/div/div[2]/div/div/div/div").text
        paradata = careerparadata.replace('Maiden Contribution',';Maiden Contribution').split(';')
        description= paradata[0].replace('\n',' ').strip()
        careerInfoStartDate = re.findall("[a-zA-Z]+\s[0-9]+,\s[0-9]+",description)
        # try:
        #     careerInfoStartDate = careerInfoStartDate[0]
        # except:
        #     pass
        try:
            additionalInfo = paradata[1].replace('The House of Representatives - ','').strip().replace('The Senate - ','').strip().replace('\n',': ').strip().replace('- link','').strip()
        except:
            pass
        
        try:
            driver.find_element(By.XPATH,"/html/body/div/div[3]/div[4]/div/div/main/div/div/section[2]/div/div[1]/div/div/div/div[2]/a").click()
    
            fullAddress1 = driver.find_element(By.XPATH,"/html/body/div/div[3]/div[4]/div/div/main/div/div/section[2]/div/div[2]/div/div/div/div/div[1]").text
            fullAddress = fullAddress1.replace('Address:','').strip().replace('\n',' ').strip().replace('\n\n',' ').strip()
            #print(fullAddress)
            telephoneNos = driver.find_element(By.XPATH,"/html/body/div/div[3]/div[4]/div/div/main/div/div/section[2]/div/div[2]/div/div/div/div/div[2]").text
            telephoneNos = telephoneNos.replace('Phone:','').strip()
            #print(telephoneNos)
            
            calldata = driver.find_element(By.XPATH,"/html/body/div/div[3]/div[4]/div/div/main/div/div/section[2]/div/div[2]/div/div/div/div").text
            #print(calldata)
            calldata = calldata.replace('Fax:','$Fax:').strip().replace('Email:','$Email:').strip()
            calldata = calldata.split('$')
            for j in range(len(calldata)):
                try:
                    if 'Fax:' in calldata[j]:
                        fax = calldata[j].replace('Fax:','').strip()
                        #print(fax)
                except :
                    pass
                try:
                    if 'Email:' in calldata[j]:
                        emails = calldata[j].replace('Email:','').strip()
                        #print([emails])
                except:
                    pass
        except:
            pass
        
        try:
            driver.find_element(By.XPATH,"/html/body/div/div[3]/div[4]/div/div/main/div/div/section[2]/div/div[1]/div/div/div/div[3]/a").click()
            # careerInfo = driver.find_element(By.XPATH,"/html/body/div/div[3]/div[4]/div/div/main/div/div/section[2]/div/div[2]/div/div/div/div/div").text
            # careerInfo = re.sub('\([^)]*\)','',careerInfo).strip().replace('\n',' ; ').strip()
            # print(careerInfo) 
            #print('---------------------------------------------------------')
            careerdata = driver.find_elements(By.XPATH,"/html/body/div/div[3]/div[4]/div/div/main/div/div/section[2]/div/div[2]/div/div/div/div/div/div")
            
            for j in range(1,len(careerdata)+1):
                
                
                careerinfodata = driver.find_element(By.XPATH,f"/html/body/div/div[3]/div[4]/div/div/main/div/div/section[2]/div/div[2]/div/div/div/div/div/div[{j}]").text
                cardata = careerinfodata.split('\n')
                #tempdict = {}
                
                for k in range(len(cardata)):
                    
                    careerInfoTerms = ''
                    careerInfoRoles = ''
                    
                    tempdict = {}
                  

                    if 'Republican Parliament' in cardata[k]:
                        careerdate = cardata[k].strip()
                        parliament = re.sub("\([^)]*\)","",careerdate)
                        careerInfoStartDatedata1 = re.findall("\([^)]*\)",careerdate)
                        careerInfoStartDatedata11 = careerInfoStartDatedata1
                        careerInfoStartDatedata11 = ''.join(careerInfoStartDatedata11)
                        careerInfoStartDatedataa = careerInfoStartDatedata11.replace('(','').strip().replace(')','').strip().replace('- Present','').strip()
                        careerInfoStartDatedata  = careerInfoStartDatedata1[0].replace('(','').strip().replace(')','').strip().replace('Present','').strip()
                        careerInfoStartDatedata = careerInfoStartDatedata.split('-')
                        careerInfoStartDate = careerInfoStartDatedata[0].strip()
                        if careerInfoStartDate!='':
                            careerInfoStartDate = careerInfoStartDate
                            

                        careerInfoEndDate = careerInfoStartDatedata[1].strip()
                        if careerInfoEndDate!='':
                            careerInfoEndDate = careerInfoEndDate
                        
                    if 'Minister' in cardata[k] or 'Leader ' in cardata[k] or 'Senator' in cardata[k] or 'Attorney General' in cardata[k] or 'Member' in cardata[k] or 'Speaker' in cardata[k] or 'Ministry' in cardata[k] or 'Vice-President' in cardata[k] or 'President' in cardata[k]:
                        careerInfoRoles = cardata[k].strip()
                        careerInfoRoles = re.sub("\([^)]*\)","",careerInfoRoles).strip()
                        if careerInfoRoles:
                            careerInfoRoles += ' of '+parliament
                        else:
                            careerInfoRoles = careerInfoRoles
                        #print(careerInfoRoles)
                    
                    if 'HOUSE OF REPRESENTATIVES' in cardata[k] or 'SENATE' in cardata[k]:
                        careerInfo = cardata[k].strip()
                        
                    
                    if careerInfoRoles:
                        if 'Present' in careerInfoStartDatedata11:
                            tempdict['designations'] = [careerInfoRoles]
                        else: 
                            tempdict['roles'] = [careerInfoRoles] 
                            
                        tempdict['terms'] = careerInfoStartDatedataa

                        
                        if careerInfoStartDate:
                            tempdict['startDate'] = careerInfoStartDate
                            
                        if careerInfoEndDate and 'Present' not in careerInfoEndDate:
                            tempdict['endDate'] = careerInfoEndDate
                        
                        if careerInfo:
                            tempdict['additionalInfo'] = careerInfo
                        
                        listOfCareerInfo.append(tempdict)
                        
                
                    
                        
        except Exception as error:
            print(error)
            pass
        
        print(listOfCareerInfo)
        
        try:
            driver.find_element(By.XPATH,"/html/body/div/div[3]/div[4]/div/div/main/div/div/section[2]/div/div[1]/div/div/div/div[4]/a").click()
        
            committeeName = driver.find_element(By.XPATH,"/html/body/div/div[3]/div[4]/div/div/main/div/div/section[2]/div/div[2]/div/div/div/div/div").text
            committeeName = re.sub('\([^)]*\)','',committeeName).strip().replace('\n',' , ').strip()
            committeeName = 'Committee Membership: '+committeeName.replace(' results found ','').strip()
            committeeName = re.sub('[0-9]+,','',committeeName).strip()
            committeeName = re.sub("\d\.","",committeeName).strip()
        except:
            pass
        try:
            driver.find_element(By.XPATH,"/html/body/div/div[3]/div[4]/div/div/main/div/div/section[2]/div/div[1]/div/div/div/div[5]/a").click()
            
            additionalInfo1 = driver.find_element(By.XPATH,"/html/body/div/div[3]/div[4]/div/div/main/div/div/section[2]/div/div[2]/div/div/div/div/div").text
            additionalInfo1 = re.sub('\([^)]*\)','',additionalInfo1).strip().replace('\n',' , ').strip()
            additionalInfo1 = 'Bills Debated: '+additionalInfo1.replace(' results found ','').strip()
            additionalInfo1 = re.sub('[0-9]+,','',additionalInfo1).strip()
            if additionalInfo:
                additionalInfo+=' ; '+additionalInfo1
            else:
                additionalInfo = additionalInfo1
                
            #print(additionalInfo)
        except:
            pass
        try:
            driver.find_element(By.XPATH,"/html/body/div/div[3]/div[4]/div/div/main/div/div/section[2]/div/div[1]/div/div/div/div[6]/a").click()
            
            additionalInfo2 = driver.find_element(By.XPATH,"/html/body/div/div[3]/div[4]/div/div/main/div/div/section[2]/div/div[2]/div/div/div/div/div").text
            additionalInfo2 = re.sub('\([^)]*\)','',additionalInfo2).strip().replace('\n',' , ').strip()
            additionalInfo2 = 'Motions Debated: '+additionalInfo2.replace(' results found ','').strip()
            additionalInfo2 = re.sub('[0-9]+,','',additionalInfo2).strip()
            if additionalInfo:
                additionalInfo+=' ; '+additionalInfo2
            else:
                additionalInfo = additionalInfo2
                
            additionalInfo = additionalInfo.replace('Motions Debated: 0 results found','').strip()
        except:
            pass
        driver.back()

        summary = fullName+' is elected as a member of the Parliment of the Republic of Trinidad and Tobago'
        
        print('--------------------------------------')
        if fullName:
            dict['fullName'] = fullName.strip()
            if prefix:
                dict['prefix'] = prefix.strip()
            if politicalParty:
                dict['politicalParty'] = politicalParty.strip()
            if constituency:
                dict['constituency'] = constituency.strip()
            if listOfCareerInfo:
                dict['listOfCareerInfo'] = listOfCareerInfo
            if committeeName:
                dict['committeeName'] = committeeName    
            if fullAddress:
                dict['fullAddress'] = fullAddress.strip()
            if telephoneNos:
                dict['telephoneNos'] = telephoneNos.strip()
            if fax:
                dict['fax'] = fax.strip()
            if emails:
                dict['emails'] = emails.strip()
            if additionalInfo:
                dict['additionalInfo'] = additionalInfo.strip()
            if description:
                dict['description'] = description.strip()
            if image:
                dict['image'] = image
            if summary:
                dict['summary'] = summary.strip()
                
            data_list.append(dict)
            
        
            
    driver.quit()    
    return data_list

if __name__ =="__main__":
    data_list = get_data('slug_name')
    #print(data_list)
    to_json(data_list)