import ddddocr

ocr = ddddocr.DdddOcr(beta=True)

with open("../images/img_1.png", 'rb') as f:
    image = f.read()

res = ocr.classification(image)
print(res)