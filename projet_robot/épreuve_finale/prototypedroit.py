import time
import cv2
import numpy as np
from math import*
import requests
import controller
import json

c=controller.Controller()
x,y,dire=175,25,0

aruco_dict = cv2.aruco.Dictionary_get(cv2.aruco.DICT_6X6_50)
parameters = cv2.aruco.DetectorParameters_create()
camera_matrix = np.array([[1.21863664e+03, 0.00000000e+00, 3.89606385e+02],[0.00000000e+00, 1.21604236e+03, 2.91523582e+02],[0.00000000e+00, 0.00000000e+00, 1.00000000e+00]])  # Exemple pour une caméra standard
dist_coeffs = np.array([[ 4.87005446e-01,  2.76682195e+00, -2.63558181e-03,  1.36492998e-02,-2.23536210e+00,  3.54899770e-01,  2.75318659e+00,  2.11062607e+00,0.00000000e+00,  0.00000000e+00,  0.00000000e+00,  0.00000000e+00,0.00000000e+00,  0.00000000e+00]])  # Aucun coefficient de distorsion, à remplacer si besoin
markerSizeInM = 0.02

liste_arucos = []
capturecounter = 0

def mouvement(c: controller.Controller,dist,angle=False,vit = 30):
    global x,y,dire
    nbtick=abs((dist*9000)/50)
    c.get_encoder_ticks()
    sens=copysign(1,dist)
    if not angle:
        speed = [sens*vit,sens*vit]
    else:
        speed = [sens*vit,-sens*vit]
    c.set_raw_motor_speed(*speed)
    ticks = list(c.get_encoder_ticks())
    t=time.time()

    if not angle :    #avancer
        while (abs(ticks[0]) or abs(ticks[1])) <= nbtick:
            temp = list(c.get_encoder_ticks())
            ticks[0], ticks[1] = abs(ticks[0]) + abs(temp[0]), abs(ticks[1]) + abs(temp[1] )
            if ticks[0] >= ticks[1]:
                speed[0] = sens*30
                speed[1] = sens*34
                c.set_raw_motor_speed(speed[0], speed[1])
            if ticks[1] > ticks[0]:
                speed[1] = sens*30
                speed[0] = sens*34
                c.set_raw_motor_speed(speed[0], speed[1])
            diff=time.time()-t
            if diff>1:
                diff=0
                t=time.time()
                if dire==0:
                    y=y+sens*9.5
                elif dire==180:
                    y=y-sens*9.5
                elif dire==90:
                    x=x+sens*9.5
                elif dire==270:
                    x=x-sens*9.5
                requests.post('http://proj103.r2.enst.fr/api/pos?x='+str(x)+'&y='+str(y))
        c.standby()

    else:    #tourner
        if abs(dist)==90:
            nbtick=1775
        elif abs(dist)==45:
            nbtick=737
        elif abs(dist)==360:
            nbtick=8000
        else:
            nbtick=abs((dist*1700)/90)
        while (abs(ticks[0])<=nbtick or abs(ticks[1]) <=nbtick):
            temp = list(c.get_encoder_ticks())
            ticks[0], ticks[1] = abs(ticks[0]) + abs(temp[0]), abs(ticks[1]) + abs(temp[1])
            #if nbtick-ticks[0]<100 and speed[0]>20:
             #   speed = [speed[0]-sens*1,speed[1]+sens*1]
              #  c.set_raw_motor_speed(*speed)
        time.sleep(0.07)
        c.standby()
        dire=(dire+dist)%360
    time.sleep(0.5)

def scan():
    cap = cv2.VideoCapture(0)
    global x,y,dire,capturecounter
    listecorners=[]
    listeids=[]
    for i in range(20):
        ret,frame=cap.read()
        gray=cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        corners,ids,rejectedImgPoints = cv2.aruco.detectMarkers(gray, aruco_dict, parameters=parameters)
        listecorners.append(corners)
        listeids.append(ids)
    maxi=0
    id=0
    for i in range(20):
        if len(listeids[i])>=maxi:
            id=i
    corners=listecorners[id]
    ids=listeids[id]
    if len(corners) > 0:
        dista=distancesingle(corners)
        posx,posy = correct_aruco_position(x,y,dire,dista) #Il faut possiblement faire l'inverse de la direction dépendamment de si dir est la direction où regarde le robot
        liste_arucos.append({"x" : posx,"y" : posy,"dir" : orientationaruco2(dire),"marker_id" : ids[0][0],"captured" : captured}) #L'orientation est en angles
    cap.release()

def captureflag2():
    for i in range(len(liste_arucos)):
        yflag = liste_arucos[i]["y"]
        if yflag>y and yflag-50<y and liste_arucos[i][] 
    




def distance(corners,num):
    if len(corners)>=1:
        #moyhaut=(np.abs(corners[0][0][0][1]-corners[0][0][3][1])+np.abs(corners[0][0][1][1]-corners[0][0][2][1]))/2 ancienne manière de calculer la distance
        #dist=m*moyhaut + b same
        rvec , tvec, _ = cv2.aruco.estimatePoseSingleMarkers(corners, markerSizeInM, camera_matrix, dist_coeffs)
        return(100*tvec[num][0][2])  #J'ai inversé num et 0      
        return(dist)
    return(500)

def distancesingle(corners):
    if len(corners)>=1:
        #moyhaut=(np.abs(corners[0][0][0][1]-corners[0][0][3][1])+np.abs(corners[0][0][1][1]-corners[0][0][2][1]))/2 ancienne manière de calculer la distance
        #dist=m*moyhaut + b same
        rvec , tvec, _ = cv2.aruco.estimatePoseSingleMarkers(corners, markerSizeInM, camera_matrix, dist_coeffs)
        return(100*tvec[0][0][2])        
        return(dist)
    return(500)
