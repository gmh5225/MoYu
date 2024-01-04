import time

import torch
import cv2
from yolov5.models.common import DetectMultiBackend
from yolov5.utils.dataloaders import LoadImages
from yolov5.utils.general import non_max_suppression, scale_boxes, xyxy2xywh, Profile, xywh2xyxy

device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')
model = DetectMultiBackend('../best.pt', device=device)
# 标签
labels = {
    0: '9',
    1: '+',
    2: '2',
    3: '0',
    4: '5',
    5: '6',
    6: '-',
    7: '1',
    8: '3',
    9: '8',
    10: '7',
    11: '4'
}
t = time.time()
img_path = "../resource1/验证码2.jpg"
dataset = LoadImages(img_path)
seen, windows, dt = 0, [], (Profile(), Profile(), Profile())

result = []
for path, im, im0s, vid_cap, s in dataset:
    with dt[0]:
        im = torch.from_numpy(im).to(model.device)
        im = im.half() if model.fp16 else im.float()  # uint8 to fp16/32
        im /= 255  # 0 - 255 to 0.0 - 1.0
        if len(im.shape) == 3:
            im = im[None]  # expand for batch dim
    # Inference
    with dt[1]:
        pred = model(im)
    # NMS
    with dt[2]:
        pred = non_max_suppression(pred)
    # Process predictions
    for i, det in enumerate(pred):  # per image
        seen += 1
        p, im0, frame = path, im0s.copy(), getattr(dataset, 'frame', 0)
        sw, sh, d = im0.shape
        gn = torch.tensor(im0.shape)[[1, 0, 1, 0]]  # normalization gain whwh
        if len(det):
            # Rescale boxes from img_size to im0 size
            det[:, :4] = scale_boxes(im.shape[2:], det[:, :4], im0.shape).round()
            # Write results
            for *xyxy, conf, cls in reversed(det):
                xywh = torch.tensor(xyxy).view(1, 4).view(-1).tolist()
                x, y, w, h = int(xywh[0]), int(xywh[1]), int(xywh[2])-int(xywh[0]), int(xywh[3])- int(xywh[1])
                name = labels[int(cls)]
                c = "{:.2f}".format(conf)
                result.append((name, c, (x, y, w, h)))
print("耗时：" + str(time.time() - t))
print(result)
img = cv2.imread(img_path)
print(img.shape)
for i in range(len(result)):
    name, c, (x, y, w, h) = result[i]
    cv2.rectangle(img, (x, y, w, h), (255, 0, 0), 2)
cv2.imshow('frame', img)
cv2.waitKey()
cv2.destroyAllWindows()
