import os
from paddleocr import PaddleOCR

ocr = PaddleOCR(
    use_angle_cls=True,
    lang="en",
    enable_mkldnn=False,
    use_gpu=False
)

img_path = r"C:\Users\HP\Downloads\archive\images\17.jpg"
output_txt_path = "ocr_result.txt"

result = ocr.ocr(img_path, cls=True)

with open(output_txt_path, "w", encoding="utf-8") as f:
    if result and result[0]:
        for line in result[0]:
            text = line[1][0]
            f.write(text + "\n")

print("Success!")
print("Text saved in:", os.path.abspath(output_txt_path))