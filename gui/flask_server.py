import base64
# import imp
import json
import time

import pyaudio
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS

import fay_booter

from core.tts_voice import EnumVoice
from gevent import pywsgi
from scheduler.thread_manager import MyThread
from utils import config_util, util
from core import wsa_server
from core import fay_core
from core.content_db import Content_Db
from ai_module import yolov8


__app = Flask(__name__)
CORS(__app, supports_credentials=True)


def __get_template():
    return render_template('index.html')

# 设备列表
def __get_device_list():
    audio = pyaudio.PyAudio()
    device_list = []
    for i in range(audio.get_device_count()):
        devInfo = audio.get_device_info_by_index(i)
        if devInfo['hostApi'] == 0:
            device_list.append(devInfo["name"])
    
    return list(set(device_list))


@__app.route('/api/submit', methods=['post'])
def api_submit():
    data = request.values.get('data')
    print(data)
    config_data = json.loads(data)
    if(config_data['config']['source']['record']['enabled']):
        config_data['config']['source']['record']['channels'] = 0
        audio = pyaudio.PyAudio()
        for i in range(audio.get_device_count()):
            devInfo = audio.get_device_info_by_index(i)
            if devInfo['name'].find(config_data['config']['source']['record']['device']) >= 0 and devInfo['hostApi'] == 0:
                 config_data['config']['source']['record']['channels'] = devInfo['maxInputChannels']

    config_util.save_config(config_data['config'])

    return '{"result":"successful"}'


# 接收图片
@__app.route('/receive-image', methods=['POST'])
def receive_image():
    try:
        # 获取POST请求中的JSON数据，其中包含Base64编码的图片数据
        # 获取请求的 JSON 数据
        data = request.json
        print(data)
        # 获取图片的 base64 编码
        # image_base64 = data['image_base64']
        # print(image_base64)


        if 'image_base64' in data:
            # 提取Base64编码的图片数据
            image_base64 = data.get("image_base64")

            # 将Base64编码转换为图片文件
            image_data = base64.b64decode(image_base64)
            # print(image_data)
            image_url = "C:/学习/项目/Fay-main/gui/templates/picture.jpg"  # 设置图片保存路径
            with open(image_url, 'wb') as f:
                f.write(image_data)
            # 假设 image_base64 是包含 Base64 编码的字符串
            # image_data = base64.b64decode(image_base64)
            # print(image_data)
            # txt_file_url = "C:/Users/11605/Desktop/base64_data.txt"  # 设置 txt 文件保存路径
            # with open(txt_file_url, 'w') as f:  # 将写入模式改为文本写入模式
            #     f.write(image_data.decode('utf-8'))  # 将二进制数据写入到 txt 文件中
            # 返回图片文件的URL给前端
            # image_url = f'http://127.0.0.1:5000/{image_path}'  # 设置图片文件在服务器上的访问URL
            return jsonify({"status": "success", "image_data": "图片接收成功"})

            # return jsonify({"status": "success", "image_url": image_url})

        else:
            return jsonify({"status": "error", "message": "缺少图片数据"})

    except Exception as e:
        return jsonify({"status": "error", "message": "图片接收失败", "error": str(e)})


# 加载文本
@__app.route('/api/get-text', methods=['GET'])
def process_text():
    text_data = {
        'user_name': "张三",
        'user_gender': "男",
    }
    return jsonify({"text": text_data})


@__app.route('/api/robot_data', methods=['POST'])
def get_robot_data():
    data = request.get_json()  # 获取 POST 请求中的 JSON 数据
    response_data = {'message': 'Data received successfully'}
    return jsonify(response_data)


# 提交用户信息
@__app.route('/api/post-user-inform', methods=['post'])
def api_post_user_inform():
    data = request.values.get('data')
    print(data)
    config_data = json.loads(data)

    return config_data


# @__app.route('/api/control-eyes', methods=['post'])
# def control_eyes():
#     eyes = yolov8.new_instance()
#     if(not eyes.get_status()):
#        eyes.start()
#        util.log(1, "YOLO v8正在启动...")
#     else:
#        eyes.stop()
#        util.log(1, "YOLO v8正在关闭...")
#     return '{"result":"successful"}'


@__app.route('/api/get-data', methods=['post'])
def api_get_data():
    wsa_server.get_web_instance().add_cmd({
        "voiceList": [
            {"id": EnumVoice.XIAO_XIAO.name, "name": "晓晓"},
            {"id": EnumVoice.YUN_XI.name, "name": "云溪"}
        ]
    })
    wsa_server.get_web_instance().add_cmd({"deviceList": __get_device_list()})
    return json.dumps({'config': config_util.config})


@__app.route('/api/start-live', methods=['post'])
def api_start_live():
    # time.sleep(5)
    fay_booter.start()
    time.sleep(1)
    wsa_server.get_web_instance().add_cmd({"liveState": 1})
    return '{"result":"successful"}'


@__app.route('/api/stop-live', methods=['post'])
def api_stop_live():
    # time.sleep(1)
    fay_booter.stop()
    time.sleep(1)
    wsa_server.get_web_instance().add_cmd({"liveState": 0})
    return '{"result":"successful"}'

@__app.route('/api/send', methods=['post'])
def api_send():
    data = request.values.get('data')
    info = json.loads(data)
    text = fay_core.send_for_answer(info['msg'],info['sendto'])
    return '{"result":"successful","msg":"'+text+'"}'



@__app.route('/api/get-msg', methods=['post'])
def api_get_Msg():
    contentdb = Content_Db()
    list = contentdb.get_list('all','desc',1000)
    relist = []
    i = len(list)-1
    while i >= 0:
        relist.append(dict(type=list[i][0], way=list[i][1], content=list[i][2], createtime=list[i][3], timetext=list[i][4]))
        i -= 1

    return json.dumps({'list': relist})



@__app.route('/api/get-location', methods=['get'])
def api_get_loacation():
    return '{"location":"厨房"}'


@__app.route('/api/post-location', methods=['post'])
def api_post_location():
    return '{"result":"successful"}'


@__app.route('/', methods=['get'])
def home_get():
    return __get_template()


def run():
    server = pywsgi.WSGIServer(('0.0.0.0',5000), __app)
    server.serve_forever()


def start():
    MyThread(target=run).start()

if __name__ == '__main__':
    __app.run()