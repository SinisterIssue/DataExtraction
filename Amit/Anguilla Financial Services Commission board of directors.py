# Importing necessary libraies
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import json
import re
import nltk
nltk.download('stopwords')
nltk.download('punkt')
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize

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
    url = "https://www.fsc.org.ai/staff.php"
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized") 
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--log-level=3")

    driver = webdriver.Chrome(options=options)
    try:
        driver.get(url)
        totalDepts = driver.find_elements(By.XPATH, "/html/body/div[2]/div/div[1]/div")        
        for i in range(1,len(totalDepts)+1):
            try:
                if i<5:
                    dept = driver.find_element(By.XPATH, f"/html/body/div[2]/div/div[1]/h3[{i+1}]").text
                # getting count of totalEmployees in the dept
                totalEmployees = driver.find_elements(By.XPATH, f"/html/body/div[2]/div/div[1]/div[{i}]/div")
                for j in range(1,len(totalEmployees)+1):
                    try:
                        data_dict = {}
                        additionalInfo = ''

                        # opening the details page of the entity
                        entityDetails = driver.find_element(By.XPATH, f"/html/body/div[2]/div/div[1]/div[{i}]/div[{j}]/div/div[2]/div[1]/a").click()
                        time.sleep(3)
                        name = driver.find_element(By.XPATH, f"/html/body/div[2]/div/div[1]/h3").text
                        title = name.split(maxsplit=1)[0].strip()
                        name = name.split(maxsplit=1)[1].strip()
                        
                        if "," in name:
                            honor = name.split(",")[-1].strip() 
                            additionalInfo += f"'honor': {honor} , "             
                            name = name.split(",")[0].strip()                               
                            
                        image = driver.find_element(By.XPATH, f"/html/body/div[2]/div/div[1]/img").get_attribute('src')
                        designation = driver.find_element(By.XPATH, f"/html/body/div[2]/div/div[1]/h4").text
                        if dept not in ["Staff","Legal"]:
                            designation += " of the "+dept
                        infos = driver.find_elements(By.XPATH, f"/html/body/div[2]/div/div[1]/p")
                        additionalInfo = " 'aboutThePerson': "
                        # extracting text from multiple <p> tags using for loop
                        for p in infos:
                            additionalInfo += p.text.strip() + "  "
                        additionalInfo = additionalInfo.strip('" "|,')
                                
                        additionalInfo += f" , 'aboutTheCommission': The Anguilla Financial Services Commission is headed by a Board and is staffed by a 13 member team. The members of the Board are appointed by the Governor in accordance with the Financial Services Commission Act. The Director of the Commission serves as an ex-officio member of the Board."
                        additionalInfo = additionalInfo.replace("  "," ").strip()
                        
                        summary = ''
                        if dept not in ["Staff",'Legal']:
                            summary += title+" "+name+" is the "+designation + " in the Anguilla Financial Services Commission."
                        else:
                            summary += title+" "+name+" is at the position of "+designation + " in the Anguilla Financial Services Commission."
                            
                        try:    
                            # using nltk library to create summary
                            text = re.split("'aboutThePerson'|'aboutTheCommission'",additionalInfo)[1].strip(':|,|;|" "')
                            
                            stopWords = set(stopwords.words("english"))
                            words = word_tokenize(text)

                            # Creating a frequency table to keep the score of each word
                            freqTable = dict()
                            for word in words:
                                word = word.lower()
                                if word in stopWords:
                                    continue
                                if word in freqTable:
                                    freqTable[word] += 1
                                else:
                                    freqTable[word] = 1

                            # Creating a dictionary to keep the score of each sentence
                            sentences = sent_tokenize(text)
                            sentenceValue = dict()

                            for sentence in sentences:
                                for word, freq in freqTable.items():
                                    if word in sentence.lower():
                                        if sentence in sentenceValue:
                                            sentenceValue[sentence] += freq
                                        else:
                                            sentenceValue[sentence] = freq

                            sumValues = 0
                            for sentence in sentenceValue:
                                sumValues += sentenceValue[sentence]

                            # Average value of a sentence from the original text
                            average = int(sumValues / len(sentenceValue))

                            # Storing sentences into our summary.
                            for sentence in sentences:
                                if (sentence in sentenceValue) and (sentenceValue[sentence] > (1.1 * average)):
                                    summary += " " + sentence.strip()                            
                        
                        except Exception as error:
                            pass
                        if name:
                            data_dict['fullName'] = name
                            if title:
                                data_dict['title'] = title
                            if image:
                                data_dict['image'] = image
                            if designation:
                                data_dict['designation'] = designation
                            if additionalInfo:
                                data_dict['additionalInfo'] = additionalInfo
                            if summary:
                                data_dict['summary'] = summary
                        data_list.append(data_dict)

                        # going back to main page
                        driver.get(url)
                    except:
                        pass
            except:
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
    print(data_list) 