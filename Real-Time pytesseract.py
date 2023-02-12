import time
import os
import cv2
import numpy as np
import pytesseract
import pyttsx3 as pyttsx3
pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'


cap = cv2.VideoCapture("http://192.168.1.4:8080/video")
while True:
    # Capture each frame from the video feed
    extra, frame = cap.read()
    boxes = pytesseract.image_to_data(frame)
    print(boxes)
    for x, y in enumerate(boxes.splitlines()):
        if x != 0:
            y = y.split()
            if len(y) == 12:
                x_axis, y_axis, w, h = int(y[6]), int(y[7]), int(y[8]), int(y[9])
                the_word = y[11]
                engine = pyttsx3.init()
                voices = engine.getProperty('voices')
                engine.setProperty('voice', voices[1].id)
                engine.say(the_word)
                engine.runAndWait()
                print(the_word)
    cv2.imshow('video capture' , frame)
    cv2.waitKey(10)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        cap.release()
        cv2.destroyAllWindows()
        break