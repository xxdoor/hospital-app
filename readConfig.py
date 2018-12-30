#!/bin/env python
# -*- coding: utf-8 -*-
from configobj import ConfigObj

import log


class ReadConfig(object):
    """
    读取配置文件
    """
    def __init__(self):
        self.file = './config.ini'
        self.cf = ConfigObj(self.file)
        self.logger = log.Log().get_logger(__name__)

    def read(self, key, section='app'):
        """
        读取file中section的key值
        :param key: key
        :param section: section
        :return: 对应value
        """
        try:
            value = self.cf[section][key]
        except KeyError:
            self.logger.error(u'Get %s in %s error!' % (key, section))
            value = None
        return value


if __name__ == '__main__':
    temp = ReadConfig()
    temp.read('token')
