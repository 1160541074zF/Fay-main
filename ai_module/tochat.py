import requests
import time
chat_history = [
]
count = 0
def question(cont, prompt=None):
    global count
    global ros_client
    try:
        if prompt != None:
            chat_history.append(
                {
                    "role": "user",
                    "content": prompt,
                }
            )

        chat_history.append(
            {
                "role": "user",
                "content": cont,
            }
        )

        url = "https://tochat.gwzone.cn/api"
        payload = {
            "messages": chat_history,
            "temperature": 0.6,
            "password": "801",
            "model": "gpt-3.5-turbo"
        }
        completion = requests.post(url, json=payload)
        response = completion.content.decode()
        count = 0
        return response
    except Exception as e:
        count += 1
        if count < 3:
            time.sleep(15)
            return question(cont)
        return 'tochat语音交互当前繁忙，请稍后重试' + e

# if __name__ == "__main__":
#     print(ask("nihao"))