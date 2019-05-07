import logging,time,os

class Log(object):
    def __init__(self):
        #创建logger，设置log级别
        self.logger = logging.getLogger()
        self.logger.setLevel(logging.DEBUG)

        #创建handler用于控制台输出
        self.ch = logging.StreamHandler()


        #创建handler用于写入文件
        self.log_time = time.strftime("%Y-%m-%d")
        base_dir = os.path.dirname(os.path.abspath(__file__))
        self.log_path = os.path.join(base_dir,"logs")
        self.log_name = self.log_path+os.sep+self.log_time+".log"
        self.fh = logging.FileHandler(self.log_name,'a',encoding="utf-8")
        formatter = logging.Formatter('[%(asctime)s] %(filename)s->%(funcName)s line:%(lineno)d [%(levelname)s]%(message)s')
        self.fh.setFormatter(formatter)
        self.ch.setFormatter(formatter)
        self.logger.addHandler(self.fh)
        self.logger.addHandler(self.ch)
        self.fh.close()
        self.ch.close()



    def getlog(self):
        return self.logger
