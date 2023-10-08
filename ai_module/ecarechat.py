import requests
import time
import json
import re
# rostopic命令抽取，这个方案已经被替代
def extract_rostopic_command(response):
    pattern = r"rostopic pub .*"
    match = re.search(pattern, response)
    if match:
        command = match.group()
        return command
    else:
        return None

# 从返回的回答中抽取功能代码
def extract_numbers(text):
    pattern = r'\d+'  # 匹配一个或多个数字
    numbers = re.findall(pattern, text)  # 在文本中找到匹配的所有数字
    return numbers


chat_history = [
]
count = 0
def question(cont, prompt=None):
    global count
    global ros_client
    try:


        url = "https://Sdia-LLM-KG-qm1yr71e2p69.serv-c1.openbayes.net"
        payload = {
            "prompt": cont,
            "history": chat_history
        }
        completion = requests.post(url, json=payload)
        count = 0
        data = json.loads(completion.text)
        # 获取history字段的值
        history = data['history'][0]
        # 获取response字段的值
        response_text = data['response']

        chat_history.append(history)
        return response_text
    except Exception as e:
        count += 1
        if count < 3:
            time.sleep(15)
            return question(cont)
        return 'ecarebot语音交互当前繁忙，请稍后重试'


# 机器人意图解析
def control(cont, prompt=None):
    global count
    global ros_client
    try:

        url = "https://Sdia-LLM-KG-qm1yr71e2p69.serv-c1.openbayes.net"
        payload = {
            "prompt": cont,
            "history": [
                [
                    "假设你是我的机器人助手，有以下功能。1：心率检测；2：聊天陪伴；3：一起运动；4：视觉跟随；5：聊天结束；6：添加成员；10：处方识别。根据意图或者场景，告诉我最合适的序号。",
                    "好的，我明白了，请表达您的意图给我！"
                ]
            ]
        }
        completion = requests.post(url, json=payload)
        count = 0
        data = json.loads(completion.text)
        # 获取response字段的值
        response_text = data['response']
        print(response_text)
        command = extract_numbers(response_text)
        # print(command[0])
        if command:
            return command[0]
        else:
            return "对不起，我没有理解您的意图！"
    except Exception as e:
        # count += 1
        # if count < 3:
        #     time.sleep(15)
        #     return control(cont)
        return 'ecarebot语音交互当前繁忙，请稍后重试'
# if __name__ == "__main__":
#     print(control('来了一位新朋友'))