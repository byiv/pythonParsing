from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time
from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client['mailru']
letter = db.letter

service = Service('/usr/local/bin/chromedriver')
driver = webdriver.Chrome(service=service)
driver.get('https://account.mail.ru/login')

wait = WebDriverWait(driver, 10)
elem = driver.find_element(By.NAME, "username")
elem.send_keys('study.ai_172@mail.ru')
elem.send_keys(Keys.ENTER)

elem = wait.until(EC.visibility_of_element_located((By.NAME, "password")))
elem.send_keys('NextPassword#')
elem.send_keys(Keys.ENTER)
time.sleep(10)

link = driver.find_element(By.XPATH, '//a[contains(@class, "letter")]')
driver.get(link.get_attribute('href'))
mails = []
flag = True

while flag:
    mail_data = {}
    mail_data['title'] = wait.until(EC.presence_of_element_located((By.XPATH, '//h2'))).text
    mail_data['from'] = wait.until(EC.presence_of_element_located((By.XPATH, '//div[@class="letter__author"]/span'))).get_attribute('title')
    mail_data['date'] = wait.until(EC.presence_of_element_located((By.XPATH, '//div[@class="letter__author"]/div[@class="letter__date"]'))).text
    mail_data['text'] = wait.until(EC.presence_of_element_located((By.XPATH, '//div[@class="letter__body"]'))).text
    try:
        letter.insert_one(mail_data)
    except Exception as e:
        print(e)
    time.sleep(1)
    next_mail = wait.until(EC.presence_of_element_located((By.XPATH, '//div[contains(@class, "portal-menu-element_next")]/span'))).get_attribute('data-title-shortcut')
    if next_mail is None:
        flag = False
    ActionChains(driver).key_down(Keys.CONTROL).send_keys('k').key_up(Keys.CONTROL).perform()

driver.close()
