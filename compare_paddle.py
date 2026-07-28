import os
import csv
import time
from paddleocr import PaddleOCR

ocr = PaddleOCR(lang="en")

folder = "data"

with open("resultats_paddle.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["Image", "Temps (s)", "Texte"])

    for image in sorted(os.listdir(folder)):
        if image.lower().endswith((".jpg", ".jpeg", ".png")):

            image_path = os.path.join(folder, image)

            start = time.time()
            result = ocr.ocr(image_path)
            end = time.time()

            texte = ""

            if result and result[0]:
                for line in result[0]:
                    texte += line[1][0] + " "

            writer.writerow([image, round(end - start, 2), texte])

print("Fichier CSV créé : resultats_paddle.csv")