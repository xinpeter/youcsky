from PO.login_page import LoginPage
from PO.load_data import load_data
from selenium import webdriver
import time
while True:
    list = load_data()
    for i in list.items():
        print(i[1]["username"])
        driver = webdriver.Chrome()
        driver.maximize_window()
        data = load_data()
        login_obj = LoginPage(driver)
        login_obj.click_login(**i[1])
        time.sleep(1)
        login_obj.fatie(**i[1])
        time.sleep(1)
        login_obj.modify(**i[1])
        time.sleep(10)
        login_obj.check()
        time.sleep(1)
        login_obj.logout()
        driver.quit()
        time.sleep(3600)