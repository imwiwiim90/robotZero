import cv2
import numpy as np

FRAME_SIZE = 160
class VideoCamera(object):
    def __init__(self):
        # Using OpenCV to capture from device 0. If you have trouble capturing
        # from a webcam, comment the line below out and use a video file
        # instead.
        self.video = cv2.VideoCapture(0)
        # If you decide to use video.mp4, you must have this file in the folder
        # as the main.py.
        #self.video = cv2.VideoCapture('sample.mp4')
    
    def __del__(self):
        self.video.release()
    
    def get_frame(self):
        success, image = self.video.read()

        # We are using Motion JPEG, but OpenCV defaults to capture raw images,
        # so we must encode it into JPEG in order to correctly display the
        # video stream.
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        #ret, jpeg = cv2.imencode('.jpg', image)
        ans = ""
        for x in np.nditer(image):
            ans += chr(x)
        return ans

    def int_to_byte3(self,number):
        byte = ''
        for i in range(3):
            byte += chr(number%256)
            number = number/256
        return byte

    def get_small_frame(self):
        success, image = self.video.read()
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        rows , cols = image.shape
        #M = cv2.getRotationMatrix2D((cols/2,rows/2),0,0.125)
        #dst = cv2.warpAffine(image,M,(cols,rows))
        #dst = dst[(rows*7)/16:(rows*9)/16,(cols*7)/16:(cols*9)/16]
        dst = image[:160,:160]
        img_str = cv2.imencode('.jpg',dst, [int(cv2.IMWRITE_JPEG_QUALITY), 50])[1].tostring()
        return img_str

    def get_image_slides(self):
        success, image = self.video.read()
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        rows , cols = image.shape
        frames = []
        for y in range(0,rows,FRAME_SIZE):
            for x in range(0,cols,FRAME_SIZE):
                frame = image[y:y+FRAME_SIZE,x:x+FRAME_SIZE]
                frame = cv2.imencode('.jpg',frame, [int(cv2.IMWRITE_JPEG_QUALITY), 50])[1].tostring()
                frame = self.int_to_byte3(y) + self.int_to_byte3(x) + frame
                frames.append(frame)
        return frames



