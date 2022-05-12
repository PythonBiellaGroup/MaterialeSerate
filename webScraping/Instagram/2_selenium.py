# here we're learning to use Selenium
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time
import wget

HOME = "https://www.instagram.com"

user = "USER"
passw = "PASSW"

# For Selenium we need a driver, namely a fake browser to use 
# checks requirements
driver = webdriver.Firefox()
driver.get(HOME)
# get cookies 
cookie_file = "cookie.pkl"
cookie_loaded = None
login_state = None
# accept the given cookies 
# little trick firefox has "copy css selector function"
WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.CSS_SELECTOR,"button.aOOlW:nth-child(2)"))).click()
# the cool thing of selenium is that we can have multiple find_element_by
time.sleep(5)
# without waiting we coudl have this kind of error:
# selenium.common.exceptions.ElementClickInterceptedException: Message: Element <button class="sqdOP  L3NKy   y3zKF     " type="submit"> is not clickable at point (846,304) because another element <div class="_7UhW9   xLCgt      MMzan   KV-D4           uL8Hv         "> obscures it
driver.find_element(by=By.NAME, value='username').send_keys(user)
driver.find_element(by=By.NAME, value='password').send_keys(passw)
WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button.L3NKy"))).click()
time.sleep(5)
# now we're logged in 
# click on the login store information --> not now
WebDriverWait(driver, 60).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button.sqdOP:nth-child(1)"))).click()
# again turn off notifications
time.sleep(5)
WebDriverWait(driver, 60).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button.aOOlW:nth-child(2)"))).click()
# let's scrape an image
adele_image = "https://www.instagram.com/p/CdM4PR1rGNC/"
driver.get(adele_image)
# get the image element 
images = driver.find_elements_by_tag_name("img")
images = [image.get_attribute("src") for image in images]
images = images[:-2] #slicing-off IG logo and Profile picture
# the former is the image we want 
test_image = "output.png"
wget.download(images[0], test_image)

# return to the hom 
driver.get(HOME)
# now let's look for a hashtag 
searchbox = WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.XPATH, "//input[@placeholder='Search']")))
searchbox.clear()
keyword = "#milan"
searchbox.send_keys(keyword)
time.sleep(5)
# the key is like a button
searchbox.send_keys(Keys.ENTER)
time.sleep(5)
searchbox.send_keys(Keys.ENTER)
time.sleep(5)
# now we can scroll the page here using a simple javaScript
driver.execute_script("window.scrollTo(0, 4000);")
#select images
images = driver.find_elements(by=By.TAG_NAME, value="img")
images = [image.get_attribute("src") for image in images]
images = images[:-2] #slicing-off IG logo and Profile picture
print(f"Number of scraped images: {len(images)}")