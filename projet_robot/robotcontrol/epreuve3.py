import cv2
import camapp
import numpy as np
import time
import app3
import controller
c=controller.Controller()

aruco=[]
i=0
aruco_dict = cv2.aruco.Dictionary_get(cv2.aruco.DICT_6X6_50)
parameters = cv2.aruco.DetectorParameters_create()
ref=[1,2,3,4]
pos=[25,-25,0,0]




def detect(aruco):
    cap = cv2.VideoCapture(0)
    ret,frame=cap.read()
    gray=cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    corners,ids,rejectedImgPoints = cv2.aruco.detectMarkers(gray, aruco_dict, parameters=parameters)
    dista=camapp.distance(corners)
    id=camapp.arucodetect(corners,ids,aruco)
    return(id,dista)

def bolzano(aruco):
    ide,distan=detect(aruco)
    if ide!=500:
        if ide!=0 and distan<50:
            aruco=camapp.captureflag(aruco,ide)
            time.sleep(0.5)
            return(1)
    return(500)

def automatique_parcours(c:controller.Controller):
    aruco=[]
    i=0
    aruco_dict = cv2.aruco.Dictionary_get(cv2.aruco.DICT_6X6_50)
    parameters = cv2.aruco.DetectorParameters_create()
    ref=[1,2,3,4]
    pos=[25,-25,0,0]
    b=0
    row,col=0,1
    while True:
        pos=app3.check_move(c,30,30,50,pos)
        row+=1
        for k in range(3):
            pos=app3.tourner_45(c,-30,30,pos)
            b=-1
            time.sleep(0.5)
            a=bolzano(aruco)
            time.sleep(1)
            if a==1:
                break
            pos=app3.check_move(c,30,-30,0,pos)
            b=1
            time.sleep(0.5)
            a=bolzano(aruco)
            time.sleep(0.5)
            if a==1:
                break
            pos=app3.tourner_45(c,30,-30,pos)
            time.sleep(0.5)
            if k<2:
                pos=app3.check_move(c,30,30,50,pos)
                col+=1
                time.sleep(0.5)
                pos=app3.check_move(c,-30,30,0,pos)
            time.sleep(0.5)
        if a==1:
            break
        pos=app3.check_move(c,-30,30,0,pos)
        time.sleep(0.5)
        pos=app3.check_move(c,30,30,50,pos)
        row+=1
        time.sleep(0.5)
        for k in range(2):
            pos=app3.tourner_45(c,30,-30,pos)
            time.sleep(0.5)
            a=bolzano(aruco)
            time.sleep(0.5)
            if a==1:
                break
            pos=app3.check_move(c,-30,30,0,pos)
            time.sleep(0.5)
            a=bolzano(aruco)
            time.sleep(0.5)
            if a==1:
                break
            pos=app3.tourner_45(c,-30,30,pos)
            time.sleep(0.5)
            if k<1:
                pos=app3.check_move(c,30,30,50,pos)
                col-=1
                time.sleep(0.5)
                pos=app3.check_move(c,30,-30,0,pos)
            time.sleep(0.5)

        #pos=app3.check_move(c,30,-30,0,pos)
        time.sleep(0.5)
        if a==1:
            break

    print(aruco)
    pos=app3.tourner_45(c,-30,30,pos)
    time.sleep(0.5)
    print(pos)
    if a==1:
        case_cote=2-(round(pos[0])//50)
        case_avant=5-(round(pos[1])//50)
        while pos[2]!=0:
            pos=app3.check_move(c,30,-30,0,pos)
            time.sleep(0.5)
        for i in range(case_avant):
            pos=app3.check_move(c,30,30,50,pos)
            time.sleep(0.5)
        pos=app3.check_move(c,30,-30,0,pos)
        time.sleep(0.5)
        for i in range(case_cote):
            pos=app3.check_move(c,30,30,50,pos)
            time.sleep(0.5)
        pos=app3.check_move(c,30,-30,0,pos)
        time.sleep(0.5)

    while True:
        b=0
        for k in range(3):
            pos=app3.tourner_45(c,-20,20,pos)
            b=-1
            time.sleep(0.5)
            a=bolzano(aruco)
            time.sleep(1)
            if a==1:
                break
            pos=app3.check_move(c,30,-30,0,pos)
            b=1
            time.sleep(0.5)
            a=bolzano(aruco)
            time.sleep(0.5)
            if a==1:
                break
            pos=app3.tourner_45(c,32,-30,pos)
            time.sleep(0.5)
            if k<2:
                pos=app3.check_move(c,30,30,50,pos)
                time.sleep(0.5)
                pos=app3.check_move(c,-30,30,0,pos)
            time.sleep(0.5)
        if a==1:
            break
        pos=app3.check_move(c,-30,30,0,pos)
        time.sleep(0.5)
        pos=app3.check_move(c,30,30,45,pos)
        time.sleep(0.5)
        for k in range(3):
            pos=app3.tourner_45(c,30,-30,pos)
            time.sleep(0.5)
            a=bolzano(aruco)
            time.sleep(0.5)
            if a==1:
                break
            pos=app3.check_move(c,-30,30,0,pos)
            time.sleep(0.5)
            a=bolzano(aruco)
            time.sleep(0.5)
            if a==1:
                break
            pos=app3.tourner_45(c,-30,30,pos)
            time.sleep(0.5)
            if k<2:
                pos=app3.check_move(c,30,30,50,pos)
                time.sleep(0.5)
                pos=app3.check_move(c,30,-30,0,pos)
            time.sleep(0.5)

        pos=app3.check_move(c,30,-30,0,pos)
        time.sleep(0.5)
        if a==1:
            break
