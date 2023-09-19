import base64
import json
import requests

def image_to_base64(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode('utf-8')

def danger_detection(image_base64):
    try:
        url = "https://Sdia-LLM-KG-yu74wtz23f8m.serv-c1.openbayes.net"
        data = {
            "image": image_base64,
            "text": "假设你是机器人，请根据当前画面发现的危险，生成一条预警信息",
            "history": []
        }
        completion = requests.post(url, json=data)
        response = completion.content.decode()
        return response
    except Exception as e:
        return '危险识别请求失败，请稍后重试' + str(e)
#
#示例调用
if __name__ == "__main__":
    image_path = "G:\火灾.jpg"
    image_base64 = image_to_base64(image_path)
    result = danger_detection(image_base64)
    print(result)

