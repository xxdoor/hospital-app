#!/bin/env python
# -*- coding: utf-8 -*-
import logging
import os
from logging.handlers import TimedRotatingFileHandler

from common import readConfig

class Log(object):
    """
    log配置文件
    """
    def __init__(self):
        self.level = logging.DEBUG
        cf = readConfig.ReadConfig().read_section('log')
        self.common_path = cf['common']
        self.update_path = cf['update']

    def get_logger(self, name):
        """
        :param name:
        :return: 返回logger
        """
        if logging.getLogger(name).handlers:
            return logging.getLogger(name)
        logger = logging.getLogger(name)
        logger.setLevel(self.level)
        # console handler
        console_handler = logging.StreamHandler()
        formatter = logging.Formatter(fmt='%(asctime)s: %(levelname)s '
                                        '%(message)s', datefmt='%m-%d %H:%M:%S')
        console_handler.setFormatter(formatter)
        console_handler.setLevel(self.level)
        logger.addHandler(console_handler)
        # file handler
        dir_name = os.path.dirname(self.common_path)
        if not os.path.exists(dir_name):
            os.makedirs(dir_name)
        file_handler = TimedRotatingFileHandler(self.common_path, when='D', interval=7, backupCount=4)
        file_handler.setFormatter(formatter)
        file_handler.setLevel(self.level)
        logger.addHandler(file_handler)
        return logger

    def get_update_logger(self):
        """ 记录更新accessToken日志的logger """
        if logging.getLogger('update').handlers:
            return logging.getLogger('update')
        logger = logging.getLogger('update')
        logger.setLevel(self.level)
        # file handler
        dir_name = os.path.dirname(self.update_path)
        if not os.path.exists(dir_name):
            os.makedirs(dir_name)
        formatter = logging.Formatter(fmt='%(asctime)s: %(levelname)s '
                                          '%(message)s', datefmt='%m-%d %H:%M:%S')
        file_handler = TimedRotatingFileHandler(self.update_path, when='D', interval=7, backupCount=4)
        file_handler.setFormatter(formatter)
        file_handler.setLevel(self.level)
        logger.addHandler(file_handler)
        return logger




