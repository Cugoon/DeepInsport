# 모델 위치
import os
import sys
from sys import platform

import cv2
import numpy as np
import tensorflow as tf
from keras.models import load_model

import data_preprocessing
from data_preprocessing import prediction, preprocess
from data_preprocessing import *
#import data_preprocessing *

import matplotlib as plt

dir_path = r"D:\openpose\build"
predictor = prediction("SVM.sav")
scores = []
#os.environ["CUDA_VISIBLE_DIVICES"] = "0, 1"

try:
    # Windows Import
    if platform == "win32":
        # Change these variables to point to the correct folder (Release/x64 etc.)
        sys.path.append(r"D:\openpose\build\python\openpose\Release");
        os.environ['PATH'] = os.environ[
                                 'PATH'] + ';' + "D:\\openpose\\build\\x64\\Release;" + 'D:\\openpose\\build\\bin;'
        import pyopenpose as op
    else:
        # Change these variables to point to the correct folder (Release/x64 etc.)
        sys.path.append('D:\\Anaconda3\\python');
        # If you run `make install` (default path is `/usr/local/python` for Ubuntu), you can also access the OpenPose/python module from there. This will install OpenPose and the python library at your desired installation path. Ensure that this is in your python path in order to use it.
        # sys.path.append('/usr/local/python')
        from openpose import pyopenpose as op
except ImportError as e:
    print(
        'Error: OpenPose library could not be found. Did you enable `BUILD_PYTHON` in CMake and have this Python script in the right folder?')
    raise e

params = dict()
params["model_folder"] = r"D:\openpose\models"
params['disable_blending'] = False

params["process_real_time"] = True
params["video"] = "1.JENNIE_SOLO.mp4"
params["camera"] = 0
params["process_real_time"] = True

#openpose

class Opnenpose(object):
    def __init__(self):
        # Starting OpenPose
        self.opWrapper = op.WrapperPython()
        self.opWrapper.configure(params)
        self.opWrapper.start()
        self.cont = 0

    def out_frame(self, frame):
        self.datum = op.Datum()
        self.datum.cvInputData = frame
        self.opWrapper.emplaceAndPop(op.VectorDatum([self.datum]))
#openposeend

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
def predict(frame, model):
    prediction = model.predict(frame)
    prediction = find_index(maxScore(prediction[0]), prediction[0])
    return prediction[0]
    print(prediction)

"""def predict2(frame,model):
    prediction = model.predict(frame)
    prediction = find_index(maxScore(prediction[0]), prediction[0])

    return prediction[0]
    print(prediction)"""

def imageTextInput(frame,text):
    frame = cv2.putText(frame, 'process: ' + text, (0, 80), cv2.FONT_HERSHEY_PLAIN, 5, (0, 0, 255), 2)
    return frame


def openposesocre(frame, frame2):
    #prediction = data_preprocessing.prediction("SVM.sav")
    #frame =

    try:
        if len(frame.datum.poseKeypoints) <= 1:
            keypoin_frame1 = frame.datum.poseKeypoints
        else:
            keypoin_frame1 = frame.datum.poseKeypoints

        if len(frame2.datum.poseKeypoints) <= 1:
            keypoin_frame2 = frame2.datum.poseKeypoints
        else:
            keypoin_frame2 = frame2.datum.poseKeypoints[0]

        score = prediction.score(np.array(keypoin_frame1), np.array(keypoin_frame2))
        score = (round(score[0][1] * 100))

        print("Score: " + score)

    except:
        score = 0


