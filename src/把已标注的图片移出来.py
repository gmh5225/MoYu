import os
import shutil

pic_dir = "H://DataSets/MOYUwaigua/moyu/test"
img_dir="H://DataSets/MOYUwaigua/moyu/train"
list = os.listdir(pic_dir)
for i in range(0, len(list)):
    path = os.path.join(pic_dir, list[i])
    if '.txt' in path:
        pic_path=path[:-4]+'.png'
        if os.path.exists(pic_path):
            shutil.move(path, img_dir)
            shutil.move(pic_path, img_dir)