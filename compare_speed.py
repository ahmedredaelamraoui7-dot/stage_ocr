import time
from PIL import Image
import pytesseract

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

start = time.time()

img = Image.open(r"C:\Users\HP\stage_ocr\data\0.jpg")
text = pytesseract.image_to_string(img)

end = time.time()

print("Texte :")
print(text)
print("Temps :", end - start, "secondes")