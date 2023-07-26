import base64
# import imp
import json
import sqlite3
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
from robot import client
from ai_module import yolov8
from ai_module import image_behavior

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


@__app.route('/api/get-medicine', methods=['POST'])
def receive_data():
    try:
        # 从请求中获取JSON数据
        data = request.get_json()
        print(data)
        # 检查是否包含所需的键
        if all(key in data for key in ['med_name', 'med_spec', 'med_usage', 'med_freq', 'med_dosage', 'med_num']):
            med_name = data['med_name']
            print(med_name)
            med_spec = data['med_spec']
            print(med_spec)
            med_usage = data['med_usage']
            med_freq = data['med_freq']
            med_dosage = data['med_dosage']
            med_num = data['med_num']

            # 在这里进行数据处理或数据库操作
            # 设置SQLite数据库连接
            conn = sqlite3.connect('fay.db')
            print(conn)
            cursor = conn.cursor()
            print(cursor)

            # 插入数据到数据库
            cursor.execute('''INSERT INTO med_inform (med_name, med_spec, med_usage, med_freq, med_dosage, med_num)
                                         VALUES (?, ?, ?, ?, ?, ?)''',
                           (med_name, med_spec, med_usage, med_freq, med_dosage, med_num))
            conn.commit()
            cursor.close()
            conn.close()

            response = {
                "status": "success",
                "message": "成功接收并处理数据",
                # "data": {
                #     "med_name": med_name,
                #     "med_spec": med_spec,
                #     "med_usage": med_usage,
                #     "med_freq": med_freq,
                #     "med_dosage": med_dosage,
                #     "med_num": med_dosage
                # }
            }
        else:
            response = {
                "status": "error",
                "message": "数据格式不正确，请提供所有必需的键名：med_name、med_spec、med_usage、med_freq、med_dosage、med_num"
            }

        return jsonify(response)

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})


# 加载用药信息
# @__app.route('/get-medicine', methods=['GET'])
# def get_medicine():
#     # try:
#         # 设置SQLite数据库连接
#         conn = sqlite3.connect('fay.db')
#         cursor = conn.cursor()
#         # 假设要获取id为1的药物信息
#         med_id = 1
#
#         # 从数据库中获取指定id的药物信息
#         cursor.execute('''SELECT * FROM med_inform WHERE id = ?''', (med_id))
#         row = cursor.fetchone()
#         print(row)
#
#         # 关闭数据库连接
#         conn.close()
#
#         # 如果存在指定id的药物信息，则将其转换为字典
#         if row is not None:
#             med_dict = {
#                 "med_name": row[0],
#                 "med_spec": row[1],
#                 "med_usage": row[2],
#                 "med_freq": row[3],
#                 "med_dosage": row[4],
#                 # "med_num": row[5]
#             }
#             print(med_dict)  # 输出指定id的药物信息
#         else:
#             print("未找到指定id的药物信息")
#
#         # 将字典列表转换为JSON格式的字符串
#         response_json_str = json.dumps({"status": "success", "data": med_dict})
#
#         # 返回JSON字符串
#         return response_json_str

    # except Exception as e:
    #     return jsonify({"status": "error", "message": str(e)})

@__app.route('/api/get-medicine', methods=['GET'])
def get_medicine_by_id():
    try:
        # 连接SQLite数据库
        conn = sqlite3.connect('fay.db')
        cursor = conn.cursor()

        med_id = 2
        # 从数据库中获取特定id的用药信息
        cursor.execute('SELECT * FROM med_inform WHERE id = ?', (med_id,))
        row = cursor.fetchone()

        # 关闭数据库连接
        cursor.close()
        conn.close()

        # 将查询结果转换为字典

        if row:
            med_dict = {
                "med_name": row[1],
                "med_spec": row[2],
                "med_usage": row[3],
                "med_freq": row[4],
                "med_dosage": row[5],
                "time": row[6]
            }
            response = {
                "status": "success",
                "data": med_dict

            }
        else:
            response = {
                "status": "error",
                "message": "未找到该用药信息"
            }

        # 将字典转换为JSON格式的响应并返回
        return jsonify(response)

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})



