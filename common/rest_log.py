#!/bin/env python
# -*- coding: utf-8 -*-
# 用来为RESTFUL请求打日志
import flask

from common import log


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
		form = request.data.to_dict()
		headers = request.headers
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


