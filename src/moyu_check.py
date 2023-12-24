import logging

from PIL import Image

from moyu_constance import detect_lingqu_renwu, detect_huoxianzhuijiao, detect_zidongxunlun_center, \
    detect_zidongxunlun_left, detect_my_location_x, detect_my_location_y, detect_fang_waiguai, \
    click_cancel_leftzidongxunlu, click_cancel_centerzidongxunlu, detect_bb_shishenm, \
    detect_siwang_point, click_huanshou_gezi1
from moyu_util import checkImage, letterbox_image, realDetectSize, realPoint


# 检测右边的任务版是否打开
def checkRightRenwuBan(ocr):
    result = checkImage(ocr, realDetectSize(detect_lingqu_renwu))
    if not any(result):
        return 0
    for idx in range(len(result)):
        res = result[idx]
        for line in res:
            if len(line) == 2:
                c, score = line[1]
                if '第' in c or '章' in c or '达' in c or '到' in c or '级' in c:
                    return 1
    return 0


# 检测是否领取了任务
def checkLingQuRenWu(ocr):
    result = checkImage(ocr, realDetectSize(detect_lingqu_renwu))
    if not any(result):
        return 0
    for idx in range(len(result)):
        res = result[idx]
        for line in res:
            if len(line) == 2:
                c, score = line[1]
                if '领' in c or '取' in c or '奖' in c or '励' in c:
                    return 2
    for idx in range(len(result)):
        res = result[idx]
        for line in res:
            if len(line) == 2:
                c, score = line[1]
                if '火' in c or '线' in c or '追' in c or '200' in c:
                    return 1
    return 0


# 查看火线追缴
# [[[75.0, 379.0], [178.0, 379.0], [178.0, 404.0], [75.0, 404.0]], ('魔怪追剿令', 0.919135570526123)]
def checkHuoXianZhuiJiao(ocr):
    result = checkImage(ocr, realDetectSize(detect_huoxianzhuijiao))
    if not any(result):
        return 0
    for idx in range(len(result)):
        res = result[idx]
        for line in res:
            if len(line) == 2:
                p = line[0]
                c, score = line[1]
                if '魔怪追剿令' in c:
                    return int(p[0][0]), int(p[0][1])
    return 0, 0


# 检测是否有自动寻路
def checkZiDongXunLu(ocr):
    # 检测中间的自动寻路
    result = checkImage(ocr, realDetectSize(detect_zidongxunlun_center))
    if not any(result):
        return 0, 0
    for idx in range(len(result)):
        res = result[idx]
        for line in res:
            if len(line) == 2:
                c, score = line[1]
                if '自动寻路' in c:
                    return realPoint(click_cancel_centerzidongxunlu)
    # 检测左边的自动寻路
    result = checkImage(ocr, realDetectSize(detect_zidongxunlun_left))
    if not any(result):
        return 0, 0
    for idx in range(len(result)):
        res = result[idx]
        for line in res:
            if len(line) == 2:
                c, score = line[1]
                if '自动寻路' in c:
                    return realPoint(click_cancel_leftzidongxunlu)
    return 0, 0


# 检测当前坐标
def checkMyLocation(ocr):
    list = []
    list.append(realDetectSize(detect_my_location_x))
    list.append(realDetectSize(detect_my_location_y))
    xy = [0, 0]
    for idx in range(len(list)):
        detect = list[idx]
        im = Image.open('./screenshot.png')  # (411, 273)
        region = im.crop(detect)  # 裁剪
        # 这里比较特殊，由于图片过小，需要增加padding，提高识别
        new_image = letterbox_image(region, (300, 300))
        new_image.save("crop.png")
        result = ocr.ocr('./crop.png', cls=True)
        logging.info(result)
        if not any(result):
            xy[idx] = 0
        else:
            for j in range(len(result)):
                res = result[j]
                for line in res:
                    if len(line) == 2:
                        c, score = line[1]
                        try:
                            xy[idx] = int(c)
                        except:
                            logging.info("解析x坐标异常")
    return xy[0], xy[1]


# 检测防外挂
def checkFangWaiGuai(ocr):
    result = checkImage(ocr, realDetectSize(detect_fang_waiguai))
    if not any(result):
        return 0
    for idx in range(len(result)):
        res = result[idx]
        for line in res:
            if len(line) == 2:
                c, score = line[1]
                if '回答' in c:
                    return 1
    return 0


# 检测是否领取奖励
def checkLingQuJiangli(ocr):
    result = checkImage(ocr, realDetectSize(detect_lingqu_renwu))
    if not any(result):
        return 0
    for idx in range(len(result)):
        res = result[idx]
        for line in res:
            if len(line) == 2:
                c, score = line[1]
                if '领' in c or '取' in c or '奖' in c or '励' in c:
                    return 2
    return 0


# 检测宝宝状态
def checkBB(ocr):
    img_src = Image.open('./screenshot.png')  # (411, 273)
    src_strlist = img_src.load()
    x, y = realPoint(click_huanshou_gezi1)
    # 100,100 是像素点的坐标
    data = src_strlist[x, y]
    #空的背包
    if data == (20, 22, 23):
        return 0
    else:
        result = checkImage(ocr, realDetectSize(detect_bb_shishenm))
        if not any(result):
            return -1
        for idx in range(len(result)):
            res = result[idx]
            for line in res:
                if len(line) == 2:
                    c, score = line[1]
                    if '莎菲' in c or '法师' in c or '凯隆' in c or '凯特' in c or '奥伦' in c:
                        return 1
        #其他宝宝
        return 2


# (232, 183, 241)
# 检测是否死亡
def checkIsSiWang():
    img_src = Image.open('./screenshot.png')  # (411, 273)
    src_strlist = img_src.load()
    x, y = realPoint(detect_siwang_point)
    # 100,100 是像素点的坐标
    data = src_strlist[x, y]
    if data == (232, 183, 241):
        return 1
    return 0
