#!/bin/env python
# -*- coding: utf-8 -*-
from flask_api import FlaskAPI
from flask import request
import hashlib

import readConfig

app = FlaskAPI(__name__)


@app.route('/')
def hello_world():
    return 'Hello World!'


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
    app.logger.info('Return %s' % content)
    return content


if __name__ == '__main__':
    app.run(port=5000, host='127.0.0.1', debug=True)
