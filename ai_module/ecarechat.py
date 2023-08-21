import requests
import time
import json
import re
# rostopic命令抽取
def extract_rostopic_command(response):
    pattern = r"rostopic pub .*"
    match = re.search(pattern, response)
    if match:
        command = match.group()
        return command
    else:
        return None


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
                    "假设你是一个ROS操作系统的机器人，需要你帮我生成可执行的shell命令，无论我问什么你都必须严格按照我的意图匹配生成对应的rostopic命令，以下是你需要掌握的意图和rostopic命令对应关系如下：\n\n| 意图     | topic          | datatype | args |\n| -------- | -------------- | -------- | ---- |\n| 测心率   | /voice/control | Int32    | 1    |\n| 聊天     | /voice/control | Int32    | 2    |\n| 添加成员 | /voice/control | Int32    | 3    |。我需要你根据我的意图参照以上表格返回可执行的命令，比如我的意图是聊天，你返回\"rostopic pub /voice/control Int32 2\"",
                    "好的，我明白了，请表达您的意图给我！"
                ]
            ]
        }
        completion = requests.post(url, json=payload)
        count = 0
        data = json.loads(completion.text)
        # 获取response字段的值
        response_text = data['response']
        # print(response_text)
        command = extract_rostopic_command(response_text)
        if command:
            return command
        else:
            return "未找到rostopic命令"
    except Exception as e:
        # count += 1
        # if count < 3:
        #     time.sleep(15)
        #     return control(cont)
        return 'ecarebot语音交互当前繁忙，请稍后重试'
if __name__ == "__main__":
    print(control('我想测心率'))