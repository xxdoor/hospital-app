#!/bin/env python
# -*- coding: utf-8 -*-
# 用来为RESTFUL请求打日志
import flask
from requests import Response

import log


class RestLog(object):
	"""
	HTTP请求和响应打日志类
	"""
	def __init__(self):
		self.logger = log.Log().get_logger(__name__)

	def log_request(self):
		"""
		为flask请求打日志
		:return:
		"""
		# 根据上下文获取全局变量request
		request = flask.request
		url = request.base_url
		method = request.method
		args = request.args.to_dict()
		headers = request.headers
		try:
			form = request.data.to_dict()
		except AttributeError:
			form = request.data
		remote_addr = request.remote_addr
		if method in ['GET', 'HEAD']:
			self.logger.debug('%s ====> %s, [method]: %s, [args]: %s, [headers]: %s' % (remote_addr, url, method, args, headers))
		else:
			self.logger.debug('%s ===> %s, [method]: %s, [args]: %s, [headers]: %s, [data]: %s' % (remote_addr, url, method, args, headers, form))

	def log_response(self, request, response):
		"""
		为flask响应打日志
		:param response:
		:return:
		"""
		status = response.status
		data = response.data
		coming_url = request.url
		self.logger.debug('%s <==== [status]: %s, [response]: %s' % (coming_url, status, data))

	def log_http_request(self, url, method, params=None, headers=None, body=None):
		"""
		为HTTP请求打日志
		:param url:
		:param method:
		:param params:
		:param headers:
		:param body:
		:return:
		"""
		self.logger.debug('====> %s, [method]: %s, [params]: %s, [headers]: %s, [body]: %s'
		                  % (url, method, params, headers, body))

	def log_http_response(self, request_url, response):
		"""
		为HTTP应答打日志
		:param response:
		:return:
		"""
		if isinstance(response, Response):
			self.logger.debug('<==== %s [status]: %s, [content]: %s' % (request_url, response.status_code, response.json()))
		else:
			self.logger.error('%s <==== [error]: %s' % (request_url, response))


