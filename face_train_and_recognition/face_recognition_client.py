import requests
import base64
import os

# 人脸识别测试
def detect_face_with_api(image_path):
    # 读取图片并转换为 base64 编码
    with open(image_path, 'rb') as image_file:
        base64_image = base64.b64encode(image_file.read()).decode('utf-8')

    # 构建请求数据
    data = {'image_data': base64_image}

    # 发送 POST 请求到 Flask API
    api_url = 'http://127.0.0.1:5000/recognition_face'  # 修改为你实际部署的 API 地址
    response = requests.post(api_url, json=data)

    # 解析响应结果
    result = response.json()

    # 获取识别结果
    print(result['result_id'])
    print(result['result_name'])

if __name__ == '__main__':
    image_path = '1.james.jpg'
    detect_face_with_api(image_path)

