from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from paddleocr import PaddleOCR
import os
import shutil
import uuid
import time
import re

app = FastAPI(
    title="API OCR - Reçus",
    description="Extraction de texte et d'informations depuis des images",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

print("Chargement du modèle PaddleOCR...")
ocr = PaddleOCR(use_angle_cls=True, lang="en")
print("Modèle PaddleOCR chargé.")

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


def lire_image_ocr(image_path):
    start = time.time()

    result = ocr.ocr(image_path, cls=True)

    texte = ""

    if result and result[0]:
        for ligne in result[0]:
            texte += ligne[1][0] + "\n"

    duree = round(time.time() - start, 2)

    return texte, duree


def extraire_informations(texte):
    infos = {
        "magasin": "",
        "date": "",
        "total": "",
        "articles": []
    }

    lignes = texte.split("\n")

    if len(lignes) > 0:
        infos["magasin"] = lignes[0].strip()

    date = re.search(r"\d{2}[/-]\d{2}[/-]\d{2,4}", texte)
    if date:
        infos["date"] = date.group()

    total = re.search(r"TOTAL.*?([0-9]+\.[0-9]{2})", texte, re.IGNORECASE)
    if total:
        infos["total"] = total.group(1)

    return infos


@app.get("/")
def home():
    return {
        "message": "Bienvenue dans l'API OCR",
        "documentation": "/docs"
    }


@app.get("/health")
def health():
    return {
        "status": "API opérationnelle"
    }


@app.post("/extract-text")
async def extract_text(file: UploadFile = File(...)):
    file_path = os.path.join(UPLOAD_DIR, f"{uuid.uuid4()}_{file.filename}")

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    try:
        texte, duree = lire_image_ocr(file_path)

        return JSONResponse(content={
            "texte": texte,
            "temps_ocr_secondes": duree
        })

    finally:
        if os.path.exists(file_path):
            os.remove(file_path)


@app.post("/extract-info")
async def extract_info(file: UploadFile = File(...)):
    file_path = os.path.join(UPLOAD_DIR, f"{uuid.uuid4()}_{file.filename}")

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    try:
        texte, duree = lire_image_ocr(file_path)
        infos = extraire_informations(texte)

        return JSONResponse(content={
            "informations": infos,
            "temps_ocr_secondes": duree
        })

    finally:
        if os.path.exists(file_path):
            os.remove(file_path)