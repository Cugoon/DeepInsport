import tensorflow.keras
from keras.models import load_model
from PIL import Image, ImageOps
import numpy as np
import cv2

# class
# 0 address
# 1 takeback
# 2 backswing
# 3 top
# 4 down
# 5 impact
# 6 followthrough
# 7 finish

model = load_model('.\Models\keras_model.h5')


def preprocessing(frame):
    # frame_fliped = cv2.flip(frame, 1)
    # 사이즈 조정 티쳐블 머신에서 사용한 이미지 사이즈로 변경해준다.
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


def pro_action(frame):
    prediction = model.predict(frame)
    return prediction


while True:
    ret, frame = frame.read()

    if cv2.waitKey(100) > 0:
        break

    preprocessed = preprocessing(frame)
    prediction = pro_action(preprocessed)

    if prediction[0, 0] < prediction[0, 1]:
        print('hand off')
        cv2.putText(frame, 'hand off', (0, 25), cv2.FONT_HERSHEY_PLAIN, 1, (0, 0, 0))

    else:
        cv2.putText(frame, 'hand on', (0, 25), cv2.FONT_HERSHEY_PLAIN, 1, (0, 0, 0))
        print('hand on')


def pro_action(image):
    print("Golf Swing Process Classification")
    # Load the model
    # model = load_model('.\Models\keras_model.h5')

    # Create the array of the right shape to feed into the keras model
    # The 'length' or number of images you can put into the array is
    # determined by the first position in the shape tuple, in this case 1.
    data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)
    # Replace this with the path to your image
    # image = Image.open(r'D:\test\DeepInSpr\Collin.jpg')
    # image = img
    # resize the image to a 224x224 with the same strategy as in TM2:
    # resizing the image to be at least 224x224 and then cropping from the center
    size = (224, 224)
    image = ImageOps.fit(image, size, Image.ANTIALIAS)

    # turn the image into a numpy array
    image_array = np.asarray(image)
    # Normalize the image
    normalized_image_array = (image_array.astype(np.float32) / 127.0) - 1
    # Load the image into the array
    data[0] = normalized_image_array

    # run the inference
    prediction = model.predict(data)
    print(prediction)

    return prediction


def pro_action(frame):
    prediction = model.predict(frame)
    return prediction


if __name__ == '__main__':
    print('a')
    # img = Image.open(r'D:\test\DeepInSpr\Collin.jpg')
    cap = cv2.VideoCapture(r"D:\test\DeepInSpr\Video\TigerWoods\Front\TigerWoods_Front.mp4")
    # pro_action(frame)
    # pro_action(img)

    if cap.isOpened():
        while True:
            ret, img = cap.read()
            if ret:
                cv2.imshow("file", img)
                cv2.waitKey(25)
                pro_action(cap)
            else:
                break

    cap.release()
    cv2.destroyAllWindows()
