'''NOT WORKING SHOWING retrieving data'''
# from bs4 import BeautifulSoup
# import requests

# r = requests.get("https://www.worldometers.info/world-population/india-population/")
# content = r.content
# soup = BeautifulSoup(content,"html.parser")
# print(soup.find(class_="maincounter-number"))

# from bs4 import BeautifulSoup
# from selenium import webdriver
from siddhantDixit_CountryReport import WorldoMeter
'''WORKING WITH SELENIUM'''
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

link = 'https://www.worldometers.info'
x = WorldoMeter()
x.printCountries()
inp_country = input("Enter the Country Name: ")
url = x.countries_Url[inp_country]
link+=url
rel_url = "span[rel='"+url[url.index('n/')+2:-1]+"']"
print(url)
print(link)

def get_population_count(wait,link):
    driver.get(link)
    while True:
        item = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,rel_url))).text
        if "retrieving data" not in item:
            break
    return item

if __name__ == '__main__':
    with webdriver.Chrome() as driver:
        wait = WebDriverWait(driver,10)
        print(get_population_count(wait,link))