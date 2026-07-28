import os
import time
import cv2
import pytesseract
import easyocr
from paddleocr import PaddleOCR
from doctr.io import DocumentFile
from doctr.models import ocr_predictor

IMAGE_DIR = "data"

images = sorted([
    f for f in os.listdir(IMAGE_DIR)
    if f.endswith((".jpg", ".jpeg", ".png"))
])

easy_reader = easyocr.Reader(['en', 'fr'])
paddle_ocr = PaddleOCR(use_angle_cls=True, lang='en')
doctr_model = ocr_predictor(pretrained=True)

temps_total = {
    "tesseract": 0.0,
    "easyocr": 0.0,
    "paddleocr": 0.0,
    "doctr": 0.0
}

for img_name in images:
    img_path = os.path.join(IMAGE_DIR, img_name)
    print(f"\nImage : {img_name}")


    debut = time.time()
    img = cv2.imread(img_path)
    pytesseract.image_to_string(img)
    temps_total["tesseract"] += time.time() - debut


    debut = time.time()
    easy_reader.readtext(img_path, detail=0)
    temps_total["easyocr"] += time.time() - debut


    debut = time.time()
    paddle_ocr.ocr(img_path, cls=True)
    temps_total["paddleocr"] += time.time() - debut


    debut = time.time()
    doc = DocumentFile.from_images(img_path)
    doctr_model(doc)
    temps_total["doctr"] += time.time() - debut

n = len(images)

print("\n=== RÉSUMÉ ===")
for moteur, total in temps_total.items():
    print(f"{moteur:<12} total={total:.2f}s   moy={total/n:.3f}s")