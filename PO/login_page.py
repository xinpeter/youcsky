import random,socket
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from PO.base import Action
from selenium import webdriver
import time

class LoginPage(Action):
    login_BTN = (By.XPATH,'//*[@id="messagetext"]/p[1]/a/strong')
    username_loc = (By.XPATH,'//*[@name="username"]')
    password_loc = (By.XPATH,'//*[@name="password"]')
    submit_BTN = (By.XPATH,'//*[@name="loginsubmit"]')
    username = "renzhemao"
    password = "xiaomaomao1"
    subject_loc = (By.ID,"subject")
    message_loc = (By.CSS_SELECTOR,'body')
    tem_loc = (By.ID,"e_iframe")
    submit_fatie_BTN = (By.ID,"postsubmit")

    edit_loc = (By.XPATH,'//*[@class="editp"]')

    user_info_loc = (By.ID,"cuser")
    xingxing_loc = (By.XPATH,'//*[@id="psts"]/ul/li[4]')

    logout_loc = (By.XPATH,'//*[@id="comeing_toptb"]/div/div[2]/a[5]')

    admin_pass_loc = (By.ID,"pcPassword")
    admin_pass = "1234qwer"
    admin_ok_loc = (By.ID,"loginBtn")
    ip_loc = (By.XPATH,'/html/body/center/form/table[4]/tbody/tr[2]/td/table/tbody/tr[1]/td[2]/table/tbody/tr[2]/td[2]')
    frame_loc = (By.NAME,"mainFrame")
    disconnect_loc = (By.ID,"Disconnect")
    connect_loc = (By.ID,"Connect")

    login_url = "http://www.youcsky.com/member.php?mod=logging&action=login"
    fatie_url = "http://www.youcsky.com/forum.php?mod=post&action=newthread&fid=40"

    subject = random.randint(10000000,99999999)


    def setup(self):
        pass

    #登录
    def click_login(self,**data):
        self.username = data["username"]
        self.driver.get(self.login_url)
        self.find_element(*self.login_BTN).click()
        time.sleep(1)           #等待3秒，等待登录弹窗加载完成
        self.send_keys(self.username_loc,data["username"])
        self.send_keys(self.password_loc,data["password"])
        time.sleep(1)
        self.find_element(*self.submit_BTN).click()

    #发帖
    def fatie(self,**data):
        self.driver.get(self.fatie_url)

        self.send_keys(self.subject_loc, self.subject)
        time.sleep(3)
        # self.send_keys(self.message_loc,data["message"])

        # self.find_element(*self.message_loc).send_keys(Keys.TAB)
        # self.find_element(*self.message_loc).send_keys("aaa")
        iframe = self.find_element(*self.tem_loc)
        self.driver.switch_to_frame(iframe)
        self.find_element(*self.message_loc).send_keys(data["message"])
        self.driver.switch_to_default_content()


        time.sleep(10)
        target = self.find_element(*self.submit_fatie_BTN)
        self.driver.execute_script("arguments[0].scrollIntoView(false);", target)
        target.click()

    #修改帖子标题
    def modify(self,**data):
        # self.driver.get("http://www.youcsky.com/thread-1274607-1-1.html")
        target = self.find_element(*self.edit_loc)
        self.driver.execute_script("arguments[0].scrollIntoView(false);", target)
        target.click()
        time.sleep(1)
        self.send_keys(self.subject_loc,data["subject"])
        time.sleep(1)
        target = self.find_element(*self.submit_fatie_BTN)
        self.driver.execute_script("arguments[0].scrollIntoView(false);", target)
        target.click()

    #查询星星币
    def check(self):
        self.find_element(*self.user_info_loc).click()
        time.sleep(2)
        handles = self.driver.window_handles
        self.driver.switch_to_window(handles[1])
        target = self.find_element(*self.xingxing_loc)
        self.driver.execute_script("arguments[0].scrollIntoView(false);", target)
        print(self.username,target.text)

    #登出
    def logout(self):
        handles = self.driver.window_handles
        self.driver.switch_to_window(handles[0])
        target = self.find_element(*self.logout_loc)
        self.driver.execute_script("arguments[0].scrollIntoView();", target)
        target.click()
        time.sleep(2)

    #拨号
    def adsl(self):
        self.driver.get("http://192.168.1.1")
        self.send_keys(self.admin_pass_loc,self.admin_pass)
        self.find_element(*self.admin_ok_loc).click()
        frame = self.find_element(*self.frame_loc)
        self.driver.switch_to_frame(frame)
        ip = self.find_element(*self.ip_loc)
        print("发帖IP: ",ip.text)
        self.find_element(*self.disconnect_loc).click()
        self.find_element(*self.connect_loc).click()
        time.sleep(10)
        self.find_element(*self.disconnect_loc)
        ip = self.find_element(*self.ip_loc)
        print("新IP: ", ip.text)
        time.sleep(10)