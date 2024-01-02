import ddddocr

ocr = ddddocr.DdddOcr(beta=True)

with open("../images/验证码1.png", 'rb') as f:
    image = f.read()

res = ocr.classification(image)
print(res)