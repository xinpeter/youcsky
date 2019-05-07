from PO.login_page import LoginPage
from PO.load_data import load_data
from selenium import webdriver
import time

driver = webdriver.Chrome()
driver.maximize_window()
tem_data = ["data1","data2"]
data = load_data()
login_obj = LoginPage(driver)
try:
    login_obj.adsl()
except Exception as e:
    print(e)
finally:
    driver.quit()