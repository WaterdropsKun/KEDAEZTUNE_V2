# _*_ coding: utf-8 _*_
import logging
import os.path
import time


class CLogNew(object):
    def __init__(self, logger = None):
        """
        指定保存日志的文件路径，日志级别，以及调用文件
        将日志存入到指定的文件中
        """
        # 创建一个logger
        self.logger = logging.getLogger(logger)
        self.logger.setLevel(logging.DEBUG)

        # 创建日志名称。
        self.log_time = time.strftime('%Y%m%d%H%M', time.localtime(time.time()))
        # os.getcwd()获取当前文件的路径，os.path.dirname()获取指定文件路径的上级路径
        self.log_path = os.getcwd() + "/Files/Logs/"
        # self.log_name = self.log_path + self.log_time + ".log"
        self.log_name = self.log_path + "DebugMK" + ".log"

        # 创建一个handler，用于写入日志文件
        fh = logging.FileHandler(self.log_name, 'w', encoding='utf-8')
        fh.setLevel(logging.INFO)

        # 创建一个handler，用于输出到控制台
        ch = logging.StreamHandler()
        ch.setLevel(logging.INFO)

        # 定义handler的输出格式
        formatter = logging.Formatter('[%(asctime)s] %(filename)s->%(funcName)s line:%(lineno)d [%(levelname)s]\n%(message)s\n')
        fh.setFormatter(formatter)
        ch.setFormatter(formatter)

        # 给logger添加handler
        self.logger.addHandler(fh)
        self.logger.addHandler(ch)

        #  添加下面一句，在记录日志之后移除句柄
        # self.logger.removeHandler(ch)
        # self.logger.removeHandler(fh)
        # 关闭打开的文件
        fh.close()
        ch.close()

    def getlog(self):
        return self.logger