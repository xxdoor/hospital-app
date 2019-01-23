#!/bin/env python
# -*- coding: utf-8 -*-
# 使用requests库做HTTP请求
import requests

from common import rest_log


def request(url, method='GET', params=None, headers=None, body=None):
	""" 做请求并打日志 """
	logger_kit = rest_log.RestLog()
	try:
		result = requests.request(method, url, params=params, headers=headers, data=body)
	except requests.exceptions as e:
		result = e
	logger_kit.log_http_request(url, method, params, headers, body)
	logger_kit.log_http_response(url, result)
	return result