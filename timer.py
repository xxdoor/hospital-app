#!/bin/env python
# -*- coding:utf-8 -*-
# 定时获取并更新redis中的accessToken
import threading

from common import edit_redis
from common import readConfig
from common import log
from common import request


class Timer(object):
	""" 定时器类"""
	def __init__(self, interval):
		"""
		:param interval: 定时器间隔(s)
		:param env: 环境(online、test)
		"""
		self.interval = interval
		self.redis = edit_redis.EditRedis()
		self.cf = readConfig.ReadConfig()
		self.logger = log.Log().get_update_logger()

	def get_access_token(self):
		""" 获取accessToken """
		url = self.cf.read('url', 'wx')
		method = 'GET'
		params = {
			'grant_type': 'client_credential',
			'appid': self.cf.read('app_id'),
			'secret': self.cf.read('app_secret')
		}
		result = request.request(url, method, params=params)
		text = result.json()
		access_token = text['access_token']
		self.redis.set_access_token(access_token)
		return access_token

	def get_js_ticket(self, access_token):
		"""
		获取js_ticket
		:return:
		"""
		url = self.cf.read('sdk_url', 'wx')
		method = 'GET'
		params = {
			"type": "jsapi",
			"access_token": access_token
		}
		result = request.request(url, method, params=params)
		text = result.json()
		ticket = text["ticket"]
		self.redis.set_js_ticket(ticket)

	def start(self):
		"""
		执行定时任务
		:return:
		"""
		global timer
		access_token = self.get_access_token()
		self.get_js_ticket(access_token)
		timer = threading.Timer(self.interval, self.start)
		timer.start()


if __name__ == '__main__':
	# 更新周期: 100min
	interval = 100 * 60
	timer_kit = Timer(interval)
	timer = threading.Timer(1, timer_kit.start)
	timer.start()
