import base64
import json
import requests
import time

def image_to_base64(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode('utf-8')

def behavior_detection(image_base64):
    try:
        # image_base64 = image_to_base64(image_path)
        url = "https://Sdia-LLM-KG-r8jtwdr3r5r5.serv-c1.openbayes.net/api"
        data = {
            "image_path": image_base64,
            "text": "请你描述一下这张图片",
            #"text": "图片中的老人跌倒了吗",
            "history": []
        }
        completion = requests.post(url, json=data)
        response = completion.content.decode()
        if "no healthy upstream" in response:
            return '行为识别请求失败，请稍后重试'
        else:
            return response
    except Exception as e:
        return '行为识别请求失败，请稍后重试' + str(e)

#示例调用
# if __name__ == "__main__":
#     image_path = "G:\凝视.jpg"
#     image_base64 = image_to_base64(image_path)
#     result = behavior_detection(image_base64)
#     print(result)

