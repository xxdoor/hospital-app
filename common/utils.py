#!/bin/env python
# -*- coding: utf-8 -*-
# 工具模块
import random
import time

from common import readConfig


def get_nonce(length=12):
	"""
	返回随机字符串
	:param length:
	:return:
	"""
	pool = "1234567890abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ";
	pool_length = len(pool)
	nonce = ""
	for item in range(0, length):
		index = random.randint(0, pool_length)
		nonce += pool[index]
	return nonce


def get_timestamp():
	"""
	返回秒级时间戳
	:return:
	"""
	return int(time.time())


def get_app_id():
	"""
	返回appId
	:return:
	"""
	return readConfig.ReadConfig().read("app_id")


