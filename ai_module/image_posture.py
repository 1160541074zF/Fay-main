import base64
import json
import requests

def image_to_base64(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode('utf-8')

# 图像识别大模型分析人体姿态
def posture_recognition(image_base64):
    try:
        url = "https://Sdia-LLM-KG-yu74wtz23f8m.serv-c1.openbayes.net"
        data = {
            "image": image_base64,
            # "text": "帮我描述一下图片中的老人是坐、躺、站、跌倒哪种姿态",
            "text": "请根据图片分析老人的人体姿态，包括躺、坐、立、跌倒，并提供关于姿态的描述",
            "history": []
        }
        completion = requests.post(url, json=data)
        response = completion.content.decode()
        # result history status time
        # response = 'no healthy upstream'
        return response
    except Exception as e:
        return '行为识别请求失败，请稍后重试'

# 根据图像识别大模型结果获取老人姿态
# prompt测试使用
def result_analysis(response):
    result_data = json.loads(response)
    result_describe = result_data['result']
    # print(result_describe)
    posture = ""
    if '倒' in result_describe:
        posture = 1
    elif '躺' in result_describe:
        posture =4
    elif '坐' in result_describe:
        posture = 2
    elif '站' in result_describe or '立' in result_describe:
        posture = 3
    return posture

#示例调用
if __name__ == "__main__":
    image_path = "G:\老人坐着.jpg"
    image_base64 = image_to_base64(image_path)
    # 图像识别大模型结果
    response = posture_recognition(image_base64)
    # 老人姿态
    posture = result_analysis(response)
    print(response)
    print(posture)
