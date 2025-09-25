import cv2
import camapp
import numpy as np
import time
import up_down_r_l
import controller
import requests
import json
c=controller.Controller()

aruco=[]
i=0
liste_arucos=[]
flagcapture=0


# Charger le dictionnaire ArUco standard (par exemple, DICT_6X6_250)
aruco_dict = cv2.aruco.Dictionary_get(cv2.aruco.DICT_6X6_50)
parameters = cv2.aruco.DetectorParameters_create()
ref=[1,2,3,4]

mtx =np.array([[1.21863664e+03, 0.00000000e+00, 3.89606385e+02],
 [0.00000000e+00, 1.21604236e+03, 2.91523582e+02],
 [0.00000000e+00, 0.00000000e+00, 1.00000000e+00]])

dist = np.array([[ 4.87005446e-01,  2.76682195e+00, -2.63558181e-03,  1.36492998e-02,
  -2.23536210e+00,  3.54899770e-01,  2.75318659e+00,  2.11062607e+00,
   0.00000000e+00,  0.00000000e+00,  0.00000000e+00,  0.00000000e+00,
   0.00000000e+00,  0.00000000e+00]])

markerSizeInCM = 0.02

#Données de base
m=-0.30241622381224764
b=169.53351615676857
# Ouvrir la caméra (ou spécifier un fichier vidéo)
cap = cv2.VideoCapture(0)  # Utilisez '0' pour la caméra par défaut, ou un chemin vers un fichier vidéo
    # Lire une image de la caméra ou de la vidéo

def distance(corners):
    if len(corners)>=1:
        #moyhaut=(np.abs(corners[0][0][0][1]-corners[0][0][3][1])+np.abs(corners[0][0][1][1]-corners[0][0][2][1]))/2 ancienne manière de calculer la distance
        #dist=m*moyhaut + b same
        rvec , tvec, _ = cv2.aruco.estimatePoseSingleMarkers(corners, markerSizeInCM, mtx, dist)
        return(100*tvec[0][0][2])
    return(500)



def captureflag(): #Besoin de la position, juste liste des flags
    x,y,dire=up_down_r_l.position()
    cap = cv2.VideoCapture(0)
    ret,frame=cap.read()
    gray=cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    corners,ids,rejectedImgPoints = cv2.aruco.detectMarkers(gray, aruco_dict, parameters=parameters)
    dista=distance(corners)
    captured=False
    direction={45:"SW", 135:"NW",225:"NE",315:"SE"}
    if len(corners) > 1:
        if ids[0] not in [liste_arucos[i]["marker_id"] for i in range(len(liste_arucos))] and capturecounter < 2 and ids[0][0]!=0 and dista<50:
            captured=True
            flagcapture+=1
            mouvement(c,360,True) #Danser oui
            row,col=round(y)//50,round(x)//50
            lettre=["F","E","D","C","B","A"]
            row_lettre=lettre[row]
            requests.post('http://proj103.r2.enst.fr/api/marker?id='+str(ids[0][0])+'&col='+str(col)+'&row='+str(row))
        if dire==45:
            posx,posy=x+25,y+25
        elif dire==315:
            posx,posy=x-25,y+25
        elif dire==135:
            posx,posy=x-25,y-25
        elif dire==225:
            posx,posy=x+25,y-25
        liste_arucos.append({"x" : posx,"y" : posy,"dir" : direction[dire],"marker_id" : ids[0][0],"captured" : captured})
    cap.release()
    if ids[0][0]==0:
        return True
    return False

def phase1(c:controller.Controller):
    x,y,dire=up_down_r_l.position()
    aruco=[]
    i=0
    aruco_dict = cv2.aruco.Dictionary_get(cv2.aruco.DICT_6X6_50)
    parameters = cv2.aruco.DetectorParameters_create()
    ref=[1,2,3,4]
    b=0
    row,col=0,1
    for i in range(7):
        up_down_r_l.mouvement(c,45,True)
        a=captureflag()
        up_down_r_l.mouvement(c,-90,True)
        b=captureflag()
        up_down_r_l.mouvement(c,50)
        if b:
            up_down_r_l.mouvement(c,-135,True)
            b=captureflag()
            up_down_r_l.mouvement(c,135,True)
        if a:
            up_down_r_l.mouvement(c,135,True)
            a=captureflag()
            up_down_r_l.mouvement(c,-135,True)
    up_down_r_l.mouvement(c,180,True)
    response = requests.post("http://proj103.r2.enst.fr/api/udta?idx=1", data=json.dumps(liste_arucos))
    print(response.status_code)
    print(response.content)

def go_to(row,col):
    alpha={"Z":7,"A":6,"B":5,"C":4,"D":3,"E":2,"F":1,"G":0}
    delta_y=alpha[row]*50-y-25
    for i in range(abs(delta_y)//50):
        up_down_r_l.mouvement(c,50)
    delta_x=col*50-x-25
    if delta_x!=0:
        up_down_r_l.mouvement(c,90,True)
    for i in range(abs(delta_x)//50):
        up_down_r_l.mouvement(c,50)
    if delta_x!=0:
        up_down_r_l.mouvement(c,-90,True)


def phase2(c:controller.Controller):
    while True:
        response = requests.get("http://proj103.r2.enst.fr/api/udta?idx=2") #vous lisez dans le registre
        if(response.status_code == 200 and response.content != b''):
            data = json.parse(response.content)
            for i in range(len(data["instructions"])):
                # Split the string and add spaces back as separate elements
                res = [part if part.strip() else " " for part in data["instructions"][i].split(" ")]
                if res[0]=="CAPTURE":
                    go_to(res[1][:1],int(res[1][1:]))
                    up_down_r_l.mouvement(c,360,True)
                    requests.post('http://proj103.r2.enst.fr/api/marker?id='+res[2]+'&col='+res[1][:1]+'&row='+res[1][1:])
                elif res[0]=="CHECK":
                    x1=int(res[1])//50
                    x2=x1+1
                    y1=int(res[2])//50
                    y2=y1-1
                    lettre=["F","E","D","C","B","A"]
                    y1,y2=lettre[y1],lettre[y2]
                    for j in range(len(res)-3):
                        if res[3+j]=="SW":
                            go_to(x2,y2)
                            mouvement(c,45,True)
                            a=captureflag()
                            mouvement(c,-45,True)
                        if res[3+j]=="NW":
                            go_to(x2,y1)
                            mouvement(c,90,True)
                            mouvement(c,45,True)
                            a=captureflag()
                            mouvement(c,-90,True)
                            mouvement(c,-45,True)
                        if res[3+j]=="SE":
                            go_to(x1,y2)
                            mouvement(c,-45,True)
                            a=captureflag()
                            mouvement(c,45,True)
                        if res[3+j]=="NE":
                            go_to(x1,y1)
                            mouvement(c,-90,True)
                            mouvement(c,-45,True)
                            a=captureflag()
                            mouvement(c,90,True)
                            mouvement(c,45,True)
            go_to(0,G)
            requests.post("http://proj103.r2.enst.fr/api/udta?idx=3", data="done")
            break
        else:
            time.sleep(1)
            