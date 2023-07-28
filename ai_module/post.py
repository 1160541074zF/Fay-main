import base64
import json
import requests
from datetime import datetime, timedelta

def image_to_base64(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode('utf-8')

# 指定要发送的图片
image_path = "G:\老人站立.jpg" #换成你自己的图片
image_base64 = image_to_base64(image_path)

# 请求的 URL
url = "http://127.0.0.1:5000/posture/recognition"

# 拍照时间
time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
print(time)

# 创建请求的 JSON 数据
data = {
    "image": image_base64,
    "time":time
}

# 发出 POST 请求
response = requests.post(url, json=data)
# response = requests.post(url, json=data).text
# 输出响应的 JSON 数据
# print(response.json())
print(response.text)
