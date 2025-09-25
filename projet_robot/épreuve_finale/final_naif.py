import cv2
import camapp
import numpy as np
import time
import up_down_r_l
import controller
c=controller.Controller()

aruco=[]
i=0
aruco_dict = cv2.aruco.Dictionary_get(cv2.aruco.DICT_6X6_50)
parameters = cv2.aruco.DetectorParameters_create()
ref=[1,2,3,4]
liste_aruco=[]
flagcapture=0


def detect(aruco):
    global x,y,ori,demi_ori
    cap = cv2.VideoCapture(0)
    ret,frame=cap.read()
    gray=cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    corners,ids,rejectedImgPoints = cv2.aruco.detectMarkers(gray, aruco_dict, parameters=parameters)
    dista=camapp.distance(corners)
    id=camapp.arucodetect(corners,ids,aruco)
    return(id,dista)

def capture(aruco):
    global x,y,ori,demi_ori
    ide,distan=camapp.detect(aruco)
    if ide!=500: #aruco non detecte
        if ide!=0 and distan<50:
            aruco=camapp.captureflag(aruco,ide)
            row,col=round(y)//50,round(x)//50
            lettre=["F","E","D","C","B","A"]
            row_lettre=lettre[row]
            #requests.post('http://proj103.r2.enst.fr/api/marker?id='+str(ide)+'&col='+str(col)+'&row='+str(row))
            return True
    return False

def captureflag(): #Besoin de la position, juste liste des flags
    x,y,dire=up_down_r_l.position()
    cap = cv2.VideoCapture(0)
    ret,frame=cap.read()
    gray=cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    corners,ids,rejectedImgPoints = cv2.aruco.detectMarkers(gray, aruco_dict, parameters=parameters)
    dista=distance(corners)
    captured=False
    if len(corners) > 1:
        if ids[0] not in [liste_arucos[i]["marker_id"] for i in range(len(liste_arucos))] and capturecounter < 2:
            captured=True
            capturecounter+=1
            mouvement(c,360,True) #Danser oui
        posx,posy = correct_aruco_position(x,y,dir,dista) #Il faut possiblement faire l'inverse de la direction dépendamment de si dir est la direction où regarde le robot
        liste_arucos.append({"x" : posx,"y" : posy,"dir" : dire,"marker_id" : ids[0],"captured" : captured})
    cap.release()

def parcours_final(c:controller.Controller):
    x,y,ori,demi_ori
    print(x,y,ori,demi_ori)
    aruco=[]
    i=0
    aruco_dict = cv2.aruco.Dictionary_get(cv2.aruco.DICT_6X6_50)
    parameters = cv2.aruco.DetectorParameters_create()
    ref=[1,2,3,4]
    b=0
    row,col=0,1
    for i in range(6):
        mouvement(c,50)
        mouvement(c,45,True)
        captureflag()
        a=capture(aruco)
        if a ==0:
            continue
