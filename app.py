#!/bin/env python
# -*- coding: utf-8 -*-
# TODO 去掉原生日志
from flask_api import FlaskAPI
from flask_api import status
from flask import request
import hashlib
import flask

from common import readConfig, rest_log

app = FlaskAPI(__name__)
log_kit = rest_log.RestLog()
app.before_request(log_kit.log_request)


def make_response(content, code=status.HTTP_200_OK):
    """
    覆盖原方法，用来打日志
    :param content:
    :param code:
    :return:
    """
    response = flask.make_response(content, code)
    log_kit.log_response(flask.request, response)
    return response


@app.route('/')
def hello_world():
    response = make_response('Hello World!')
    return response


@app.route('/wx')
def verify_wx():
    """
    微信校验接口
    """
    params = request.args
    kvs = {}
    kvs['timestamp'] = params.get('timestamp')
    kvs['nonce'] = params.get('nonce')
    kvs['token'] = readConfig.ReadConfig().read('token')
    signature = params.get('signature')
    echostr = params.get('echostr')

    # 开始校验
    keys_list = ['token', 'timestamp', 'nonce']
    keys_list = sorted(keys_list)
    raw_str = ''
    for index in keys_list:
        raw_str += kvs[index]
    hash_str = hashlib.sha1(raw_str).hexdigest()
    if signature == hash_str:
        content = {'echostr': echostr}
    else:
        content = 'Signature error!'
    response = make_response(content, status.HTTP_200_OK)
    # response, status, headers
    return response


if __name__ == '__main__':
    app.run(port=5000, host='127.0.0.1', debug=True)
