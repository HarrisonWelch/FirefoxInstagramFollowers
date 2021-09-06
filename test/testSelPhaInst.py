from selenium import webdriver
import time

driver = webdriver.PhantomJS()
driver.set_window_size(1120, 550)
driver.get("https://www.instagram.com/accounts/login/")

time.sleep(5)
print('sleep 5')
time.sleep(5)
print('sleep 10')
time.sleep(5)
print('sleep 15')

username = driver.find_element_by_name('username')

driver.quit()

# from selenium import webdriver
# driver = webdriver.PhantomJS()
# driver.set_window_size(1120, 550)
# driver.get("https://www.google.com/")

# # driver.find_element_by_id('search_form_input_homepage').send_keys("realpython")

# username = driver.find_element_by_name('q')

# driver.quit()