def swingclass(frame):
    if prediction == 0:
        frame = imageTextInput(frame, 'address')

    elif prediction == 1:
        frame = imageTextInput(frame, 'take back')
        # cv2.imshow("VideoFrame", frame)

    elif prediction == 2:
        frame = imageTextInput(frame, 'back swing')
        #cv2.imshow("VideoFrame", frame)

    elif prediction == 3:
        frame = imageTextInput(frame, 'top swing')
        #cv2.imshow("VideoFrame", frame)

    elif prediction == 4:
        frame = imageTextInput(frame, 'down swing')
        #cv2.imshow("VideoFrame", frame)

    elif prediction == 5:
        frame = imageTextInput(frame, 'impact')
        #cv2.imshow("VideoFrame", frame)

    elif prediction == 6:
        frame = imageTextInput(frame, 'follow through')
        #cv2.imshow("VideoFrame", frame)

    elif prediction == 7:
        frame = imageTextInput(frame,'finish')
        #cv2.imshow("VideoFrame", frame)

        #print("Frame 1: " + frame.prediction)
        #print("Frame 2: " + frame2.prediction)


if __name__ == "__main__" :

    # Tensorflow GPU 사용량 관리
    gpus = tf.config.experimental.list_physical_devices('GPU')
    if gpus:
        try:
            # Currently, memory growth needs to be the same across GPUs
            for gpu in gpus:
                tf.config.experimental.set_memory_growth(gpu, True)
            logical_gpus = tf.config.experimental.list_logical_devices('GPU')
            print(len(gpus), "Physical GPUs,", len(logical_gpus), "Logical GPUs")
        except RuntimeError as e:
            # Memory growth must be set before GPUs have been initialized
            print(e)

    OP = Opnenpose()

    model = load_model('.\Models\keras_model.h5')
    predictor = prediction("SVM.sav")

    filePath = r"D:\test\DeepInSpr\Video\TigerWoods\Front\TigerWoods_Front.mp4"
    filePath2 = r"D:\test\DeepInSpr\Video\CollinMorikawa\Front\CollinMorikawa_Front.mp4"
    #filePath2 = r"D:\test\DeepInSpr\Video\LeeHanSol\Side\LeeHanSol_Side.mp4"

    player = os.path.basename(filePath)
    player = player[:-4]
    angle = player[-5:]

    player2 = os.path.basename(filePath2)
    player2 = player2[:-4]
    angle2 = player2[-5:]

    # 카메라를 제어할 수 있는 객체
    capture = cv2.VideoCapture(0)
    cap = cv2.VideoCapture(filePath)
    cap2 = cv2.VideoCapture(filePath2)

    # cap = Openpose.datum.cvOutputData

    ret_frame, frame_frame = cap.read()
    ret_frame2, frame_frame2 = cap2.read()

    # 카메라 길이 너비 조절
    capture.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
    capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)

    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)

    cap2.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
    cap2.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)

"""    predictions = {0: 'address', 1: 'take back', 2: 'back swing', 3: 'top swing', 4: 'down swing', 5: 'impact',
                  6: 'follow through', 7: 'finish'}"""

while cap.isOpened() and cap2.isOpened():
    ret, frame = cap.read()
    ret2, frame2 = cap2.read()

    if cv2.waitKey(100) > 0:
        break

    cv2.putText(frame, "Player: " + player, (0, 150), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), 2)
    cv2.putText(frame, "Angle: " + angle, (0, 200), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), 2)
    cv2.putText(frame2, "Player: " + player2, (0, 150), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), 2)
    cv2.putText(frame2, "Angle: " + angle2, (0, 200), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), 2)

    preprocessed = preprocessing(frame)  # 영상 프레임을 전치러
    prediction = predict(preprocessed, model)  # 전처리한 프레임을 예측
    swingclass(frame)  # 스윙 프로세스
    OP.out_frame(frame)  # OpenPose
    cv2.imshow("Player", OP.datum.cvOutputData)

    preprocessed2 = preprocessing(frame2)  # 영상 프레임을 전치러
    prediction2 = predict(preprocessed2, model)  # 전처리한 프레임을 예측
    swingclass(frame2)  # 스윙 프로세스
    OP.out_frame(frame2)  # OpenPose
    cv2.imshow("Player2", OP.datum.cvOutputData)

    openposesocre(frame, frame2)


    """if prediction == 0 :
        frame = imageTextInput(frame,'address')
        frame2 = imageTextInput(frame2, 'address')

    elif prediction == 1 :
        frame = imageTextInput(frame,'take back')
        frame2 = imageTextInput(frame2,'take back')

        # cv2.imshow("VideoFrame", frame)

    elif prediction == 2 :
        frame = imageTextInput(frame,'back swing')
        frame2 = imageTextInput(frame2,'back swing')

        #cv2.imshow("VideoFrame", frame)

    elif prediction == 3 :
        frame = imageTextInput(frame,'top swing')
        frame2 = imageTextInput(frame2,'top swing')
        #cv2.imshow("VideoFrame", frame)

    elif prediction == 4 :
        frame = imageTextInput(frame,'down swing')
        frame2 = imageTextInput(frame2,'down swing')
        #cv2.imshow("VideoFrame", frame)

    elif prediction == 5 :
        frame = imageTextInput(frame,'impact')
        frame2 = imageTextInput(frame2,'impact')
        #cv2.imshow("VideoFrame", frame)

    elif prediction == 6 :
        frame = imageTextInput(frame,'follow through')
        frame2 = imageTextInput(frame,'follow through')

        #cv2.imshow("VideoFrame", frame)

    elif prediction == 7 :
        frame = imageTextInput(frame,'finish')
        frame2 = imageTextInput(frame,'finish')

        #cv2.imshow("VideoFrame", frame)"""

