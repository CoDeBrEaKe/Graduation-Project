import pytesseract
from PIL import Image
import pyttsx3
from googletrans import Translator

img = Image.open('tmp.png')
print(img)
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

result = pytesseract.image_to_string(img)

with open('abc4.txt', mode='w') as file:
    file.write(result)
    print(result)

engine = pyttsx3.init()

engine.say(result)
engine.runAndWait()