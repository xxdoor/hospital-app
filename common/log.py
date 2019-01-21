#!/bin/env python
# -*- coding: utf-8 -*-
import logging


class Log(object):
    """
    log配置文件
    """
    def __init__(self):
        self.level = logging.DEBUG

    def get_logger(self, name):
        """
        :param name:
        :return: 返回console logger
        """
        logger = logging.getLogger(name)
        logger.setLevel(self.level)
        console_handler = logging.StreamHandler()
        formatter = logging.Formatter(fmt='%(asctime)s: %(levelname)s '
                                        '%(message)s', datefmt='%m-%d %H:%M:%S')
        console_handler.setFormatter(formatter)
        console_handler.setLevel(self.level)
        logger.addHandler(console_handler)
        return logger
