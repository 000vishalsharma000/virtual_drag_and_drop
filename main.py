import cv2
from cvzone.HandTrackingModule import HandDetector
import cvzone
import numpy as np

cap = cv2.VideoCapture(1)
cap.set(3,1280)
cap.set(4, 720)
detector = HandDetector(detectionCon=0.8)
colorR= (255, 0, 255) # by default color purple of rectangle

cx, cy, w, h,=100, 100, 200, 200



class DragRect():
    def __init__(self, posCenter,  colorR,size=[200,200]):
        self.posCenter = posCenter
        self.size = size
        self.colorR=colorR

    def update(self , cursor):
        cx, cy = self.posCenter
        w, h = self.size

        # if the index finger tip in rectangle area
        if cx - w // 2 < cursor[0] < cx + w // 2 and cy - h // 2 < cursor[1] < cy + h // 2:
            self.posCenter = cursor[0] , cursor[1]
            self.colorR = (0, 255, 0)


rectList=[]
for x in range(5):
    rect = DragRect([x*250+150, 150], (255, 0, 255))
    rectList.append(rect)

while True:

    success, img = cap.read()
    img= cv2.flip(img, 1) # 1 for horizontal flip
    hands, img = detector.findHands(img)
    if hands:
        lmList= hands[0]["lmList"] # list of loc of all point on hand

        l,_,_= detector.findDistance([lmList[8][0], lmList[8][1]], [lmList[12][0], lmList[12][1]], img)
        print(l)

        if(l<80): # clicked

            cursor= lmList[8] #your x, y, z of index finger tip ( given in media pipe lib)
            for rect in rectList:
                rect.update(cursor) # call update
        else:
            for rect in rectList:
                rect.colorR=(255, 0,255)



    # #draw solid rectangle
    # for rect in rectList:
    #     cx, cy = rect.posCenter
    #     w, h = rect.size
    #     cv2.rectangle(img, (cx-w//2,cy-h//2 ),(cx+w//2,cy+h//2 ), rect.colorR, cv2.FILLED )
    #     cvzone.cornerRect(img, (cx-w//2,cy-h//2 ,w, h), 20, rt=0)

    #draw transparent rectangle
    imgNew =np.zeros_like(img, np.uint8)
    for rect in rectList:
        cx, cy =rect.posCenter
        w, h =rect.size
        cv2.rectangle(imgNew, (cx-w//2,cy-h//2 ),(cx+w//2,cy+h//2 ), rect.colorR, cv2.FILLED )
        cvzone.cornerRect(imgNew, (cx-w//2,cy-h//2 ,w, h), 20, rt=0)

    out =img.copy()
    alpha=0.1
    mask=imgNew.astype(bool)
    out[mask] = cv2.addWeighted(img, alpha, imgNew, 1-alpha, 0)[mask]





    cv2.imshow("Image", out)
    cv2.waitKey(1)

