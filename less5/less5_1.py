from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

service = Service('/usr/local/bin/chromedriver')
driver = webdriver.Chrome(service=service)
driver.get('https://account.mail.ru/login')

wait = WebDriverWait(driver, 10)
elem = driver.find_element(By.NAME, "username")
elem.send_keys('study.ai_172@mail.ru')
elem.send_keys(Keys.ENTER)

elem = wait.until(EC.visibility_of_element_located((By.NAME, "password")))
elem.send_keys('NextPassword172???')
elem.send_keys(Keys.ENTER)
time.sleep(10)

# while True:
links = driver.find_element(By.XPATH, '//a[contains(@class, "letter")]')
for link in links:
    print(link.get_attribute('href'))




# driver.close()