#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2020-09-18 16:34:19
# @Author  : Kaiyan Zhang (minekaiyan@gmail.com)
# @Link    : https://github.com/iseesaw
# @Version : 1.0.0
import re
import logging
from flask import Flask, request, jsonify
from dialog_bot import ChatBot

app = Flask(__name__)

app.logger.setLevel(logging.INFO)

model = ChatBot("baidu.json", "name_embeddings.pt")

# TODO: 服务器部署时外部数据加载位置
#import sys
#sys.path.append("../../../../config")
#from base_config import BaseConfig
#BASE_DATA_DIR = BaseConfig.DATA_PATH
#DATA_DIR = os.path.join(BASE_DATA_DIR, "core/module/skill_modules/<TEST_MODULE>")

@app.route("/", methods=["GET"])
def get_index():
    return "Hello, here is test module."


@app.route("/", methods=["POST"])
def post_index():
    """
    Request:
    {
        'bot_config': {'address': '',
                        'age': 18,
                        'constellation': 'xxx',
                        'developer': 'xxx',
                        'father': 'xxx',
                        'gender': 0,
                        'hobby': 'xxx',
                        'intro': 'xxx',
                        'mother': 'xxx',
                        'name': 'xxx'},
        'bot_id': 'xxx-xxx-xxx',
        'content': '你好呀',
        'context': {}, # 该模块的多轮对话历史
        'metafield': {
            'emotion': 'just test',
            'ltp': {'arc': '0:HED 1:RAD',
                   'ner': 'O O',
                   'pos': 'i u',
                   'seg': '你好 呀'},
            'multi_turn_status_dict': {},
            'ner_word': ''},
        'msg_type': 'text',
        'user': {
            'id': 'xxx-xxx-xxx'
        }
    }

    Returns:
    {
        "msg_type": "text",
        "reply": "I am fine, how are you ?",
        "context": {}, # 该模块的多轮信息
        "status": 0, # 多轮状态标识
        "code": 1, # 单轮拒识标识（单轮模块必须）
        "metafield": {}
    }
    """
    data = request.json
    res = get_single_turn_question(data)
    #res = get_multi_turn_compute(data)
    return jsonify(res)


def get_single_turn_question(data):
    """（单轮模块案例）
    功能介绍：
        可用于系统demo展示，前端创建机器人唯一选择该模块
        同时该模块设置始终触发（code=1）即可

    Args:
        data (Dict): Ibid.

    Returns:
        Dict: Ibid.
    """
    content = data.get("content")
    reply =  model.get_res(content)
    return {
        "msg_type": "text",
        "reply": reply,
        "context": {},
        "status": 1,  # 单轮状态标识
        "metafield": {
            "code": 1 # 触发标识为1，表示始终触发
        } 
    }


def get_multi_turn_compute(data):
    """（多轮模块状态管理案例）多轮计算模式
    功能介绍：
        输入"开启多轮计算器"进入多轮
        进入多轮后，依次输入数字和运算符
        直到输入"计算结果"，则计算结果返回，并清除当前记录，等待新一轮计算

        用户输入"退出"、"结束"等话语时退出
        计算过程中输入不符合要求，包括不是数字、运算符，则提示用户
    Args:
        data (Dict): Ibid

    Returns:
        Dict: Ibid
    """
    content = data.get("content").strip().replace(" ", "")
    context = data.get("context")
    print(data, "<context>", context)
    # 当前模块是否处于多轮状态中
    mstat = context.get("mstat", False)
    # 模块触发分类器，例如简单关键字
    trigged = content == "开始多轮计算模式"

    reply = ""
    status = 1
    # 第一次触发
    if not mstat and trigged:
        reply = "下面开始多轮计算模式，请间轮输入数字和运算符（目前仅支持整数和 +, -, *, / 四种运算）"
        context["form"] = ""
        context["mstat"] = True
    # 处于多轮
    elif mstat:
        # 模块进行中状态
        # 上一轮输入情况，True表示是数字，则当前只能输入运算符
        last_digit = context.get("last_digit", False)

        is_ok = True
        # 主动退出，模块结束，返回3
        if content in ["退出", "结束"]:
            reply = "好的！"
            status = 3
        elif content == "=":
            try:
                reply = f"{context['form']} = {eval(context.get('form'))}"
            except Exception as e:
                reply = "计算出错！" + context.get('form') + "，" + str(e)
            finally:
                context["form"] = ""
                context["last_digit"] = False
        elif last_digit and content in ["+", "-", "*", "/"]:
            context["form"] += content
            context["last_digit"] = False
            reply = context["form"]
        elif not last_digit and re.match(r"\d+", content):
            context["form"] += content
            context["last_digit"] = True
            reply = context["form"]
        else:
            reply = "当前轮需要输入" + ("运算符(+, -, *, /)" if last_digit else "数字")
            is_ok = False

        # 识别用户多次非法输入
        if is_ok:
            context["count"] = 0
        else:
            context["count"] += 1

        # 超过阈值， 则主动结束
        if context["count"] >= 3:
            status = 4
    else:
        status = 0

    return {
        "msg_type": "text",
        "reply": reply,
        "context": context,
        "status": status,  # 多轮状态
        "metafield": {}
    }

# gunicorn -b 127.0.0.1:<PORT> -k eventlet --reload test_app:app