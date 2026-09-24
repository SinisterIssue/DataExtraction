def get_soup(url):
    from bs4 import BeautifulSoup as bs
    import requests
    headers={'User-Agent': 'Mozilla/5.0 (iPad; U; CPU OS 3_2_1 like Mac OS X; en-us) AppleWebKit/531.21.10 (KHTML, like Gecko) Mobile/7B405'}
    #     headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36"}
    with requests.get(url, headers = headers, stream = True) as res:
        soup = bs(res.text, 'html.parser')
    return soup



def get_data(slug = "slugName"):
    import re

    url = "https://en.wikipedia.org/wiki/Category:People_convicted_of_money_laundering"
    soup = get_soup(url)

    hrefs = soup.find("div", class_="mw-category mw-category-columns").find_all("a")
    hrefs = ["https://en.wikipedia.org" + i["href"] for i in hrefs]

    data_list = []
    for href in hrefs:
        data_dict = {}
        familyInfo = ""
        desig = ""
        dob_pob = ""
        dob = ""
        pobCity = ""
        pobCountry = ""
        dod = ""
        name = ""
        image = ""
        education  = ""
        nationality = ""
        occupation = ""
        yearsActive = ""
        knownFor = ""
        crimePenality = ""
        charges = ""
        maritalStatus = ""
        politicalParty = ""
        alias = ""
        offense = ""
        description = ""
        careerInfo = ""
        achievements = ""
        crimeInfo = ""
        crimeDes = ""
        remarks = ""
        summary = ""


        soup = get_soup(href)

        name = soup.find("h1", {"id": "firstHeading"}).text.strip()

        try:
            image = soup.find("table", class_="infobox biography vcard").find("img")
            if image:
                image = "https:" + image["src"]
        except:
            pass

        try:
            infoBox = soup.find("table", class_="infobox biography vcard").find_all("tr")
            infoBox = [i.text for i in infoBox]
        except:
            pass


        try:
            temp = soup.find("table", class_="infobox vcard").find("th", class_="infobox-header").text
            if not re.match(".*[Pp][Ee][Rr][Ss][Oo][Nn][Aa][Ll].*", desig):
                desig = temp.strip()
        except:
            pass

        try:
            infoBox = soup.find("table", class_="infobox vcard").find_all("tr")
            infoBox = [i.text for i in infoBox]
        except:
            pass


        for info in infoBox:
            info = re.sub("\[.*?\]", " ", info)
            if re.match("^[Bb]orn", info):
                dob_pob = info
                dob = re.findall("\d{1,2}\s{0,1}[A-Z][a-z]+\s{0,1}\d{4}|[A-Z][a-z]+ \d{0,2}, \d{4}", dob_pob)
                if dob:
                    dob = dob[0]
                else:
                    dob = dob = re.findall("\d{4}", dob_pob)
                    if dob:
                        dob = dob[0]
                dob_pob = re.sub(".*\d{0,2}\s{0,1}[A-Z][a-z]+\s{0,1}\d{4}|.*\d{4}", "", dob_pob)
                pob = re.sub("[Bb]orn|\(.*?\)", "", dob_pob).strip()
                pob = pob.split(",")
                if len(pob) > 1:
                    pobCountry = pob[-1].strip()
                    pobCity = ",".join(pob[:-1]).strip()
            elif re.match("^[Dd]ied", info):
                dod = re.findall("\d{0,2}\s{0,1}[A-Z][a-z]+\s{0,1}\d{4}|[A-Z][a-z]+ \d{0,2}, \d{4}|\d{4}", info)
                if dod:
                    dod = dod[0].strip()
            elif re.match("^[Nn]ationality", info):
                nationality = re.sub("[Nn]ationality", "", info).strip()
            elif re.match("^[Aa]lma|^[Ee][Dd][Uu][Cc][Aa][Tt][Ii][Oo][nN]", info):
                education = re.sub("[aA]lma.*?mater|[Ee][Dd][Uu][Cc][Aa][Tt][Ii][Oo][nN]", "", info).strip()
                education = re.sub("\n", "; ", education)
            elif re.match("^[oO]ccupation", info):
                occupation = re.sub("[oO]ccupation", "", info).strip()
            elif re.match("^[Yy]ears.*?active", info):
                yearsActive = re.sub("[Yy]ears.*active", "", info).strip()
            elif re.match("^[Kk]nown.*?for", info):
                knownFor = re.sub("[Kk]nown.*?for", "", info).strip()
            elif re.match("^[Cc]riminal.*?penalty", info):
                crimePenality = re.sub("[Cc]riminal.*?penalty", "", info).strip()
            elif re.match("^[Ss]pouse\(s\)", info):
                maritalStatus = "Married"
                familyInfo = "Spouse Name: " + re.sub("[sS]pouse\(s\)|\(.*?\)|\n", "", info).strip()
            elif re.match("^[cC]hildren", info):
                children = re.sub("[cC]hildren", "", info).strip()
                children = re.findall("[A-Z][a-z]+", children)
                children = ", ".join(children)
                if familyInfo:
                    familyInfo += "; Children: " + children
                else:
                    familyInfo = "Children: " + children
            elif re.match("^[Pp]olitical party", info):
                politicalParty = re.sub("[Pp]olitical party", "", info).strip()
            elif re.match("^[oO]ther.*names", info):
                alias = re.sub("[oO]ther.*?names", "", info)
            elif re.match(".*[Cc][Oo][Nn][Vv][Ii][Cc][Tt][Ii][Oo][Nn].*", info):
                offense = re.sub("[Cc][Oo][Nn][Vv][Ii][Cc][Tt][Ii][Oo][Nn]|\(s\)", "", info).strip()
            elif re.match(".*Criminal charge(s).*", info):
                charges = re.sub(".*Criminal charge(s).*", "", info)


        details = soup.find("div", class_="mw-parser-output").find_all(["p", "h2", "li"])
        for tag in details:
            if "<p>" in str(tag):
                summary = re.sub("\(.*?\)|\[\d+\]", "", tag.text)
                summary = re.sub("\s{2,}", " ", summary)
                break


        t = 0
        while t < len(details):
            if '<h2 class="section-heading"' in str(details[t]):
                head = details[t].text.strip()
                head = re.sub("[Ee][Dd][Ii][Tt]", "", head).strip()
                t += 1
                data = ""
                while True and t < len(details):
                    data += ' ' + details[t].text.strip()
                    t += 1
                    if t >= len(details) or '<h2 class="section-heading"' in str(details[t]):
                        break
                data = re.sub("\[.*?\]", "", data).strip()
                data = re.sub("\n", " ", data)
                if re.match(".*[Ee][aA][Rr][Ll][Yy].*|.*[bB][Aa][Cc][Kk][Gg][Rr][Oo][Uu][Nn][Dd].*", head):
                    if description:
                        description += "; " + data
                    else:
                        description = data
                elif re.match(".*[Cc][aA][rR][eE][Ee][rR].*", head):
                    if careerInfo:
                        careerInfo += '; ' + data
                    else:
                        careerInfo = data
                elif re.match(".*[Pp][Ee][Rr][Ss][oO][nN][aA][lL] [Ll][iI][fF][Ee].*", head):
                    if description:
                        description += "; " + data
                    else:
                        description = data
                elif re.match(".*[aA][wW][aA][Rr][Dd].*", head):
                    achievements = data
                elif re.match(".*[bB][iI][Cc][Hh][Ee][Ii][Rr][Oo].*", head):
                    if crimeInfo:
                        crimeInfo += '; ' + data
                    else:
                        crimeInfo = data
                elif re.match(".*[fF][Ii][Xx][Ii][Nn][Gg].*|.*[Cc][Oo][Nn][Vv][Ii][Cc][Tt][Ii][Oo][Nn].*", head):
                    if crimeDes:
                        crimeDes += "; " + data
                    else:
                        crimeDes = data
                elif re.match(".*[Aa][rR][Rr][Ee][Ss][tT].*|.*[cC][Oo][Rr][Rr][Uu][Pp][Tt][Ii][Oo][Nn].*", head):
                    if crimeDes:
                        crimeDes += "; " + data
                    else:
                        crimeDes = data
                elif desig in head:
                    if careerInfo:
                        careerInfo += '; ' + data
                    else:
                        careerInfo = data
                elif re.match(".*[pP][Rr][Oo][Ss][Ee][Cc][Uu][Tt][Ii][Oo][Nn].*|.*[tT][Rr][Ii][aA][Ll].*", head):
                    if remarks:
                        remarks += "; " + head + ": " + data
                    else:
                        remarks = head + ": " + data
            else:
                t += 1


        if name:
            data_dict["fullName"] = name
            if image:
                data_dict["image"] = image
            if desig:
                data_dict["careerInfoDesignation"] = desig
            if dob:
                data_dict["dob"] = dob
            if pobCity:
                data_dict["placeOfBirthCity"] = pobCity
            if pobCountry:
                data_dict["placeOfBirthCountry"] = pobCountry
            if dod:
                data_dict["importantDates"] = "Date of Death: "+dod
            if familyInfo:
                data_dict["familyInfo"] = familyInfo
            if education:
                data_dict["educationInfo"] = education
            if nationality:
                data_dict["nationality"] = nationality
            if occupation:
                data_dict["occupation"] = occupation
            if summary:
                data_dict["summary"] = summary
            if charges:
                data_dict["charges"] = charges
            if yearsActive:
                data_dict["additionalInfo"] = "Years Active: "+yearsActive
            if knownFor:
                if yearsActive:
                    data_dict["additionalInfo"] += "; Known For: "+knownFor
                else:
                    data_dict["additionalInfo"] = "Known For: " + knownFor
            if maritalStatus:
                data_dict["maritalStatus"] = maritalStatus
            if politicalParty:
                data_dict["politicalPartyName"] = politicalParty
            if alias:
                data_dict["alias"] = alias
            if offense:
                data_dict["offense"] = offense
            if description:
                data_dict["description"] = description
            if careerInfo:
                data_dict["careerInfo"] = careerInfo
            if achievements:
                data_dict['achievements'] = achievements
            if crimeInfo:
                data_dict["crimeInfo"] = crimeInfo
            if crimeDes:
                data_dict["crimeDescription"] = crimeDes
            if remarks:
                data_dict["remarks"] = remarks


            data_list.append(data_dict)


    return data_list



def to_json(data):
    import json
    with open("judge.json", "w") as outfile:
        json.dump(data, outfile,indent=4)
        outfile.close()


if __name__ == "__main__":
    to_json(get_data())
