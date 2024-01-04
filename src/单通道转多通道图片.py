
import os

import cv2
import numpy as np
from PIL import Image

shuziDir = "H://DataSets/MOYUwaigua/MNIST/"
shuzi1Dir = "H://DataSets/MOYUwaigua/MNIST3/"
shuziFiles = os.listdir(shuziDir)


for img_name in os.listdir(shuziDir):
    path=shuziDir+img_name
    print(path)
    image=Image.open(path)
    if len(image.split())==1: #查看通道数
        print(len(image.split()))
        img = cv2.imread(path)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        img2 = np.zeros_like(img)
        img2[:,:,0] = gray
        img2[:,:,1] = gray
        img2[:,:,2] = gray
        cv2.imwrite(shuzi1Dir+img_name, img2)
