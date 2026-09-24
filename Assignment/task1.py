
from googletrans import Translator
import requests
from bs4 import BeautifulSoup

url = "https://www.gov.br/economia/pt-br/acesso-a-informacao/institucional/quem-e-quem/gabinete/quem-e-quem-do-gabinete-do-ministro"
r = requests.get(url)

soup = BeautifulSoup(r.content, "html.parser")



body = soup.find("body")

f = open("tsk1.html", "w")
f.write(body.prettify())
f.close()


body = body.text
translator = Translator(service_urls=['translate.googleapis.com'])


out = translator.translate(soup.text, dest="en")
# print(out.text)
a = out.text.split("\n")
# print(a)
x=[]
for i in a:
    if i!=" " or i!="":
        b = translator.translate(i, dest="en")
        x.append(b)
print(x)
