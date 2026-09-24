from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

driver = webdriver.Chrome()
driver.get("http://www.hcmc.gr/en_US/web/portal/cv")

people = driver.find_element(By.XPATH, f'//ul[@class="layouts level-1"]/li[2]/a').click()   

name = driver.find_element(By.XPATH, f"//div/h1").text
print(name)
name = name.rsplit("-", maxsplit=1)
print(name)
position = name[1].strip()
print(position)
name  = name[0]
print(name)
# for i in range (3, 7):
#     posts = driver.find_element(By.XPATH, f'//div[1]/p[{i}]/strong').text
#     print(posts)
# image = driver.find_element(By.XPATH, f"//div/div/div[1]/p[1]/img").get_attribute("src")
# print(image)
positions = driver.find_elements(By.XPATH, f"//div/div/div/div/div[1]/p")
additionalInfo = ""
for p in positions:
    if len(p.text.strip()):
        additionalInfo += p.text.strip() + "; "
print(additionalInfo)