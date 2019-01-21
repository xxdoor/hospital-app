#!/bin/env python
# -*- coding: utf-8 -*-
from configobj import ConfigObj

from common import log


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

	def read_section(self, section):
		"""
	    读取file中的section
	    :param section:
	    :return:
	    """
		try:
			section_dict = self.cf[section]
		except KeyError:
			self.logger.error(u'Get config: %s error!' % section)
			section_dict = {}
		return section_dict


if __name__ == '__main__':
	temp = ReadConfig()
	temp.read('token')