@__app.route("/robot/send_msg", methods=["POST"])
def receive_message():
    payload = request.json
    kafka_ip = payload["kafka_ip"]
    topic_name = payload["topic_name"]
    message = payload["message"]

    # Process to send message
    client.send_message_to_kafka(kafka_ip, topic_name, message)
    response = {'message': 'send successfully'}
    return jsonify(response), 200  # 返回响应和状态码



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
@__app.route('/receive-image', methods=['GET'])
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
            print(image_data)
            image_url = "./gui/static/source/img/picture.jpg"  # 设置图片保存路径

            with open(image_url, 'wb') as f:
                f.write(image_data)
            # 假设 image_base64 是包含 Base64 编码的字符串
            # image_data = base64.b64decode(image_base64)
            # print(image_data)
            # txt_file_url = "C:/Users/11605/Desktop/base64_data.txt"  # 设置 txt 文件保存路径
            # with open(txt_file_url, 'w') as f:  # 将写入模式改为文本写入模式
            #     f.write(image_data.decode('utf-8'))  # 将二进制数据写入到 txt 文件中
                # 返回图片文件的URL给前端
                # return jsonify({"status": "success", "image_url": "/static/picture.jpg"})
            # image_url = f'http://127.0.0.1:5000/{image_path}'  # 设置图片文件在服务器上的访问URL
            # return jsonify({"status": "success", "image_data": "图片接收成功"})

            return jsonify({"status": "success", "image_url": image_url})

        else:
            return jsonify({"status": "error", "message": "缺少图片数据"})

    except Exception as e:
        return jsonify({"status": "error", "message": "图片接收失败", "error": str(e)})


# 加载位置信息
@__app.route('/api/get-location', methods=['GET'])
def get_location():
    location_data = {
        # 'user_name': "张三",
        # 'user_gender': "男",
        "location": "卧室 ",
        "coordinate": "x: 0.531435847282 , y: 1.22645330429, z: 0.0,x: 0.0,y: 0.0,z: -0.0285912500452,w: 0.999591186646"
    }
    return jsonify({"text": location_data})


# 加载用药信息
@__app.route('/get-medcine', methods=['GET'])
def get_medcine():
    med_data = {
        'med_name': "头孢克肟颗粒",
        'med_spec': "50mg*6袋",
        'med_usage': "口服",
        'med_freq': "2次/天",
        'med_dosage': "50mg",
    }
    return jsonify({"text": med_data})


# 接收位置
@__app.route('/api/sent_pose', methods=['POST'])
def get_robot_data():
    data = request.get_json()  # 获取 POST 请求中的 JSON 数据
    print(data)
    response_data = {'message': 'Data received successfully'}
    return jsonify(response_data)



# 创建数据库表（如果还不存在）
# cursor.execute('''CREATE TABLE IF NOT EXISTS user_info (
#                   id INTEGER PRIMARY KEY AUTOINCREMENT,
#                   user_name TEXT NOT NULL,
#                   user_gender TEXT NOT NULL,
#                   user_age INTEGER NOT NULL,
#                   user_type TEXT NOT NULL
#                   )''')
# conn.commit()

@__app.route('/save-user-info', methods=['POST'])
def save_user_info():
    try:
        if request.method == 'POST':
            user_info = request.json  # 假设前端将数据以JSON格式发送
            print(user_info)
            user_name = user_info.get('user_name')
            user_gender = user_info.get('user_gender')
            user_age = user_info.get('user_age')
            user_type = user_info.get('user_type')

            # 设置SQLite数据库连接
            conn = sqlite3.connect('fay.db')
            print(conn)
            cursor = conn.cursor()
            print(cursor)

            # 插入数据到数据库
            cursor.execute('''INSERT INTO user_inform (user_name, user_gender, user_age, user_type)
                              VALUES (?, ?, ?, ?)''', (user_name, user_gender, user_age, user_type))
            conn.commit()
            cursor.close()
            conn.close()
            return 'User information saved successfully.'
    except sqlite3.Error as e:
        print(e)
        return 'An error occurred while saving user information.'
    except Exception as e:
        print(e)
        return 'An error occurred while saving user information.'

    return 'User information saved successfully.'


@__app.route('/save-medicine-info', methods=['POST'])
def save_medicine_info():
    try:
        if request.method == 'POST':
            med_info = request.json  # 假设前端将数据以JSON格式发送
            print(med_info)
            med_name = med_info.get('med_name')
            med_spec = med_info.get('med_spec')
            med_usage = med_info.get('med_usage')
            med_freq = med_info.get('med_freq')
            med_dosage = med_info.get('med_dosage')
            med_time = med_info.get('med_time')

            # 设置SQLite数据库连接
            conn = sqlite3.connect('fay.db')
            print(conn)
            cursor = conn.cursor()
            print(cursor)

            # 插入数据到数据库
            cursor.execute('''INSERT INTO med_inform (med_name, med_spec, med_usage, med_freq, med_dosage, med_time)
                              VALUES (?, ?, ?, ?, ?, ?)''', (med_name, med_spec, med_usage, med_freq, med_dosage, time))
            conn.commit()
            cursor.close()
            conn.close()
            return 'User information saved successfully.'
    except sqlite3.Error as e:
        print(e)
        return 'An error occurred while saving medicine information.'
    except Exception as e:
        print(e)
        return 'An error occurred while saving medicine information.'

    return 'User information saved successfully.'


