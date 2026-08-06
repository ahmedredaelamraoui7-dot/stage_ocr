import os
import csv
import time
from doctr.io import DocumentFile
from doctr.models import ocr_predictor

model = ocr_predictor(pretrained=True)

folder = "data"

with open("resultats_doctr.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["Image", "Temps (s)", "Texte"])

    for image in sorted(os.listdir(folder)):
        if image.lower().endswith((".jpg", ".jpeg", ".png")):

            image_path = os.path.join(folder, image)

            start = time.time()

            doc = DocumentFile.from_images(image_path)
            result = model(doc).export()

            end = time.time()

            texte = ""

            for page in result["pages"]:
                for block in page["blocks"]:
                    for line in block["lines"]:
                        texte += " ".join(word["value"] for word in line["words"]) + " "

            writer.writerow([image, round(end - start, 2), texte])

print("Terminé : resultats_doctr.csv")