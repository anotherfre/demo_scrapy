from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


def login():
    browser = webdriver.Edge()
    url = 'https://www.zhihu.com/signin?next=%2Fhot'
    browser.get(url)
    wait = WebDriverWait(browser, timeout=10)
    wait.until(EC.presence_of_all_elements_located((By.XPATH, '//div[@class="SignFlow-tab"]')))
    pwd_login_btn = browser.find_element_by_xpath('//div[@class="SignFlow-tab"]')
    pwd_login_btn.click()
    username_input = browser.find_element_by_xpath('//input[@name="username"]')
    username_input.send_keys(USERNAME)
    pwd_input = browser.find_element_by_xpath('//input[@name="password"]')
    pwd_input.send_keys(PASSWORD)
    pwd_input.send_keys(Keys.ENTER)
    print(browser.page_source)
    pass


if __name__ == '__main__':
    login()
