import os
import csv
import time
import easyocr

reader = easyocr.Reader(['en'])

folder = "data"

with open("resultats_easy.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["Image", "Temps (s)", "Texte"])

    for image in sorted(os.listdir(folder)):
        if image.lower().endswith((".jpg", ".jpeg", ".png")):

            image_path = os.path.join(folder, image)

            start = time.time()
            result = reader.readtext(image_path, detail=0)
            end = time.time()

            texte = " ".join(result)

            writer.writerow([image, round(end-start,2), texte])

print("Terminé : resultats_easy.csv")