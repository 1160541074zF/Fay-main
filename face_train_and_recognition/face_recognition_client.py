import cv2
import requests
import base64
import os

# 人脸识别测试
def detect_face_with_api(image_path):
    # 提取图片文件名（不包含扩展名）
    file_name = os.path.splitext(os.path.basename(image_path))[0]

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
    result_name = result['result_name']

    # # 将 base64 编码的图片转换为图像并保存，使用原始图片名字加上识别结果作为保存文件名
    # result_image_base64 = result['result_image']
    # result_image_data = base64.b64decode(result_image_base64)
    # result_image_path = f'result_{result_name}.jpg'
    # with open(result_image_path, 'wb') as result_image_file:
    #     result_image_file.write(result_image_data)

    return result_name

if __name__ == '__main__':
    image_path = '2.lena.jpg'
    result_name = detect_face_with_api(image_path)
    print(result_name)
