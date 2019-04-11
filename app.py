#!/bin/env python
# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf8')
import json

from flask_api import FlaskAPI
from flask_api import status
from flask_cors import CORS
from flask import request
import hashlib
import flask

from common import readConfig
from common import rest_log
from common import edit_redis
from common import utils
from common import mysqlUtils


app = FlaskAPI(__name__)
CORS(app)
log_kit = rest_log.RestLog()
app.before_request(log_kit.log_request)


def make_response(content, code=status.HTTP_200_OK):
    """
    覆盖原方法，用来打日志，并构造返回内容
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


@app.route('/wx', methods=['GET', 'POST'])
def verify_wx():
    """
    微信校验接口（GET） & 用户点击菜单事件推送接口（POST）
    """
    if request.method == 'GET':
        params = request.args
        timestamp = params.get('timestamp')
        nonce = params.get('nonce')
        token = readConfig.ReadConfig().read('token')
        signature = params.get('signature')
        echostr = params.get('echostr')

        # 开始校验
        keys_list = [timestamp, nonce, token]
        keys_list = sorted(keys_list)
        raw_str = ''
        for item in keys_list:
            try:
                raw_str += item
            except TypeError:
                continue
        hash_str = hashlib.sha1(raw_str).hexdigest()
        if signature == hash_str:
            content = echostr
            response = make_response(content, status.HTTP_200_OK)
        else:
            content = 'Signature error!'
            response = make_response(content, status.HTTP_406_NOT_ACCEPTABLE)
        # response, status, headers
        return response
    else:
        response = make_response('Ok')
        return response


@app.route('/access_token')
def get_access_token():
    """
    获取当前wx access_token
    :return:
    """
    redis = edit_redis.EditRedis()
    access_token = redis.get_access_token()
    content = {
        'access_token': access_token
    }
    response = make_response(content, status.HTTP_200_OK)
    return response


@app.route("/api/detail/<id>")
def get_detail(id):
    """
    根据id获取首页文案
    :param id:
    :return:
    """
    # 拉取title
    mysql_utils = mysqlUtils.MysqlUtils()
    title_cmd = "SELECT id, title, subTitle FROM `page` WHERE name=\"" + id + "\";"
    page_id, title, subTitle = mysql_utils.execute("hospital", title_cmd)[0]

    # 拉取内容
    content_cmd = "SELECT path, sequence, title, subTitle, text FROM `content` WHERE " \
                  "page_id = \"" + str(page_id) + "\";"
    content = mysql_utils.execute("hospital", content_cmd)
    # 按照sequence排序
    sorted_content = sorted(content, key=lambda x: x[1])
    res_content = []
    keys = ["url", "sequence", "title", "subTitle", "text"]
    # 当前服务host
    host = readConfig.ReadConfig().read("host", section="service")
    # 拼接返回内容
    for item in sorted_content:
        dict_item = dict(map(lambda x,y: (x, y), keys, item))
        dict_item["url"] = "http://%s/api/resource" % host + dict_item["url"]
        res_content.append(dict_item)
    data = {
        "title": title,
        "subTitle": subTitle,
        "id": id,
        "content": res_content
    }
    data = json.dumps(data)
    return make_response(data)


@app.route("/api/js_sdk", methods=['POST'])
def get_sdk_params():
    """
    获取前端调用js_sdk的参数
    :return:
    """
    # 获取ticket
    redis = edit_redis.EditRedis()
    ticket = redis.get_js_ticket()
    # 生成参数
    nonce = utils.get_nonce()
    timestamp = utils.get_timestamp()
    url = request.data.get("url")
    raw_str = "jsapi_ticket=%s&noncestr=%s&timestamp=%s&url=%s" % (ticket, nonce, timestamp, url)
    hash_str = hashlib.sha1(raw_str).hexdigest()
    # 返回内容
    data = {
        "appId": utils.get_app_id(),
        "timestamp": timestamp,
        "nonceStr": nonce,
        "signature": hash_str
    }
    return make_response(data)


@app.route("/api/resource/<path:resource>", methods=["GET"])
def get_resource(resource):
    """
    下载图片
    :return:
    """
    # 资源base路径
    base_path = readConfig.ReadConfig().read("base_path", section="pictures")
    path = base_path + "/" + resource
    with open(path, "rb") as fin:
        img_stream = fin.read()
    image_type = "image/" + resource.split(".")[1]
    return flask.send_file(img_stream, mimetype=image_type)


if __name__ == '__main__':
    app.run(port=8888, host='127.0.0.1', debug=False)
