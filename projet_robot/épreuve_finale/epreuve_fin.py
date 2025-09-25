import up_down_r_l
import controller
import time
from math import*
import camapp
import cv2
import numpy as np
import requests
import json

c=controller.Controller()

aruco=[]
aruco_dict = cv2.aruco.Dictionary_get(cv2.aruco.DICT_6X6_50)
parameters = cv2.aruco.DetectorParameters_create()
 

response = requests.post("http://proj103.r2.enst.fr/api/udta?idx=1", data=json.dumps(liste_arucos))
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
    x,y,dire=up_down_r_l.position()
    if ide!=500:
        if ide!=0 and distan<50:
            aruco=camapp.captureflag(aruco,ide)
            row,col=round(y)//50,round(x)//50
            lettre=["F","E","D","C","B","A"]
            row_lettre=lettre[row]
            requests.post('http://proj103.r2.enst.fr/api/marker?id='+str(ide)+'&col='+str(col)+'&row='+str(row))
            time.sleep(0.5)
            return(1)
    return(500)

def scan_aruco():
    aruco=[]
    arucos_captures=[]
    aruco_simple = {}
    aruco_dict = cv2.aruco.Dictionary_get(cv2.aruco.DICT_6X6_50)
    parameters = cv2.aruco.DetectorParameters_create()
    id, dist = bolzano(aruco)
    if id == 500:
        return
    else:
        if id!=0:
            if len(arucos_captures) <=2:
                if dire==315:
                    aruco_simple = {
                        "x" : x,
                        "y" : y, 
                        "dir" : "SE", 
                        "marker_id" : id, 
                        "captured" : True 
                    }
                    arucos_captures.append(aruco_simple)
                    response = requests.post("http://proj103.r2.enst.fr/api/udta?idx=1", data=json.dumps(arucos_captures))
                    return
                else:
                    aruco_simple = {
                        "x" : x,
                        "y" : y, 
                        "dir" : "SW", 
                        "marker_id" : id, 
                        "captured" : True 
                    }
                    arucos_captures.append(aruco_simple)
                    response = requests.post("http://proj103.r2.enst.fr/api/udta?idx=1", data=json.dumps(arucos_captures))
                    return
            else: 
                return
        else:
            if dire==315:
                aruco_simple = {
                    "x" : x,
                    "y" : y, 
                    "dir" : "SE", 
                    "marker_id" : id, 
                    "captured" : False 
                }
                arucos_captures.append(aruco_simple)
                response = requests.post("http://proj103.r2.enst.fr/api/udta?idx=1", data=json.dumps(arucos_captures))
                return
            else:
                aruco_simple = {
                    "x" : x,
                    "y" : y, 
                    "dir" : "SW", 
                    "marker_id" : id, 
                    "captured" : False 
                }
                arucos_captures.append(aruco_simple)
                response = requests.post("http://proj103.r2.enst.fr/api/udta?idx=1", data=json.dumps(arucos_captures))
                return

def phase1_robot(aruco,c):
    up_down_r_l.mouvement(c,-45,True)
    time.sleep(0.5)
    scan_aruco()
    up_down_r_l.mouvement(c,90,True)
    time.sleep(0.5)
    up_down_r_l.mouvement(c,-45,True)
    for i in range(6):
        up_down_r_l.mouvement(c,50)
        time.sleep(0.5)
        up_down_r_l.mouvement(c,-45,True)
        time.sleep(0.5)
        scan_aruco()
        up_down_r_l.mouvement(c,90,True)
        time.sleep(0.5)
        up_down_r_l.mouvement(c,-45,True)
        time.sleep(0.5)
    up_down_r_l.mouvement(c,50)

