import torch
import cv2

name =[]
myfile = open("catagram\yolo\config\coco.names", "r")
for i in myfile:
    line = str(i)
    line = line.strip('\n')
    name.append(line)

def yolodetect(image):
# โหลดโมเดล YOLOv7
    model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)

# โหลดภาพที่ต้องการตรวจจับ
    image = cv2.imread(image)

# ทำการตรวจจับวัตถุและวาดกรอบสี่เหลี่ยมรอบวัตถุที่ตรวจพบบนภาพ
    results = model(image)
    for detection in results.xyxy[0]:
        label = name[int(detection[5])]
        if label == 'cat':
            return image



# แสดงผลภาพ

