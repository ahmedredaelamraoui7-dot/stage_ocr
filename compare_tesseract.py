import os
import csv
import time
import pytesseract
from PIL import Image

# Chemin vers Tesseract
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

folder = "data"

with open("resultats_tesseract.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["Image", "Temps (s)", "Texte"])

    for image in sorted(os.listdir(folder)):
        if image.lower().endswith((".jpg", ".jpeg", ".png")):

            image_path = os.path.join(folder, image)

            start = time.time()

        
            texte = pytesseract.image_to_string(Image.open(image_path))

    
            texte = " ".join(texte.split())

            end = time.time()

            writer.writerow([image, round(end - start, 2), texte])

print("Terminé : resultats_tesseract.csv")