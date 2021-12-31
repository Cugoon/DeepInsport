import tensorflow as tf
from keras.models import load_model
from PIL import Image, ImageOps
import numpy as np
import cv2

# 모델 위치
import Openpose,os

model = load_model('.\Models\keras_model.h5')
filePath = r"D:\test\DeepInSpr\Video\TigerWoods\Front\TigerWoods_Front.mp4"
player = os.path.basename(filePath)
player = player[:-4]
# 카메라를 제어할 수 있는 객체
capture = cv2.VideoCapture(0)
cap = cv2.VideoCapture(filePath)

# 카메라 길이 너비 조절
capture.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)

cap.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)

prediction = {0: 'address', 1: 'take back', 2: 'back swing', 3: 'top swing', 4: 'down swing', 5: 'impact',
              6: 'follow through', 7: 'finish'}


# 이미지 처리하기
def preprocessing(frame):
    # frame_fliped = cv2.flip(frame, 1)
    # 사이즈 조정 티쳐블 머신에서 사용한 이미지 사이즈로 변경.
    size = (224, 224)
    frame_resized = cv2.resize(frame, size, interpolation=cv2.INTER_AREA)

    # 이미지 정규화
    # astype : 속성
    frame_normalized = (frame_resized.astype(np.float32) / 127.0) - 1

    # 이미지 차원 재조정 - 예측을 위해 reshape 해줍니다.
    # keras 모델에 공급할 올바른 모양의 배열 생성
    frame_reshaped = frame_normalized.reshape((1, 224, 224, 3))
    # print(frame_reshaped)

    return frame_reshaped

def maxScore(data) :
    result = data[0]
    for item in data :
        if item > result :
            result = item

    return result

def find_index(num,data):
    index = []
    for i in range(len(data)) :
        if data[i] == num:
            index.append(i)

    return index



# 예측용 함수
def predict(frame):
    prediction = model.predict(frame)
    prediction = find_index(maxScore(prediction[0]), prediction[0])
    return prediction[0]


def imageTextInput(text):
    cv2.putText(frame, 'process: ' + text, (0, 80), cv2.FONT_HERSHEY_PLAIN, 5, (0, 0, 255), 2)



# prediction = {0: 'address', 1: 'take back',
#               2: 'back swing', 3: 'top swing',
#               4: 'down swing', 5: 'impact',
#               6: 'follow through', 7: 'finish'}

while True:
    ret, frame = cap.read()

    if cv2.waitKey(100) > 0:
        break

    preprocessed = preprocessing(frame)
    prediction = predict(preprocessed)
    cv2.putText(frame, player, (0, 150), cv2.FONT_HERSHEY_PLAIN, 5, (0, 0, 255), 2)

    if prediction == 0 :
        imageTextInput('address')

    elif prediction == 1 :
        imageTextInput('take back')
        #cv2.imshow("VideoFrame", frame)

    elif prediction == 2 :
        imageTextInput('back swing')
        #cv2.imshow("VideoFrame", frame)

    elif prediction == 3 :
        imageTextInput('top swing')
        #cv2.imshow("VideoFrame", frame)

    elif prediction == 4 :
        imageTextInput('down swing')
        #cv2.imshow("VideoFrame", frame)

    elif prediction == 5 :
        imageTextInput('impact')
        #cv2.imshow("VideoFrame", frame)

    elif prediction == 6 :
        imageTextInput('follow through')
        #cv2.imshow("VideoFrame", frame)

    elif prediction == 7 :
        imageTextInput('finish')
        #cv2.imshow("VideoFrame", frame)

    cv2.imshow("VideoFrame", frame)

# ret, frame = cap.read()
    #
    # if cv2.waitKey(100) > 0:
    #     break
    #
    # preprocessed = preprocessing(frame)
    # prediction = predict(preprocessed)
    #
    # if prediction[0, 0]:
    #     print('0')
    #     cv2.putText(frame, '0', (0, 25), cv2.FONT_HERSHEY_PLAIN, 3, (255, 255, 255), 2)
    #
    # elif prediction[0, 1]:
    #     print('1')
    #     cv2.putText(frame, '1', (0, 25), cv2.FONT_HERSHEY_PLAIN, 3, (255, 255, 255), 2)
    #
    # elif prediction[0, 2]:
    #     cv2.putText(frame, '2', (0, 25), cv2.FONT_HERSHEY_PLAIN, 3, (255, 255, 255), 2)
    #     print('1')
    #
    # elif prediction[0, 3]:
    #     cv2.putText(frame, '3', (0, 25), cv2.FONT_HERSHEY_PLAIN, 3, (255, 255, 255), 2)
    #     print('2')
    #
    # elif prediction[0, 4]:
    #     cv2.putText(frame, '4', (0, 25), cv2.FONT_HERSHEY_PLAIN, 3, (255, 255, 255), 2)
    #     print('3')
    #
    # elif prediction[0, 5]:
    #     cv2.putText(frame, '4', (0, 25), cv2.FONT_HERSHEY_PLAIN, 3, (255, 255, 255), 2)
    #     print('3')
    #
    # else:
    #     print('else')
    #
    # cv2.imshow("VideoFrame", frame)
    #
    # print(prediction)
    #
