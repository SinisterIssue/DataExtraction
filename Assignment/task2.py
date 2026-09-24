import requests
from bs4 import BeautifulSoup
import json


# Get HTML source code from the webpage.
url = "https://www.iomfsa.im/enforcement/disqualified-directors/"
r = requests.get(url)
c = r.content
soup = BeautifulSoup(c, "html.parser")

# All names are contained within <section> having class "accordian item". Extract Text from these sections.
vcdiv = soup.findAll('section', attrs={'class': 'accordion-item'})
a = []
for i in vcdiv:
    a.append(i.text)

old_features = [
    "Name:", "Address (at date of disqualification):", "Date of Birth:", "Period of Disqualification:", "Dates of Disqualification:", "Notes:"]

new_features = ["name", "address", "dob",
                "periodOfDisqualification", "datesOfDisqualification", "summary"]

# Run a loop that extracts values of all parameters and stores it in a list of dictionaries.
names = []
for i in a:
    person = {}
    for j in old_features:
        s = i
        s = s[s.find(j):]
        s = s[(len(j)):s.find("\n")]
        person[new_features[old_features.index(j)]] = s.strip()
    names.append(person)

# Convert dictionary to JSON.
final_json = json.dumps(names, indent=2)

# Save JSON file.
f = open("task_2.json", "w")
f.write(final_json)
f.close()
