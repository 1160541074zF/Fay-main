import base64
import json
import requests

def image_to_base64(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode('utf-8')

# 指定要发送的图片
image_path = r"C:/Users/11605/Desktop/test.jpg"
image_base64 = image_to_base64(image_path)
print(image_base64)
# 请求的 URL
url = "http://192.168.3.18:5000/receive-image"

# 创建请求的 JSON 数据
data = {
    "image_base64": image_base64
}

# 发出 POST 请求
headers = {'Content-Type': 'application/json'}
response = requests.post(url, json=data, headers=headers)

# 输出响应的 JSON 数据
print(response.json())

print(response.text)