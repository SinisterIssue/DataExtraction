from email.mime import image
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import json
import re
# import nltk
# nltk.download('stopwords')
# nltk.download('punkt')
# from nltk.corpus import stopwords
# from nltk.tokenize import word_tokenize, sent_tokenize

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
    url = "http://www.hcmc.gr/en_US/web/portal/cv"
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized") 
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--log-level=3")

    driver = webdriver.Chrome(options=options)
    try:
        driver.get(url)
        totalMembers = driver.find_elements(By.XPATH, f'//ul[@class="layouts level-1"]/li/a')
        links = [i.get_attribute("href") for i in totalMembers]
        for i in links:
            driver.get(i)
            time.sleep(3)
            try:
                data_dict = {}
                additionalInfo = ''
                name = driver.find_element(By.XPATH, f"//div[2]/div/h1").text
                if "-" in name:
                    name = name.split("-")
                    position = name[1].strip()
                    name  = name[0] 
                if "," in name:
                    name = name.split(",")
                    position = name[1].strip()
                    name  = name[0]

                image = driver.find_element(By.XPATH, f"//div/div/div[1]/p[{i}]/img").get_attribute("src")

                # for i in range (3, 7):
                #     posts = driver.find_element(By.XPATH, f'//div[1]/p[{i}]/strong').text
                totalInfos = driver.find_elements(By.XPATH, f'//div[1]/p')
                infos = [i.get_attribute("p") for i in totalInfos]
                for i in infos:
                    info = driver.find_element(By.XPATH, f'//div[1]/p["{i}"]')
            except:
                pass    
    except:
        pass