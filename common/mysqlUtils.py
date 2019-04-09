#!/bin/env python
# -*- coding: utf-8 -*-
import mysql.connector

import readConfig
import log


class MysqlUtils(object):
	"""
	mysql client
	"""
	def __init__(self):
		self.cf = readConfig.ReadConfig()
		self.logger = log.Log().get_logger(__name__)

	def init_db(self, db):
		"""
		初始化db
		:return:
		"""
		mysql_config = self.cf.read_section("mysql")
		host = mysql_config.get("host")
		user = mysql_config.get("user")
		password = mysql_config.get("password")
		try:
			db = mysql.connector.connect(user=user, password=password, host=host, database=db)
		except mysql.connector.Error as err:
			self.logger.error(err)

		return db

	def execute(self, db, cmd):
		"""
		执行cmd并commit
		:param cmd:
		:return:
		"""
		db = self.init_db(db)
		cursor = db.cursor()
		influence = cursor.execute(cmd)
		values = cursor.fetchall()
		cursor.commit()
		cursor.close()
		db.close()
		self.logger.info("DB: %s, operation: %s, result: %s" % (db, cmd, influence))
		return values




