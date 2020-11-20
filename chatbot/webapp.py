#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author : SMP-MCC评测会务组
# @Email  : smp_mcc@163.com
# @About  :
#   SMP机器人群聊比赛（SMP-MCC）参赛队伍机器人API搭建脚本
#   该脚本需要 flask 库支持，请自行安装（pip install flask）
#   如有任何疑问，请随时联系评测会务组

import time
from flask import Flask, jsonify, request
from dialog_bot import ChatBot

app = Flask(__name__)

# TODO: 初始化您的模型
# eg.
bot = ChatBot("baidu.json", "name_embeddings.pt")

@app.route("/hello", methods=["GET"])
def hello():
    return "hello"

@app.route('/get_resp', methods=["POST", "GET"])
def get_res():
    # 获取群聊请求数据
    # type: json
    data = request.json
    """
    data = {
        # 当前群聊唯一id
        "group_id": group_id, 

        # 当前群聊主题
        "topic": topic,

        # 您的机器人唯一id
        "robot_id": your_robot_id, 

        # 自该机器人上次回复之后的群聊消息记录
        # 按时间顺序保存
        "msgs": [
            {
                "from_id": robot_id, # 群聊机器人唯一id
                "msg": msg, # 群聊消息
                "timestamp": timestamp # 消息时间
            },
            ...
        ]
    }
    """

    # TODO: 在这里给出参赛机器人的群聊回复
    # 注意：timeout=10s，超时视为回复失败
    #（请不要在这里初始化模型，避免每次请求都初始化）
    # eg.
    msg = bot.get_res(data)

    # 返回您的机器人回复
    res = {
        "msg": msg,
        "from_id": data["robot_id"],
        "timestamp": time.time() 
    }
    return jsonify(res)


if __name__ == '__main__':
    # 该服务将运行在 http://0.0.0.0:10240/
    # 机器人API为 http://your_ip:10240/get_res（请将该URL提交给会务组）
    # 参赛队伍可以根据情况自行修改运行端口
    # 注意：请确保您的服务器对应端口是开启的
    app.run(host="0.0.0.0", port=10240)