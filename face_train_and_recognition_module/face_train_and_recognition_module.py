from flask import Flask, request, jsonify
import os
import base64
import cv2
from PIL import Image
import numpy as np



app = Flask(__name__)


warningtime = 0

# 人脸识别
def face_recognition(image_data):
    # 获取当前路径basedir
    basedir = os.path.abspath(os.path.dirname(__file__))

    recognizer = cv2.face.LBPHFaceRecognizer_create()
    recognizer.read(basedir + '/../face_train_and_recognition/trainer/trainer.yml')

    # 把目录下的图片名字存入到一个数组中
    names = []
    path = basedir + '/../face_train_and_recognition/data/jm'
    imagePaths = [os.path.join(path, f) for f in os.listdir(path)]
    for imagePath in imagePaths:
        name = str(os.path.split(imagePath)[1].split('.', 2)[1])
        names.append(name)

    # 将 base64 编码的图片数据解码为图像
    image_data = base64.b64decode(image_data)
    nparr = np.frombuffer(image_data, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    # 人脸检测函数
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    face_detect = cv2.CascadeClassifier(basedir + '/../face_train_and_recognition/haarcascade_frontalface_alt2.xml')

    face = face_detect.detectMultiScale(gray,1.01,5,0,(100,100),(300,300))

    # 绘制人脸矩形框
    for x, y, w, h in face:
        cv2.rectangle(img, (x, y), (x + w, y + h), color=(0, 0, 255), thickness=2)

        # 人脸识别
        ids, confidence = recognizer.predict(gray[y:y + h, x:x + w])
        if confidence > 70:
            name = 'null'
            ids = 0
            cv2.putText(img, 'unkonw', (x + 10, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 255, 0), 1)
        else:
            name = str(names[ids - 1])
            cv2.putText(img, name, (x + 10, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 255, 0), 1)
    return img,name,ids


# def name():
#     path = '../face_train_and_recognition/data/jm'
#     imagePaths=[os.path.join(path,f) for f in os.listdir(path)]
#     for imagePath in imagePaths:
#        name = str(os.path.split(imagePath)[1].split('.',2)[1])
#        names.append(name)


def getImageAndLabels(path):
    # 获取当前路径basedir
    basedir = os.path.abspath(os.path.dirname(__file__))

    facesSamples=[]
    ids=[]
    imagePaths=[os.path.join(path,f) for f in os.listdir(path)]
    #检测人脸
    face_detector = cv2.CascadeClassifier(basedir +'/../face_train_and_recognition/haarcascade_frontalface_alt2.xml')
    #打印数组imagePaths
    print('数据排列：',imagePaths)
    #遍历列表中的图片
    for imagePath in imagePaths:
        #打开图片,黑白化
        PIL_img=Image.open(imagePath).convert('L')
        #将图像转换为数组，以黑白深浅
        # PIL_img = cv2.resize(PIL_img, dsize=(400, 400))
        img_numpy=np.array(PIL_img,'uint8')
        #获取图片人脸特征
        faces = face_detector.detectMultiScale(img_numpy)
        #获取每张图片的id和姓名
        id = int(os.path.split(imagePath)[1].split('.')[0])
        #预防无面容照片
        for x,y,w,h in faces:
            ids.append(id)
            facesSamples.append(img_numpy[y:y+h,x:x+w])
        #打印脸部特征和id
        #print('fs:', facesSamples)
        print('id:', id)
        #print('fs:', facesSamples[id])
    print('fs:', facesSamples)
    #print('脸部例子：',facesSamples[0])
    #print('身份信息：',ids[0])
    return facesSamples,ids


# 保存base64图片数据为文件
def save_base64_image(image_data, save_path):
    with open(save_path, 'wb') as image_file:
        image_file.write(base64.b64decode(image_data))

# 传入要保存的路径。返回传入文件夹路径下所有的文件个数+1
def get_next_number(save_folder):
    # 获取当前目录中 jpg 图片的个数
    jpg_files = [f for f in os.listdir(save_folder) if f.endswith('.jpg')]
    count = len(jpg_files)

    # 返回新的文件名
    return count + 1
