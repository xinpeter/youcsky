import re, requests, time, random
import yaml, os

base = os.path.dirname(os.path.dirname(__file__))

#读取数据
def load_data():
    print(base)
    with open("data.yml", "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    return data


class Youcsky(object):
    #UA
    headers = {
        "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1"}
    headers_pc = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36"}
    #             "Content-Type": "multipart/form-data; boundary=------WebKitFormBoundary3WKkN5pXd6HiAsqy"
    headers_pc1 = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36",
        "Referer": "http://www.youcsky.com/forum.php?mod=post&action=edit&fid=40&tid=1320136&pid=4637902&page=1",
        "Origin": "http://www.youcsky.com",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3"}

    #登录url
    login_url = "http://www.youcsky.com/member.php?mod=logging&action=login&mobile=2"

    def __init__(self):
        self.session = requests.Session()

    #获取formhas and loginhash
    def get_hash(self, url):
        r = self.session.get(url, headers=self.headers).text
        self.r = r
        self.formhash = re.findall('"formhash" value=.(.{8})', r)[0]
        try:
            self.loginhash = re.findall("loginhash=(.{5})", r)[0]
        except:
            pass

    def get_hash2(self, url):
        r = self.session.get(url, headers=self.headers_pc).text
        self.r = r
        self.formhash = re.findall('"formhash" value=.(.{8})', r)[0]


    #登录
    def login(self, username, password):
        self.username = username
        self.get_hash(self.login_url)
        self.post_login_url = "http://www.youcsky.com/member.php?mod=logging&action=login&loginsubmit=yes&loginhash=" + self.loginhash + "&mobile=2&handlekey=loginform&inajax=1"
        data = {
            "formhash": self.formhash,
            "referer": "http: // www.youcsky.com / forum.php?mobile = 2",
            "fastloginfield": "username",
            "cookietime": 2592000,
            "username": username,
            "password": password,
            "questionid": 0,
            "answer": ""
        }
        r = self.session.post(self.post_login_url, data=data, headers=self.headers).text
        t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        if "欢迎您回来" in r:
            print(t," 登陆成功",username)

    #发帖
    def posting(self, message):
        self.message = message
        self.get_hash("http://www.youcsky.com/forum.php?mod=post&action=newthread&fid=40&mobile=2")
        post_url = "http://www.youcsky.com/forum.php?mod=post&action=newthread&fid=40&extra=&topicsubmit=yes&mobile=2"
        subject = "".join(random.choices("qwertyuiopasdfghjklzxcvbnm", k=15))
        t = int(time.mktime(time.localtime()))
        data = {
            "formhash": self.formhash,
            "posttime": t,
            "topicsubmit": "yes",
            "subject": subject,
            "message": message,
            "Filedata": "",
        }
        r = self.session.post(post_url,data=data,headers = self.headers)
        print(r.url)

        self.new_url = r.url

    #修改标题
    def modify(self,subject):
        self.get_hash(self.new_url)
        post_url = "http://www.youcsky.com/forum.php?mod=post&action=edit&extra=&editsubmit=yes"
        pid = re.findall('pid(.+?)"',self.r)[0]
        tid = re.findall('tid=(.+?)&',self.r)[0]
        t = int(time.mktime(time.localtime()))

        params = {"formhash": (None, self.formhash), "posttime": (None, t), "delattachop": (None, 0), "wysiwyg": (None, 1),
                  "fid": (None, 40),"tid": (None, tid),"pid": (None, pid),
                  "page": (None, 1),"subject": (None, subject),"message": (None, self.message),"romotepic": (None, 1),"readperm": (None, ""),
                  "allownoticeauthor": (None, 1),"usesig": (None, 1),"save": (None, "")}

        self.new_url = self.session.post(post_url,files=params,headers=self.headers_pc).url
        r = self.session.get(self.new_url,headers=self.headers_pc).text
        t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        print(t,"发帖成功",self.username)

    #登出
    def logout(self):
        #获取formhash
        self.get_hash(self.new_url)
        #登出
        self.session.get("http://www.youcsky.com/member.php?mod=logging&action=logout&formhash={}".format(self.formhash))

    #查看IP
    def ip(self):
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36"}
        i = requests.get("http://ip.tool.chinaz.com", headers=self.headers_pc).text
        i = re.findall('<dd class="fz24">(.+)</dd>', i)
        print(i)

    #查询星星币
    def check_star(self):
        r = self.session.get("http://www.youcsky.com/forum-40-1.html",headers=self.headers).text
        uid = re.findall("uid = '(.{5})",r)[0]
        myspace = "http://www.youcsky.com/home.php?mod=space&uid="+uid
        r = self.session.get(myspace,headers=self.headers).text
        xingxing = re.findall("<span>(.+?)</span>星星币",r)[0]
        print("星星币剩余：" ,xingxing)




if __name__ == '__main__':
    youcsky = Youcsky()
    while True:
        l = load_data()
        for i in l.items():
            c_time = int(time.strftime("%H", time.localtime()))
            while 0 <= c_time <= 9 or 11 <= c_time < 12 or 12 < c_time < 16 or 24 < c_time < 24:
                print("非工作时间等待600秒")
                youcsky.ip()
                time.sleep(600)

                c_time = int(time.strftime("%H", time.localtime()))
            try:
                youcsky.login(i[1].get("username"), i[1].get("password"))
                time.sleep(1)
                youcsky.posting(i[1].get("message"))
                time.sleep(1)
            except:
                print(i[1].get("username"),"发帖失败")
                youcsky.logout()
                continue
            youcsky.modify(i[1].get("subject"))
            time.sleep(1)
            youcsky.ip()
            youcsky.check_star()
            time.sleep(1)
            youcsky.logout()
            time.sleep(3600)