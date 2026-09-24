{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": 33,
   "id": "31935943",
   "metadata": {},
   "outputs": [],
   "source": [
    "from selenium import webdriver\n",
    "from selenium.webdriver.common.by import By\n",
    "from selenium.webdriver.support.ui import WebDriverWait\n",
    "from selenium.webdriver.support import expected_conditions as EC\n",
    "import time\n",
    "import json"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 34,
   "id": "260d27b1",
   "metadata": {},
   "outputs": [],
   "source": [
    "def to_json(data):\n",
    "    \"\"\"\n",
    "    This function takes list of dictionary as Input and \n",
    "    then Creates a JSON file in which Input data is stored\n",
    "    \"\"\"\n",
    "    with open(\"data_dict.json\", \"w\") as outfile:\n",
    "        json.dump(data, outfile,indent=4)\n",
    "        outfile.close()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 35,
   "id": "f6a5e60d",
   "metadata": {},
   "outputs": [],
   "source": [
    "data_list = []\n",
    "url = \"http://www.mca.gov.in/MinistryV2/minister_ca_state.html\"\n",
    "options = webdriver.ChromeOptions()\n",
    "options.add_argument(\"--start-maximized\") \n",
    "options.add_argument(\"--disable-blink-features=AutomationControlled\")\n",
    "options.add_argument(\"--log-level=3\")\n",
    "\n",
    "driver = webdriver.Chrome(options=options)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "988fbdc9",
   "metadata": {},
   "outputs": [],
   "source": [
    "driver.get(url)\n",
    "total_links = driver.find_elements(By.XPATH, f'//div/div/ul/li/a')\n",
    "# links = [i.get_attribute(\"href\") for i in total_links]\n",
    "for i in range (2, len(total_links)+1):\n",
    "    driver.find_element(By.XPATH, f'//div/div/ul/li[{i}]/a').click()\n",
    "    time.sleep(3)\n",
    "    try:    \n",
    "        try:\n",
    "            driver.find_element(By.XPATH, '//div/div/div[1]/div[2]/div//*[@id=\"show_all_details\"]').click()\n",
    "            time.sleep(3)\n",
    "        except:\n",
    "            driver.find_element(By.XPATH, '//div[3]/div/div/div/div//*[@id=\"view-ofc\"]').click()\n",
    "            time.sleep(3)\n",
    "    except Exception:\n",
    "        pass\n",
    "    \n",
    "    try:    \n",
    "        try:\n",
    "            driver.find_element(By.XPATH, '//div/div[2]/div[4]/div//*[@id=\"viewmore\"]').click()\n",
    "            time.sleep(3)\n",
    "        except:\n",
    "            driver.find_element(By.XPATH, '//div/div[2]/div[5]/div//*[@id=\"viewmore\"]').click()\n",
    "            time.sleep(3)\n",
    "    except Exception:\n",
    "        pass\n",
    "\n",
    "    list1 = driver.find_elements(By.XPATH, f\"//div[@class='profileData1']/p/span[1]\")\n",
    "#         print(list1)\n",
    "    for j in range (1, len(list1)+1):\n",
    "        if Designation in list1:\n",
    "            designation = driver.find_element(f\"//div[@class='profileData1']/p[{j}]/span[2]\").text\n",
    "            print(designation)\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "34047e86",
   "metadata": {},
   "outputs": [],
   "source": []
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3 (ipykernel)",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.9.6"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 5
}
