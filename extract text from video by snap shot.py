[7:01 PM, 2/12/2023] Habeba Adnan 🌸🌸: import cv2
import numpy as np
import matplotlib.pyplot as plt
import pytesseract
import pyttsx3 
from gtts import gTTS

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
tessdata_dir_config = r'--tessdata-dir "C:\Program Files\Tesseract-OCR\tessdata"'

img=cv2.imread("book.png")
img=cv2.cvtColor(img,cv2.COLOR_BGR2RGB)

h,w,c = img.shape
if w > 100:
    new_w=1000
    ar=w/h
    new_h=int(new_w/ar)
    img=cv2.resize(img,(new_w,new_h),interpolation=cv2.INTER_AREA)

plt.imshow(img)

def threshoding(image):
    img_gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    ret,thres=cv2.threshold(img_gray,80,225,cv2.THRESH_BINARY_INV)
    plt.imshow(thres,cmap="gray")
    return thres

thres_img=threshoding(img)   
kernal=np.ones((3,85)…
[7:02 PM, 2/12/2023] Habeba Adnan 🌸🌸: line detection
[7:02 PM, 2/12/2023] Habeba Adnan 🌸🌸: import sys
from os import path

import cv2
import numpy as np

from PyQt5 import QtCore
from PyQt5 import QtWidgets
from PyQt5 import QtGui

import pytesseract
from PIL import Image
from pytesseract import image_to_string
from gtts import gTTS
import os


pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

tessdata_dir_config = r'--tessdata-dir "C:\Program Files\Tesseract-OCR\tessdata"'



class RecordVideo(QtCore.QObject):
    image_data = QtCore.pyqtSignal(np.ndarray)

    def _init_(self, camera_port=0, parent=None):
        super()._init_(parent)
        self.camera = cv2.VideoCapture(camera_port)
        self.timer = QtCore.QBasicTimer()

    def start_recording(self):
        self.timer.start(0, self)

    
    def timerEvent(self, event):
        if (event.timerId() != self.timer.timerId()):
            return

        read, data = self.camera.read()
        if read:
            self.image_data.emit(data)
    def framesave(self):
        
        read, data = self.camera.read()
        if read:
            cv2.imwrite('a.png',data)
            img=Image.fromarray(data)
            img.load()
            
            text=pytesseract.image_to_string(img, config=tessdata_dir_config)
            print ('Text_Found: ',text,len(text))
            if len(text)>0:
                tts = gTTS(text=text, lang='en')# for english language use (lang='en')
                tts.save("pcvoice.mp3")
                os.system("start pcvoice.mp3")


class FaceDetectionWidget(QtWidgets.QWidget):
    
    def _init_(self, parent=None):
        super()._init_(parent)
        self.image = QtGui.QImage()
        self._red = (0, 0, 255)
        self._width = 2
        self._min_size = (30, 30)


    def image_data_slot(self, image_data):


        
        self.image = self.get_qimage(image_data)
        if self.image.size() != self.size():
            self.setFixedSize(self.image.size())

        self.update()
    
        
        
    def get_qimage(self, image: np.ndarray):
        height, width, colors = image.shape
        bytesPerLine = 3 * width
        QImage = QtGui.QImage

        image = QImage(image.data,
                       width,
                       height,
                       bytesPerLine,
                       QImage.Format_RGB888)

        image = image.rgbSwapped()
        return image

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        painter.drawImage(0, 0, self.image)
        self.image = QtGui.QImage()


class MainWidget(QtWidgets.QWidget):
    def _init_(self, parent=None):
        super()._init_(parent)
        
        self.face_detection_widget = FaceDetectionWidget()

        # TODO: set video port
        self.record_video = RecordVideo()

        image_data_slot = self.face_detection_widget.image_data_slot
        self.record_video.image_data.connect(image_data_slot)

        layout = QtWidgets.QVBoxLayout()

        layout.addWidget(self.face_detection_widget)
        self.run_button = QtWidgets.QPushButton('Start')
        layout.addWidget(self.run_button)

        self.run_button.clicked.connect(self.record_video.start_recording)

        self.screenshot = QtWidgets.QPushButton('Snap Shot')
        layout.addWidget(self.screenshot)

        self.screenshot.clicked.connect(self.record_video.framesave)
        self.setLayout(layout)


    
def main():
    app = QtWidgets.QApplication(sys.argv)

    main_window = QtWidgets.QMainWindow()
    main_widget = MainWidget()
    main_window.setCentralWidget(main_widget)
    main_window.show()

    sys.exit(app.exec_())


if _name_ == '_main_':

    main()