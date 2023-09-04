import base64
import json
import requests

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
        result_data = json.loads(response)
        describe = result_data['result']
        util.log(1, describe)
        # 调用语音播报接口
        url = "http://192.168.3.48:5000/robot/send_msg"
        payload = json.dumps({
            "kafka_ip": "192.168.3.48:9092",
            "topic_name": "reminder",
            "message": {
                "type": "voice",
                "content": describe
            }
        })
        headers = {
            'Content-Type': 'application/json'
        }
        response = requests.request("POST", url, headers=headers, data=payload)
        return response.text
    except Exception as e:
        return '情绪识别请求失败，请稍后重试' + str(e)
#
#示例调用
if __name__ == "__main__":
    image_path = "G:\情绪.png"
    image_base64 = image_to_base64(image_path)
    print(image_base64)
    result = emotion_detection(image_base64)
    print(result)

