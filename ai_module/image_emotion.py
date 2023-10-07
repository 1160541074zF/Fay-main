import base64
import json
import requests
import re
from utils import util


def image_to_base64(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode('utf-8')

def emotion_detection(image_base64):
    try:
        url = "https://Sdia-LLM-KG-yu74wtz23f8m.serv-c1.openbayes.net"
        data = {
            "image": image_base64,
            "text": "假设你是助老服务机器人的眼睛，请根据图片告诉我老人的情绪，生成一段问候语",
            "history": []
        }
        completion = requests.post(url, json=data)
        response = completion.content.decode()
        return response
        # ==========9.5 服务器部署调试
        # result_data = json.loads(response)
        # describe = result_data['result']
        # util.log(1, describe)
        # # 调用语音播报接口
        # url = "http://192.168.3.48:5000/robot/send_msg"
        # payload = json.dumps({
        #     "kafka_ip": "192.168.3.48:9092",
        #     "topic_name": "reminder",
        #     "message": {
        #         "type": "voice",
        #         "content": describe
        #     }
        # })
        # headers = {
        #     'Content-Type': 'application/json'
        # }
        # response = requests.request("POST", url, headers=headers, data=payload)
        # print(response)
        # return response.text
        # =============
        # result_data = {
        #     #"result": "您好，您看起来很开心，祝您拥有美好的一天"
        #     "result": "您看起来很高兴。您的微笑和自信的表情表明您在享受当前的一天。作为助老服务机器人，我感谢您的快乐和支持，希望您能继续享受生活中的美好时光。"
        # }
        # return json.dumps(result_data)
    except Exception as e:
        return '情绪识别请求失败，请稍后重试' + str(e)

def extract_chinese_quotes(text):
    # 使用正则表达式匹配中文双引号括起来的文本
    pattern = r'“([^“”]+)”'
    matches = re.findall(pattern, text)

    # 返回匹配的文本列表
    return matches




#示例调用
if __name__ == "__main__":
    image_path = "G:\图像大模型测试照片\情绪识别.jpg"
    image_base64 = image_to_base64(image_path)
    print(image_base64)
    result = emotion_detection(image_base64)
    print(result)

    text = "你好！你看起来非常愉悦，因为你正在享受美味的食物、“与朋友交谈”或者参加有趣的活动。祝你度过愉快的一天！"
    chinese_quotes = extract_chinese_quotes(text)
    for quote in chinese_quotes:
        print(quote)

