import requests
import base64
import os
# 人脸训练保存测试
def get_next_filename(save_folder, image_name):
    # 获取当前目录中 jpg 图片的个数
    jpg_files = [f for f in os.listdir(save_folder) if f.endswith('.jpg')]
    count = len(jpg_files)

    # 返回新的文件名
    return f"{count + 1}.{image_name}.jpg"

def send_image_to_api(image_path, image_name):
    # 读取图片并转换为 base64 编码
    with open(image_path, 'rb') as image_file:
        base64_image = base64.b64encode(image_file.read()).decode('utf-8')

    # 获取图片的保存路径和文件名
    save_folder = './data/jm/'
    image_save_filename = get_next_filename(save_folder, image_name)

    # 构建请求数据，包括图片数据和图片名字
    data = {'image_data': base64_image, 'filename': image_save_filename}

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
