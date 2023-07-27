import requests
import json
import base64


def send_picture():
    url = "http://192.168.3.48:5000/receive-image"
    image_path = "C:/Users/11605/Desktop/test.jpg"
    data = image_to_base64(image_path)
    payload = json.dumps({
        "image_base64": image_to_base64(image_path)
    }
    )
    headers = {
        'Content-Type': 'application/json'
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    print(response.text)


def image_to_base64(image_path):
    with open(image_path, "rb") as img_file:
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode('utf-8')


if __name__=='__main__':
    send_picture()