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
        # result_data = {
        #     # "result": "厨房着火了！火源位于炉灶上方的烤箱里。如果火灾没有及时发现并控制，将会导致火势扩大、蔓延至整个房间，甚至导致建筑物倒塌或人员伤亡.为了预防这种情况的发生，建议立即采取行动，关闭所有电源和燃气管道，并使用灭火器灭火。同时，及时联系消防部门进行救援处理。"
        #     # "result": "厨房有碎玻璃，请注意"
        #     # "result": "老人躺卧在沙发上"
        #     "result": "老人躺卧在沙发上"
        # }
        # return json.dumps(result_data)
    except Exception as e:
        return '危险识别请求失败，请稍后重试' + str(e)
#
#示例调用
if __name__ == "__main__":
    image_path = "G:\测试图片\火灾.jpg"
    image_base64 = image_to_base64(image_path)
    result = danger_detection(image_base64)
    print(result)

