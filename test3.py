import cv2
from cv2 import VideoCapture

from Openpose import Opnenpose
OP = Opnenpose()

#import test2_clone
#import score_show
#import data_preprocessing

class VideoOpenpose(object):
    def __init__(self, video):
        self.video = VideoCapture(video)
        self.OP_target = Opnenpose()

    def run(self):
        while self.video.isOpened():
            ret_video, frame_video = self.video.read()

            if ret_video:
                self.OP_target.out_frame(frame_video)



if __name__ == '__main__':
    cap = cv2.VideoCapture(r"D:\test\DeepInSpr\Video\TigerWoods\Front\TigerWoods_Front.mp4")
    VideoOpenpose(cap)
