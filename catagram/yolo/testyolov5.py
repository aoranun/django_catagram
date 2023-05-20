import torch
import yolov5

# Image
#img = r'C:\Users\MiniDragon\Documents\test\cat6.jpg'
def modelcat(img):
  ca =[]
  #ca2 =[]
  catmodel=['catjump','catrun','catsit','catsleep']
  # Model
  model = torch.hub.load('ultralytics/yolov5', 'custom', path='catagram/yolo/config/best.pt')
  # Inference
  results = model(img)

  for obj in results.xyxy[0]:
    label = int(obj[5])
    confidence = float(obj[4])
    ca.append([catmodel[label],confidence])
    
  con = (results.pandas().xyxy[0]['confidence'])
  ca2 = max(con)
  for i in ca:
    if ca2 in i :
      return i[0]

#modelcat(r'C:\Users\MiniDragon\Documents\test\cat6.jpg')