@__app.route('/save-location-info', methods=['POST'])
def save_location_info():
    try:
        if request.method == 'POST':
            location_info = request.json  # 假设前端将数据以JSON格式发送
            print(location_info)
            location = location_info.get('location')
            coordinate = location_info.get('coordinate')

            # 设置SQLite数据库连接
            conn = sqlite3.connect('fay.db')
            print(conn)
            cursor = conn.cursor()
            print(cursor)

            # 插入数据到数据库
            cursor.execute('''INSERT INTO location_inform (location, coordinate)
                              VALUES (?, ?)''', (location, coordinate))
            conn.commit()
            cursor.close()
            conn.close()
            return 'User information saved successfully.'
    except sqlite3.Error as e:
        print(e)
        return 'An error occurred while saving location information.'
    except Exception as e:
        print(e)
        return 'An error occurred while saving location information.'

    return 'User information saved successfully.'


@__app.route('/save-sit-time', methods=['POST'])
def save_time_info():
    try:
        if request.method == 'POST':
            sit_time = request.json  # 假设前端将数据以JSON格式发送
            print(sit_time)
            sit_time = sit_time.get('time')

            # 设置SQLite数据库连接
            conn = sqlite3.connect('fay.db')
            print(conn)
            cursor = conn.cursor()
            print(cursor)

            # 插入数据到数据库
            cursor.execute('''INSERT INTO sedentary_info (timespan)
                              VALUES (?)''', (sit_time))
            conn.commit()
            cursor.close()
            conn.close()
            return 'User information saved successfully.'
    except sqlite3.Error as e:
        print(e)
        return 'An error occurred while saving sittime information.'
    except Exception as e:
        print(e)
        return 'An error occurred while saving sittime information.'

    return 'User information saved successfully.'


@__app.route('/api/control-eyes', methods=['post'])
def control_eyes():
    eyes = yolov8.new_instance()
    if(not eyes.get_status()):
       eyes.start()
       util.log(1, "YOLO v8正在启动...")
    else:
       eyes.stop()
       util.log(1, "YOLO v8正在关闭...")
    return '{"result":"successful"}'


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
    # data = request.values.get('data')
    # info = json.loads(data)
    # text = fay_core.send_for_answer(info['msg'],info['sendto'])
    data = request.json
    # info = json.loads(data)
    text = fay_core.send_for_answer(data['msg'], data['sendto'])
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

@__app.route('/behavior/detection', methods=['post'])
def behavior_detection():
    # conn = sqlite3.connect('fay.db')
    # conn.execute('PRAGMA busy_timeout = 5000')
    try:
        # 图像识别
        request_data = request.json
        image = request_data.get("image")
        result = image_behavior.behavior_detection(image)

        #结果写死 站着、坐着的概率


        # 根据图像识别结果判断是否有坐
        result = "有个老人正在坐着"

        if "坐" in result:
            # 获取最新的久坐数据
            contentdb = Content_Db()
            row = contentdb.get_sit()
            # 更新数据库
            if row:
                id, timespan, date_time = row
                new_timespan = timespan + 10
                new_date_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                contentdb.add_sit(new_timespan,new_date_time,id+1)
                # if new_timespan >= 120:
                #     # 当前久坐时长到达2小时
                #     # 调用语音播报接口
                #     # 调用视频播放接口
                #     print("当前已经久坐2小时，跟我一起运动吧")
            else:
                print("表中没有数据")

            # 更新前端数据

            # 判断是否达到两小时
        else:
            print("字符串中不包含坐着")

        # <Response [200]>
        return jsonify({'result': result})

    except sqlite3.Error as e:
        print(e)
        return jsonify({'error': '请求处理出错：' + str(e)}), 500
    except Exception as e:
        return jsonify({'error': '请求处理出错：' + str(e)}), 500
    # finally:
    #     # 关闭连接
    #     if conn:
    #         print("数据库关闭")
    #         conn.close()

def run():
    server = pywsgi.WSGIServer(('0.0.0.0',5000), __app)
    server.serve_forever()


def start():
    MyThread(target=run).start()

if __name__ == '__main__':
    __app.run()