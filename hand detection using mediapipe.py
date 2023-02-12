import cv2

import mediapipe as mp
import pytesseract
import pyttsx3


cap = cv2.VideoCapture("https://192.168.1.3:8080/video")
# cap = cv2.VideoCapture(0)
mp_hands = mp.solutions.hands
hands = mp_hands.Hands()
mpDraw = mp.solutions.drawing_utils

while True:
    success, image = cap.read()
    imageRGB = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = hands.process(imageRGB)

    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:  # working with each hand
            for id, lm in enumerate(handLms.landmark):
                h, w, c = image.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                if id == 8:
                    cv2.circle(image, (cx, cy), 12, (255, 0, 255), cv2.FILLED)
                    # print(lm)
                    # print(cx)
                    # print(cy)

                    # Start Text Detection
                    extra, frame = cap.read()
                    boxes = pytesseract.image_to_data(frame)
                    # print(boxes)
                    for x, y in enumerate(boxes.splitlines()):
                        if x != 0:
                            y = y.split()
                            if len(y) == 12:
                                x_axis, y_axis, w, h = int(y[6]), int(y[7]), int(y[8]), int(y[9])
                                if cx >= x_axis and cx <= x_axis + w:
                                    if cy >= y_axis and cy <= y_axis + h:
                                        the_word = y[11]
                                        engine = pyttsx3.init()
                                        voices = engine.getProperty('voices')
                                        engine.setProperty('voice', voices[1].id)
                                        engine.say(the_word)
                                        engine.runAndWait()
                                        print(the_word)
                    # cv2.imshow('video capture', frame)
                    cv2.waitKey(3)
                    if cv2.waitKey(1) & 0xFF == ord('q'):
                        break

                    # End Text Detection

                mpDraw.draw_landmarks(image, handLms, mp_hands.HAND_CONNECTIONS)
    cv2.imshow("Output", image)
    cv2.waitKey(1)

cap.release()
cv2.destroyAllWindows()
