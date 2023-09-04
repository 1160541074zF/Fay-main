import base64
import json
import requests
# from datetime import datetime, timedelta


def image_to_base64(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode('utf-8')

def sendEmotionPicture():
    image_path = "./emotion.png" #换成你自己的图片
    image_base64 = image_to_base64(image_path)
    url = "http://localhost:5000/recognition/emotion"
    data = {
    "image": image_base64
    }
    response = requests.post(url, json=data)
    return response

if __name__ == '__main__':
    a = sendEmotionPicture()
    print(a)
    # url = "http://192.168.3.48:5000/robot/send_msg"
    # payload = json.dumps({
    #     "kafka_ip": "192.168.3.48:9092",
    #     "topic_name": "reminder",
    #     "message": {
    #         "type": "voice",
    #         "content": "你好"
    #     }
    # })
    # headers = {
    #     'Content-Type': 'application/json'
    # }
    # response = requests.request("POST", url, headers=headers, data=payload)