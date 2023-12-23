# 初始化日志
import logging
import time
from pynput import keyboard
import pyautogui
import pyttsx3
import win32gui
from paddleocr import PaddleOCR

from moyu_check import checkRightRenwuBan, checkLingQuRenWu, checkHuoXianZhuiJiao, checkZiDongXunLu, checkMyLocation, \
    checkFangWaiGuai, checkBB, checkIsSiWang
from moyu_constance import click_lingqu_mianban, click_lingqujiangli, click_lingqu_rewnu1, click_lingqu_rewnu1_1, \
    click_lingqu_rewnu2, click_lingqu_rewnu3, detect_huoxianzhuijiao, \
    click_lingqu_rewnu7, topBianJie, bottomBianJie, leftBianJie, rightBianJie, click_scroll_huoxian, click_huanshou, \
    click_huanshou_gezi1, click_huanshou_fuhua, click_huanshou_diuqi_out, click_huanshou_diuqi_queding, \
    detect_siwang_point, click_bb1_chuzheng, click_bb2_chuzheng, click_huchu_zidongxunlu
from moyu_util import windwow_capture, leftClick

# 游戏运行
doing = 1
# 默认打怪往左边走
goLeft = 1
# 上次检测宝宝的时间
lastCheckBBTime = time.time()


# 监听按键
def on_press(key):
    # 监听按键
    if str(key) == 'Key.esc':
        global doing
        doing = 0


# 检测状态
def check(hwnd):
    # 检测是否领取了任务
    logging.info("检测是否领取了任务")
    result = checkLingQuRenWu(ocr)
    # 需要点击领取奖励
    if result == 2:
        logging.info("点击领取奖励")
        x, y = click_lingqujiangli
        leftClick(left + x, top + y)
        time.sleep(1)
        # 重新截屏，方便下一次
        windwow_capture(hwnd)
    # 继续打怪
    elif result == 1:
        logging.info("打怪")
        daguai(ocr)
    # 需要领取任务
    else:
        logging.info("需要领取任务")
        clickPoints = []
        clickPoints.append(click_lingqu_rewnu1)
        clickPoints.append(click_lingqu_rewnu1_1)
        clickPoints.append(click_lingqu_rewnu2)
        clickPoints.append(click_lingqu_rewnu3)
        for i in clickPoints:
            x, y = i
            leftClick(left + x, top + y)
            time.sleep(1)
        # 查找火线追缴
        logging.info("准备滚动查找火线追缴")
        x, y = click_scroll_huoxian
        # 向下滑动鼠标20
        pyautogui.mouseDown(left + x, top + y, button='left')
        pyautogui.dragTo(left + x, top + y + 300, button='left')
        time.sleep(2)
        # 查找火线追缴
        windwow_capture(hwnd)
        logging.info("识别火线追缴")
        x, y = checkHuoXianZhuiJiao(ocr)
        if x != 0 and y != 0:
            logging.info("魔怪追缴令识别坐标：" + str(x) + "," + str(y))
            pyautogui.mouseUp()
            x, y = x + detect_huoxianzhuijiao[0], y + detect_huoxianzhuijiao[1]
            logging.info("魔怪追缴令真实坐标：" + str(x) + "," + str(y))
            clickPoints = []
            clickPoints.append((x, y))
            clickPoints.append((x, y + 35))
            clickPoints.append(click_lingqu_rewnu7)
            for i in clickPoints:
                x, y = i
                leftClick(left + x, top + y)
                time.sleep(1)
            while True:
                # 这里的时间有点长，因为自动寻路不是立马弹出的
                time.sleep(1)
                logging.info("点击外部一下，呼出自动寻路")
                x, y =click_huchu_zidongxunlu
                leftClick(left + x, top + y)
                time.sleep(2)
                 # 取消自动寻路
                logging.info("查询界面是否是自动寻路")
                windwow_capture(hwnd)
                x, y = checkZiDongXunLu(ocr)
                if x != 0 and y != 0:
                    logging.info("取消自动寻路")
                    leftClick(left + x, top + y)
                    time.sleep(1)
                    break
        daguai(ocr)


