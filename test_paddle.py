import easyocr

reader = easyocr.Reader(['en'])

result = reader.readtext(r"C:\Users\HP\Pictures\test.png", detail=0)

print(result)