#!/bin/env python
# -*- coding:utf-8 -*-

import redis

import log
import readConfig


class EditRedis(object):
	"""
	用于操作redis
	"""
	def __init__(self):
		"""
		读取redis配置
		"""
		rc = readConfig.ReadConfig()
		redis_conf = rc.read_section('redis')
		redis_host, redis_port = redis_conf['host'], redis_conf['port']
		self.redis = redis.Redis(host=redis_host, port=redis_port)
		self.redis_key = rc.read_section('redis-key')
		self.logger = log.Log().get_logger(__name__)

	# 操作accessToken
	def set_access_token(self, access_token):
		"""
		设置access_token
		:return: True/False
		"""
		key = self.redis_key['WX_ACCESSTOKEN']
		duration = self.redis_key['duration']
		self.logger.debug('Redis set [key]:%s, [value]:%s, [duration]:%ss' % (key, access_token, duration))
		return self.redis.setex(key, duration, access_token)

	def get_access_token(self):
		"""
		取access_token
		:return:
		"""
		key = self.redis_key['WX_ACCESSTOKEN']
		value = self.redis.get(key)
		self.logger.debug('Redis get %s - %s' % (key, value))
		return value


if __name__ == '__main__':
	er = EditRedis()
	er.set_access_token(u"这是accessToken!")
	count = 10
	while count:
		count -= 2
		er.get_access_token()

