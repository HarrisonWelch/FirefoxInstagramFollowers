from selenium import webdriver
from time import sleep
from selenium.common.exceptions import NoSuchElementException

browser = webdriver.Firefox()
browser.implicitly_wait(5)
browser.get('https://www.instagram.com/')


email = ""
username = ""
password = ""

username_input = browser.find_element_by_css_selector("input[name='username']")
password_input = browser.find_element_by_css_selector("input[name='password']")
username_input.send_keys(username)
password_input.send_keys(password)
login_button = browser.find_element_by_xpath("//button[@type='submit']")
login_button.click()

try:
    avatar_button = browser.find_element_by_xpath('//*[@alt="'+str(username)+'\'s profile picture"]')
    avatar_button.click()
    print('Clicked "Avatar" Button')
except NoSuchElementException as nsee:
    print('Didn\'t find the Avatar Button.')

try:
    profile_menu_option = browser.find_element_by_xpath('//a[@href="/'+str(username)+'/"]')
    profile_menu_option.click()
    print('Clicked "Profile menu option" Button')
except NoSuchElementException as nsee:
    print('Didn\'t find the "Profile menu option" Button.')

try:
    following_button = browser.find_element_by_xpath('//a[@href="/'+str(username)+'/following/"]')
    following_button.click()
    print('Clicked "Following" Button')
except NoSuchElementException as nsee:
    print('Didn\'t find the Following Button.')
sleep(2)
