# use selenium to scrape headlines from corriere.it 
# pip install selenium
from re import L
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import pandas as pd
import time 
import sys 

HOME = "https://corriere.it"
# open Firefox
driver = webdriver.Firefox()
# navigate to corriere.it 
driver.get(HOME)
# In order to extract the information that you’re looking to scrape, 
# you need to locate the element’s XPath. 
# An XPath is a syntax used for finding any element on a webpage.

# We can see the headline
#<a class="has-text-black" href="https://www.corriere.it/sport/calcio/coppa-italia/22_aprile_19/inter-milan-formazioni-news-risultato-f607f438-bfef-11ec-9f78-c9d279c21b38.shtml">Inter-Milan, doppio Lautaro e Gosens, nerazzurri in finale di Coppa Italia  </a>
# --> [@class=”name”] 
# all great but we need to sort out this coxokie pop-up 
#driver.find_element_by_xpath("//*[@id='_cpmt-accept']").click()
#WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, '_cpmt-accept'))).click()
#WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "div#_cpmt-buttons button#_cpmt-accept"))).click()
time.sleep(5)
# carefully look at the env, we have an iframe here 
cookie_iframe = driver.find_element_by_xpath("//iframe[@id='_cpmt-iframe']")
driver.switch_to.frame(cookie_iframe)
print(cookie_iframe)
#driver.switch_to.frame(driver.find_element(By.XPATH("//iframe[@id='_cpmt-iframe']")))
button = driver.find_element_by_id("_cpmt-accept").click()

# back to the main class 
driver.get(HOME)
# elements --> find_all
headlines  = driver.find_elements_by_xpath('//h4[@class="title-art-hp is-medium is-line-h-106"]')
# here we get all the headlines from the corriere 
# we can get the text 
for headline in headlines:
    print(headline.text)