"""
    OP.out_frame(frame)
    cv2.imshow("Player1", OP.datum.cvOutputData)
    
    OP.out_frame(frame2)
    cv2.imshow("Player2", OP.datum.cvOutputData)"""

"""while True:
    ret, frame = cap.read()
    ret2, frame2 = cap2.read()

    if cv2.waitKey(100) > 0:
        break

    preprocessed = preprocessing(frame)
    prediction = predict(preprocessed,model)

    preprocessed2 = preprocessing(frame2)
    prediction2 = predict2(preprocessed2, model)


    cv2.putText(frame, "Player: " + player, (0, 150), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), 2)
    cv2.putText(frame, "Angle: " + angle, (0, 200), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), 2)

    cv2.putText(frame2, "Player: " + player2, (0, 150), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), 2)
    cv2.putText(frame2, "Angle: " + angle2, (0, 200), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), 2)

    if prediction == 0 :
        frame = imageTextInput(frame,'address')
        frame2 = imageTextInput(frame2, 'address')

    elif prediction == 1 :
        frame = imageTextInput(frame,'take back')
        frame2 = imageTextInput(frame2,'take back')

        # cv2.imshow("VideoFrame", frame)

    elif prediction == 2 :
        frame = imageTextInput(frame,'back swing')
        frame2 = imageTextInput(frame2,'back swing')

        #cv2.imshow("VideoFrame", frame)

    elif prediction == 3 :
        frame = imageTextInput(frame,'top swing')
        frame2 = imageTextInput(frame2,'top swing')
        #cv2.imshow("VideoFrame", frame)

    elif prediction == 4 :
        frame = imageTextInput(frame,'down swing')
        frame2 = imageTextInput(frame2,'down swing')
        #cv2.imshow("VideoFrame", frame)

    elif prediction == 5 :
        frame = imageTextInput(frame,'impact')
        frame2 = imageTextInput(frame2,'impact')
        #cv2.imshow("VideoFrame", frame)

    elif prediction == 6 :
        frame = imageTextInput(frame,'follow through')
        frame2 = imageTextInput(frame,'follow through')

        #cv2.imshow("VideoFrame", frame)

    elif prediction == 7 :
        frame = imageTextInput(frame,'finish')
        frame2 = imageTextInput(frame,'finish')

        #cv2.imshow("VideoFrame", frame)

    OP.out_frame(frame)
    cv2.imshow("Player1", OP.datum.cvOutputData)
    cv2.imshow("Player1_Origin", frame)


    OP.out_frame(frame2)
    cv2.imshow("Player2", OP.datum.cvOutputData)
    cv2.imshow("Player2_Origin", frame2)
"""