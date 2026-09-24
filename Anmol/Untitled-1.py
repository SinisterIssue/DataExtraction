def get_soup(url):
    from bs4 import BeautifulSoup as bs
    import requests
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36"}
    res = requests.get(url, headers = headers)
    soup = bs(res.text, 'html.parser')
    return soup



def get_data(slug = "slugName"):
    import time
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    import re


    url = "https://www.adamscosheriff.org/most-wanted-list/"
    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(options=options)
    driver.get(url)
    time.sleep(3)

    hrefs = driver.find_elements(By.XPATH, f"/html/body/div/div[1]/div['i']/div[2]/p/a")
    hrefs = [i.get_attribute("href") for i in hrefs]


    data_list = []
    for href in hrefs:
        data_dict = {}
        name = ""
        address = ""
        employer = ""
        gender = ""
        dob = ""
        hair = ""
        eyes = ""
        height = ""
        weight = ""
        race = ""


        soup = get_soup(href)

        image = soup.find("div", class_="wanted-mugshot").find("img")["src"]


        info = soup.find("div", class_="inmate-info").find_all("p")
        for i in info:
            text = i.text
            value = text.split(":")[1].strip()
            if value:
                if "Full Name:" in text:
                    name = value
                elif "Address:" in text:
                    address = value
                elif "Employer:" in text:
                    employer = value
                elif "Sex:" in text:
                    gender = value
                elif "Date of Birth:" in text:
                    dob = value
                elif "Hair Color:" in text:
                    hair = value
                elif "Eyes:" in text:
                    eyes = value
                elif "Height:" in text:
                    height = value
                elif "Weight:" in text:
                    weight = value
                elif "Race:" in text:
                    if value == "W":
                        race = "White"
                    elif value == "B":
                        race = "Black"
                    else:
                        race = value


        if name:
            data_dict["fullName"] = name
            if address:
                data_dict["addressLine1"] = "Last Known: " + address
            if employer:
                data_dict["employerName"] = "Last Known: " + employer
            if gender:
                data_dict["gender"] = gender
            if dob:
                data_dict["dob"] = dob
            if hair:
                data_dict["hair"] = hair
            if eyes:
                data_dict["eyes"] = eyes
            if height:
                data_dict["height"] = height
            if weight:
                data_dict["weight"] = weight
            if race:
                data_dict["race"] = race


            data_dict["image"] = image

        attributes = list(data_dict.keys())
        if "race" in attributes and "gender" in attributes:
            data_dict["summary"] = "{} is a {} {}. Subject is held by Adams County Sherif's Office".format(name, race, gender)
        else:
            data_dict["summary"] = "{} is held by Adams County Sherif's Office".format(name)

        data_list.append(data_dict)


    driver.quit()
    return data_list



def to_json(data):
    import json
    with open("judge.json", "w") as outfile:
        json.dump(data, outfile,indent=4)
        outfile.close()


if __name__ == "__main__":
    to_json(get_data())