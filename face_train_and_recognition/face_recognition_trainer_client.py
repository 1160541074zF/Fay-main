import requests
import base64

# 人脸训练保存测试
def send_image_to_api(image_path, image_name):
    # 读取图片并转换为 base64 编码
    with open(image_path, 'rb') as image_file:
        base64_image = base64.b64encode(image_file.read()).decode('utf-8')

    # 构建请求数据，包括图片数据和图片名字
    data = {'image_data': base64_image, 'filename': image_name}

    # 发送 POST 请求到 Flask API
    api_url = 'http://127.0.0.1:5000/save_image_and_train'  # 修改为你实际部署的 API 地址
    response = requests.post(api_url, json=data)

    # 解析响应结果
    result = response.json()
    print(result['message'])


if __name__ == '__main__':
    image_path = '2.lena.jpg'
    image_name = 'lena'  # 设置图片名字（除去文件后缀 .jpg）
    send_image_to_api(image_path, image_name)
