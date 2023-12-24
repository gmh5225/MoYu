import logging

import pyautogui
import win32gui
from PIL import Image
from PIL import ImageGrab

global scaleScreen


def windwow_capture(hwnd):
    # 获取窗口大小和位置
    left, top, right, bottom = win32gui.GetWindowRect(hwnd)
    # 截图
    grab_image = ImageGrab.grab((left, top, right, bottom))
    grab_image.save("screenshot.png")


# 检测图片，所有
def checkImage(ocr, rect):
    im = Image.open('./screenshot.png')  # (411, 273)
    region = im.crop(rect)  # 裁剪
    region.save("crop.png")
    result = ocr.ocr('./crop.png', cls=True)
    logging.info(result)
    return result

# 鼠标左键点击
def leftClick(x, y):
    pyautogui.mouseDown(x, y, button='left')
    pyautogui.mouseUp()

# 鼠标滚动
def mouseScroll(x, y, dy):
    pyautogui.moveTo(x, y)
    pyautogui.scroll(dy)

# 获取真实大小
def realDetectSize(size):
    left, top, right, bootom = size
    return int(left * scaleScreen), int(top * scaleScreen), int(right * scaleScreen), int(bootom * scaleScreen)


# 获取真实大小
def realPoint(point):
    x, y = point
    return int(x * scaleScreen), int(y * scaleScreen)

# 对图片进行扩大，因为有些图片，较小，识别率低
def letterbox_image(image, size):
    # 对图片进行resize，使图片不失真。在空缺的地方进行padding
    iw, ih = image.size
    w, h = size
    scale = min(w / iw, h / ih)
    nw = int(iw * scale)
    nh = int(ih * scale)
    image = image.resize((nw, nh), Image.Resampling.BICUBIC)
    new_image = Image.new('RGB', size, (128, 128, 128))
    new_image.paste(image, ((w - nw) // 2, (h - nh) // 2))
    return new_image