# 打怪
def daguai(ocr):
    # 检测是否死亡
    result = checkIsSiWang()
    if result == 1:
        countDown = 20
        while (countDown > 0):
            logging.info("等待" + str(countDown) + "秒点击原地复活")
            time.sleep(1)
            countDown -= 1
        time.sleep(20)
        x, y = detect_siwang_point
        # 点击原地复活
        leftClick(left + x, top + y)
        time.sleep(3)
        # 点击出征宝宝1
        x, y = click_bb1_chuzheng
        leftClick(left + x, top + y)
        time.sleep(1)
        # 点击出征宝宝2
        x, y = click_bb2_chuzheng
        leftClick(left + x, top + y)
        time.sleep(1)
    currentTime = time.time()
    global lastCheckBBTime
    # 检测宝宝，间隔5分钟
    if (currentTime - lastCheckBBTime) > 5 * 60:
        lastCheckBBTime = currentTime
        x, y = click_huanshou
        logging.info("点击幻兽,打开")
        # 点击幻兽
        leftClick(left + x, top + y)
        time.sleep(1)
        logging.info("点击孵化所,打开")
        # 点击孵化所
        x, y = click_huanshou_fuhua
        leftClick(left + x, top + y)
        time.sleep(1)

        while True:
            logging.info("鼠标移动到幻兽第一个格子")
            # 鼠标移动到幻兽第一个格子
            x, y = click_huanshou_gezi1
            pyautogui.moveTo(left + x, top + y)
            # 截屏
            windwow_capture(hwnd)
            result = checkBB(ocr)
            if result == 0:
                logging.info("没有找到宝宝")
                break
            elif result == 1:
                logging.info("是需要的宝宝，放到孵化所")
                leftClick(left + x, top + y)
                time.sleep(2)
            else:
                logging.info("丢弃该宝宝")
                # 按下宝宝
                pyautogui.mouseDown(left + x, top + y, button='left')
                x, y = click_huanshou_diuqi_out
                # 鼠标移动到外面
                pyautogui.dragTo(left + x, top + y, button='left')
                # 抬起丢弃
                pyautogui.mouseDown(left + x, top + y, button='left')
                pyautogui.mouseUp()
                time.sleep(2)
                # 丢弃界面弹出
                x, y = click_huanshou_diuqi_queding
                leftClick(left + x, top + y)
                time.sleep(2)
        # 点击孵化所,关闭
        logging.info("点击孵化所,关闭")
        x, y = click_huanshou_fuhua
        leftClick(left + x, top + y)
        time.sleep(1)
        # 点击幻兽
        logging.info("点击幻兽,关闭")
        x, y = click_huanshou
        leftClick(left + x, top + y)
        time.sleep(1)
    windwow_capture(hwnd)
    # 检测自己的坐标
    x, y = checkMyLocation(ocr)
    if (x == 0 or y == 0):
        # 如果坐标为0，可能弹出了防外挂
        logging.info("自己坐标为0，查询是否弹出防外挂检测")
        result = checkFangWaiGuai(ocr)
        # 检测到了防外挂
        if result == 1:
            while 1:
                engine.say("外挂检测")
                engine.runAndWait()
                time.sleep(1)
    else:
        logging.info("自己坐标：" + str(x) + "," + str(y))
        global goLeft
        # 位置修正，Y方向
        if y < topBianJie:
            # 1536,1152
            # 下598,686 右 952，711，上991，372，左445，383
            #  下0.389,0.595 右0.619，0.617，上0.593，0.322，左0.289，0.332
            cX = left + width * 0.389
            cY = top + height * 0.595
            logging.info("小于上边界，向下偏移")
            pyautogui.mouseDown(cX, cY, button='left')
            time.sleep(0.1)
            pyautogui.mouseUp()
            time.sleep(0.1)
        if y > bottomBianJie:
            cX = left + width * 0.593
            cY = top + height * 0.322
            logging.info("大于下边界，向上偏移")
            pyautogui.mouseDown(cX, cY, button='left')
            time.sleep(0.1)
            pyautogui.mouseUp()
            time.sleep(0.1)
            # 到了左边界了，需要往右边移动
        if x < leftBianJie:
            goLeft = 0
            logging.info("调整方向，向右偏移")
        elif x > rightBianJie:
            # 到了左边界了，需要往右边移动
            goLeft = 1
            logging.info("调整方向，向左偏移")
        if goLeft == 1:
            cX = left + width * 0.289
            cY = top + height * 0.332
            logging.info("向左偏移")
            pyautogui.mouseDown(cX, cY, button='left')
            time.sleep(1.6)
            pyautogui.mouseUp()
        else:
            cX = left + width * 0.619
            cY = top + height * 0.585
            logging.info("向右偏移")
            pyautogui.mouseDown(cX, cY, button='left')
            time.sleep(1.6)
            pyautogui.mouseUp()
        pyautogui.keyDown("f1")
        time.sleep(1.2)
        pyautogui.keyUp("f1")


# 初始化日志
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
file_handler = logging.FileHandler('log.txt')
logger.addHandler(file_handler)
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
file_handler.setFormatter(formatter)

logging.info("初始化语音播报")
# 初始化语音播报
engine = pyttsx3.init()
engine.setProperty("voice", "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_ZH-CN_HUIHUI_11.0")
logging.info("监听按键")
# 连接事件以及释放
listener = keyboard.Listener(on_press=on_press)
listener.start()
while True:
    print("获取魔域的窗口")
    # 获取魔域的窗口
    hwnd = win32gui.FindWindow(None, "【魔域】")
    if hwnd != 0:
        logging.info("找到魔域窗口")
        # 获取窗口大小和位置
        left, top, right, bottom = win32gui.GetWindowRect(hwnd)
        width = right - left
        height = bottom - top
        print(left, top, right, bottom)
        # 将创建指定窗口的线程设置到前台，并且激活该窗口
        win32gui.SetForegroundWindow(hwnd)
        # 延时1秒
        time.sleep(1)
        # 初始化OCR
        ocr = PaddleOCR(use_angle_cls=True, lang="ch")  # need to run only once to download and load model into memory
        logging.info("初始化OCR")
        # 抓拍一张图片
        windwow_capture(hwnd)
        # 第一步检测右侧任务表有没有弹出来
        logging.info("检测右侧任务表有没有弹出来")
        result = checkRightRenwuBan(ocr)
        # 如果没有打开面板
        if result == 0:
            x, y = click_lingqu_mianban
            leftClick(left + x, top + y)
            time.sleep(1)
        # 循环工作
        while doing:
            check(hwnd)
    print("finish")
    exit(0)
