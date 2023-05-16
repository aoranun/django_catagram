import cv2
import numpy as np
import time


def yolodetect(image):
    # Load YOLO model
    CONFIG_FILE='catagram\yolo\config\yolov3.cfg'
    WEIGHTS_FILE='catagram\yolo\config\yolov3.weights'
    LABELS_FILE='catagram\yolo\config\coco.names'

    net = cv2.dnn.readNet(WEIGHTS_FILE, CONFIG_FILE)
    LABELS = open(LABELS_FILE).read().strip().split("\n")

    # Get image dimensions
    image = cv2.imread(image)
    height, width, _ = image.shape

    # Create a blob from the input image and forward pass it through the network
    blob = cv2.dnn.blobFromImage(image, 1/255.0, (416, 416), swapRB=True, crop=False)
    net.setInput(blob)
    output_layers_names = net.getUnconnectedOutLayersNames()
    layer_outputs = net.forward(output_layers_names)

    # Initialize lists for detected bounding boxes, confidences and class IDs
    boxes = []
    confidences = []
    class_ids = []

    t0 = time.time()
    # Loop through the layer outputs
    for output in layer_outputs:
        # Loop through each detected object
        for detection in output:
            # Extract the class ID and confidence of the prediction
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]

            # Ignore predictions with low confidence
            if confidence > 0.5:
                # Extract the bounding box coordinates
                center_x, center_y, w, h = (detection[0:4] * np.array([width, height, width, height])).astype("int")
                x = int(center_x - w / 2)
                y = int(center_y - h / 2)
                boxes.append([x, y, int(w), int(h)])
                confidences.append(float(confidence))
                class_ids.append(class_id)
                if LABELS[class_id] == 'cat' :
                    #print(LABELS[class_id], confidences)
                    
                    #cv2.imshow('image',image)

                    #cv2.waitKey(0)

                    #cv2.destroyAllWindows()
                    t1 =time.time()
                    #print('เวลาในการสร้าง: %f'%(t1-t0))
                    return image                 
                

    # Perform non-maximum suppression to remove overlapping bounding boxes
    #indices = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)
    #print(indices)

    # Draw the bounding boxes on the input image
    #if indices > 0:
    #    for i in indices:
    #        #i = i[0]
    #        box = boxes[i]
    #        x, y, w, h = box
    #        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
            

#    cv2.imshow('image',image)

 #   cv2.waitKey(0)

 #   cv2.destroyAllWindows()
    
 #   return image

# Load input image
#image = cv2.imread("cat2.jpg")

# Detect objects in the image
#output_image = yolodetect

yolodetect(r'C:\Users\MiniDragon\Documents\test\cnc.jpg')

