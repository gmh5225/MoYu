import os
import random

import numpy as np
from PIL import Image, ImageDraw
from PIL import ImageFont


def createPic(font, fontcolor, shuzi1, shuzi2, suan, pic):
    img = Image.new(mode='RGB', size=(300, 100))
    draw = ImageDraw.Draw(img)
    draw.rectangle((15, 15, 260, 80), fill=(255, 255, 255))

    shuzi1 = Image.open(shuzi1)
    shuzi1 = shuzi1.resize((50, 50))
    data = list(shuzi1.getdata())
    #print(data)
    for i in range(len(data)):
        if data[i] != (255, 255, 255):
            data[i] = fontcolor
    tempImg = Image.new(shuzi1.mode, shuzi1.size)
    tempImg.putdata(data=data)
    px = 60
    py = 20
    img.paste(tempImg, (px, py))  # 将图像填充为中间图像，两侧为灰色的样式

    shuzi2 = Image.open(shuzi2)
    shuzi2 = shuzi2.resize((50, 50))
    data = list(shuzi2.getdata())
    #print(data)
    for i in range(len(data)):
        if data[i] != (255, 255, 255):
            data[i] = fontcolor
    tempImg = Image.new(shuzi2.mode, shuzi2.size)
    tempImg.putdata(data=data)
    px = 200
    py = 20
    img.paste(tempImg, (px, py))  # 将图像填充为中间图像，两侧为灰色的样式

    source3 = Image.open(suan)
    source3 = source3.resize((50, 50))
    data = list(source3.getdata())
    for i in range(len(data)):
        if data[i] != (255, 255, 255):
            data[i] = fontcolor
    tempImg = Image.new(source3.mode, source3.size)
    tempImg.putdata(data=data)
    px = 120
    py = 30
    img.paste(tempImg, (px, py))  # 将图像填充为中间图像，两侧为灰色的样式

    draw = ImageDraw.Draw(img)

    # 画噪点
    for i in range(100):
        # 第一个参数为点的位置，第二个参数为点的颜色
        startX = 15 + random.randint(1, 245)
        startY = 15 + random.randint(1, 65)
        rW = random.randint(2, 5)
        rH = random.randint(1, 2)
        rLineWidth = random.randint(1, 3)
        draw.line((startX, startY, startX + rW, startY + rH), width=rLineWidth, fill=fontcolor)
        startX = 15 + random.randint(1, 245)
        startY = 15 + random.randint(1, 65)
        # 画圆弧？
        rLineWidth = random.randint(1, 3)
        draw.arc((startX, startY, startX + 4, startY + 4), 0, 90, width=rLineWidth, fill=fontcolor)
    img.save(pic)
    print("Successfully!")


shuziDir = "H://DataSets/MOYUwaigua/MNIST3"
jiaDir = "H://DataSets/MOYUwaigua/jia"
jianDir = "H://DataSets/MOYUwaigua/jian"
fontDir = '../font'
shuziFiles = os.listdir(shuziDir)
jiaFiles = os.listdir(jiaDir)
jianFiles = os.listdir(jianDir)
# 字体的位置，不同版本的系统会有不同
fontFils = os.listdir(fontDir)

# for i in range(22):
#     fontPath=fontDir+ "/" +fontFils[i]
#     s=fontFils[i].split("ttf")
#     if(len(s)==2):
#         os.rename(fontPath,fontDir+ "/"+str(i+1)+".ttf")
#     else :
#         s=fontFils[i].split("otf")
#         os.rename(fontPath,fontDir+ "/"+str(i+1)+".otf")

count = 1500
# for i in range(500):
#     # 字体颜色，默认为蓝色
#     # 字体的位置，不同版本的系统会有不同
#     fontPath = fontDir + "/" + random.choice(fontFils)
#     # fontPath=fontDir+ "/" +fontFils[i]
#     fontcolor = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
#     #print(fontcolor)
#     font = ImageFont.truetype(fontPath, 50)  # 验证码的字体
#     shuzi1 = shuziDir + "/" + random.choice(shuziFiles)
#     shuzi2 = shuziDir + "/" + random.choice(shuziFiles)
#     jiaP = jiaDir + "/" + random.choice(jiaFiles)
#     createPic(font, fontcolor, shuzi1, shuzi2, jiaP, "../test/" + str(count) + ".png")
#     count += 1

for i in range(500):
    fontPath =fontDir+ "/" + random.choice(fontFils)
    fontcolor =(random.randint(0,255),random.randint(0,255),random.randint(0,255))
    #print(fontcolor)
    font = ImageFont.truetype(fontPath,50) #验证码的字体
    shuzu1File=random.choice(shuziFiles)
    shuzi1Name=int(shuzu1File.split('_')[0].replace("train",""))
    shuzi1 = shuziDir + "/" + shuzu1File

    shuzu2File=random.choice(shuziFiles)
    shuzi2Name=int(shuzu2File.split('_')[0].replace("train",""))
    shuzi2 = shuziDir + "/" + shuzu2File

    jianP = jianDir + "/" + random.choice(jianFiles)
    if shuzi1Name > shuzi2Name:
        createPic(font,fontcolor,shuzi1, shuzi2, jianP, "../test/" + str(count) + ".png")
    else:
        createPic(font,fontcolor,shuzi2, shuzi1, jianP, "../test/" + str(count) + ".png")
    count+=1
