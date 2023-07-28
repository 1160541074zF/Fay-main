import requests
import time
import json
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

# if __name__ == "__main__":
#     print(ask("nihao"))