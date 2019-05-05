from PO.login_page import LoginPage
from PO.load_data import load_data
from selenium import webdriver
import time

driver = webdriver.Chrome()
driver.maximize_window()
tem_data = ["data1","data2"]
data = load_data(tem_data[0])
login_obj = LoginPage(driver)
login_obj.click_login(**data)
time.sleep(1)
login_obj.fatie(**data)
time.sleep(10)
driver.quit()