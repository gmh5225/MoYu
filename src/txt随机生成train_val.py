import os
import random
import shutil
import sys

root_path = 'H://DataSets/MOYUwaigua/moyu/train'

trainDir = root_path + "/images/train/"
testDir = root_path + "/images/test/"
validDir = root_path + "/images/valid/"

train_test_percent = 0.95  # (训练集+验证集)/(训练集+验证集+测试集)
train_valid_percent = 0.93  # 训练集/(训练集+验证集)
total_txt=[]
list = os.listdir(root_path)
for i in range(0, len(list)):
    if list[i].endswith('.txt'):
        total_txt.append(list[i])

num = len(total_txt)
list = range(num)
tv = int(num * train_test_percent)  # 训练集+验证集数量
ts = int(num - tv)  # 测试集数量
tr = int(tv * train_valid_percent)  # 训练集数量
tz = int(tv - tr)  # 验证集数量
trainval = random.sample(list, tv)
train = random.sample(trainval, tr)

print("train and valid size:", tv)
print("train size:", tr)
print("valid size:", tz)
print("test size:", ts)


# ftrainall = open(txtsavepath + '/ftrainall.txt', 'w')
ftest = open(root_path + '/test.txt', 'w')
ftrain = open(root_path + '/train.txt', 'w')
fvalid = open(root_path + '/valid.txt', 'w')

# 建立cg数据的文件夹
new_dataset_train = root_path + '/images/train/'
new_dataset_test = root_path + '/images/test/'
new_dataset_valid = root_path + '/images/valid/'

new_dataset_trainl = root_path + '/labels/train/'
new_dataset_testl = root_path + '/labels/test/'
new_dataset_validl = root_path + '/labels/valid/'

if not os.path.exists(new_dataset_train):
    os.makedirs(new_dataset_train)
if not os.path.exists(new_dataset_test):
    os.makedirs(new_dataset_test)
if not os.path.exists(new_dataset_valid):
    os.makedirs(new_dataset_valid)
if not os.path.exists(new_dataset_trainl):
    os.makedirs(new_dataset_trainl)
if not os.path.exists(new_dataset_testl):
    os.makedirs(new_dataset_testl)
if not os.path.exists(new_dataset_validl):
    os.makedirs(new_dataset_validl)

for i in list:
    imgname = total_txt[i][:-4] + '.png'
    xmlname = total_txt[i][:-4] + '.txt'
    if i in trainval:
        # ftrainall.write(name)
        if i in train:
            ftrain.write(trainDir + imgname + '\n')
            shutil.move(root_path + "/" + imgname, new_dataset_train)
            shutil.move(root_path + "/" + xmlname, new_dataset_trainl)

        else:
            fvalid.write(validDir + imgname + '\n')
            shutil.move(root_path + "/" + imgname, new_dataset_valid)
            shutil.move(root_path + "/" + xmlname, new_dataset_validl)
    else:
        ftest.write(testDir + imgname + '\n')
        shutil.move(root_path + "/" + imgname, new_dataset_test)
        shutil.move(root_path + "/" + xmlname, new_dataset_testl)
# ftrainall.close()
ftrain.close()
fvalid.close()
ftest.close()
