import sys
import cv2
import os
from sys import platform

#from test import *



dir_path = r"D:\openpose\build"



try:
    # Windows Import
    if platform == "win32":
        # Change these variables to point to the correct folder (Release/x64 etc.)
        sys.path.append(r"D:\openpose\build\python\openpose\Release");
        os.environ['PATH'] = os.environ['PATH'] + ';' + "D:\\openpose\\build\\x64\\Release;" + 'D:\\openpose\\build\\bin;'
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

    def out_img(self, image):
            self.datum = op.Datum()
            self.datum.cvInputData = image
            self.opWrapper.emplaceAndPop(op.VectorDatum([self.datum]))


if __name__ == "__main__":
    OP = Opnenpose()
    #cap = cv2.VideoCapture(r"D:\NexTep\Main_code\video\1.JENNIE_SOLO.mp4")
    cap = cv2.VideoCapture(r"D:\test\DeepInSpr\Video\TigerWoods\Front\TigerWoods_Front.mp4")
    #cap = cv2.VideoCapture(r"rtsp://admin:123456@192.168.0.216:8554/live")
    # cap = cv2.VideoCapture(0)
    img = cv2.imread(r"D:\test\DeepInSpr\Collin.jpg")
    #pro_action(cap)

    while (cap.isOpened()):

        ret, frame = cap.read()
        if ret:
            try:
                #OP = Opnenpose()
                OP.out_frame(frame)
                OP.out_img(img)

                #cv2.imshow("OpenPose 1.5.1 - Tutorial Python API", OP.datum.cvOutputData)
                cv2.imshow("img", OP.datum.cvOutputData)
                cv2.imshow("OpenPose 1.7.1 - Tutorial Python API", frame)

                if cv2.waitKey(10) & 0xFF == ord('q'):
                    break

            except Exception as e:
                print(e)
        else:
            break

    cap.release()
    cv2.destroyAllWindows()

