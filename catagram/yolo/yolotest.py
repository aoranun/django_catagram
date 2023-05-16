import yolotest2
import testdetect
import testyolov5
a = yolotest2.yolodetect(r'C:\Users\MiniDragon\Documents\test\cat6.jpg')
w = testyolov5.modelcat(a)
#for i in testdetect.detectword(w):
#    print(i)
print(testdetect.detectword(w))