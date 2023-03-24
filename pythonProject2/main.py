import time
import cv2
import cvzone
from cvzone.PoseModule import PoseDetector
import numpy as np

cap = cv2.VideoCapture(0)

detector = PoseDetector()
ptime = 0
ctime = 0
color = (0,0,255)
dir = 0
push_up = 0
while True:
    # noinspection PyUnresolvedReferences
    _, img = cap.read()
    p = 1.5
    w = int(img.shape[1] * p)
    h = int(img.shape[0] * p)
    img = cv2.resize(img, (w, h))

    assert isinstance(img, object)
    img = detector.findPose(img)
    lmlst, bbox = detector.findPosition(img, draw=False)
    assert isinstance(lmlst, object)
    if lmlst:
        # print(lmlst)
        a1 = detector.findAngle(img, 12, 14, 16)
        a2 = detector.findAngle(img, 15, 13, 11)
        a3 = detector.findAngle(img, 13, 11, 12)
        a4 = detector.findAngle(img, 14, 12, 11)
        per_val1 = np.interp(a1,(85,155),(100,0))
        per_val2 = np.interp(a2,(85,155),(100,0))
        bar_val1 = int(np.interp(per_val1,(0,100),(40+350,40)))
        bar_val2 = int(np.interp(per_val2,(0,100),(40+350,40)))
        # print(per_val1)
        # 1st bar
        cv2.rectangle(img,(860,bar_val1),(860+35, 45+350),color,cv2.FILLED)
        cv2.rectangle(img,(860,45),(860+35,45+350),(),3)
        # 2nd bar
        cv2.rectangle(img,(45,bar_val2),(45+35,45+350),color,cv2.FILLED)
        cv2.rectangle(img, (45,45), (45 + 35, 45 + 350), (), 3)
        # bar 1
        cvzone.putTextRect(img,f'{int(per_val1)} %',(36,45),1.1,2,colorT=(255,255,255),colorR=color,border=2,colorB=())
        # bar 2
        cvzone.putTextRect(img,f'{int(per_val2)} %',(858,45),1.1,2,colorT=(255,255,255),colorR=color,border=2,colorB=())
        int(a3)
        int(a4)
        if per_val1 == 100 and per_val2 == 100:

            if dir == 0 :
                push_up += 0.5
                dir = 1
                color = (0,255,0)
        elif per_val1 == 0 and per_val2 == 0:
            if dir == 1:
                push_up += 0.5
                dir = 0
                color = (0,255,0)
        else:
            color = (0,0,255)
        cvzone.putTextRect(img,f'Push Ups : {push_up}',(428,700),1.6,2,colorT=(255,255,255),colorR=(255,0,0),border=2,
                           colorB=())
        cvzone.putTextRect(img,'Left Hand',(21,460),1.1,2,colorT=(255,255,255),colorR=(255,0,0),border=2,
                           colorB=()) 
        cvzone.putTextRect(img, 'Right Hand', (844, 460), 1.1, 2, colorT=(255, 255, 255),colorR=(255, 0, 0), border=2,
                           colorB=())

    ctime = time.time()
    fps = 1/(ctime-ptime)
    ptime = ctime
    cvzone.putTextRect(img,f'FPS : {int(fps)}',(436,28),1.2,2,colorT=(255,255,255),colorR=(0,125,0),border=2,colorB=())
    # noinspection PyUnresolvedReferences
    cv2.imshow('push-ups counter', img)

    # noinspection PyUnresolvedReferences
    if cv2.waitKey(1) == ord('a'):
        break
cap.release()
cv2.destroyAllWindows()
