import pytesseract
import cv2
import matplotlib.pyplot as plt
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
img=cv2.imread("text.png")
#plt.imshow(img)
img2char=pytesseract.image_to_string(img,lang="eng")
print(img2char)