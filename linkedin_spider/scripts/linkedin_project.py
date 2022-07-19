import parameters
from time import sleep
from selenium import webdriver
from parsel import Selector
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import csv

writer = csv.writer(open(parameters.result_file, 'w'))
writer.writerow(['name', 'job', 'location', 'ln_url'])

driver = webdriver.Chrome()
driver.maximize_window()
sleep(0.5)

driver.get('https://www.linkedin.com/')
sleep(5)

driver.find_element(By.XPATH, '//a[@class="nav__button-secondary btn-md btn-secondary-emphasis"]').click()
sleep(3)

username_input = driver.find_element(By.NAME, 'session_key')
username_input.send_keys(parameters.username)
sleep(0.5)

password_input = driver.find_element(By.NAME, 'session_password')
password_input.send_keys(parameters.password)
sleep(0.5)

# click on the sign in button
driver.find_element(By.XPATH, '//button[@class="btn__primary--large from__button--floating"]').click()
sleep(5)

driver.get('https://www.google.com/')
sleep(5)

search_input = driver.find_element(By.NAME, 'q')
search_input.send_keys(parameters.search_query) 
sleep(1)

search_input.send_keys(Keys.RETURN)
sleep(3)

profiles = driver.find_elements(By.XPATH, '//*[@class="yuRUbf"]/a')
profiles = [profile.get_attribute('href') for profile in profiles]

for profile in profiles:
    driver.get(profile)
    sleep(5)

    sel = Selector(text=driver.page_source)
    name = sel.xpath('//title/text()').extract_first().split(' | ')[0]
    job = sel.xpath('//*[@class="text-body-medium break-words"]/text()').extract_first().strip()
    location = sel.xpath('//*[@class="text-body-small inline t-black--light break-words"]/text()').extract_first().strip()
    ln_url = driver.current_url

    print('\n')
    print(name)
    print(job)
    print(location)
    print(ln_url)
    print('\n')

    writer.writerow([name, job, location, ln_url])
driver.quit()
