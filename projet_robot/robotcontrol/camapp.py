import cv2
import numpy as np
import controller
import app
import request

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

def captureflag(arucotrouve,id):
    ark=arucotrouve
    print(id)
    ark.append(id)
    print("Flag capturé :",id)
    app.tour_complet_robot(c,50,-50)
    return(ark)

def arucodetect(corners,ids,arucotrouve):
    if len(corners) > 0 :
        for i in range(len(ids)):
            id=ids[i]
            if id not in arucotrouve and id not in ref :
                print("Nouveau flag détecté :", id)
                return(id)
    return(500)

def detect(aruco):
    cap = cv2.VideoCapture(0)
    ret,frame=cap.read()
    gray=cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    corners,ids,rejectedImgPoints = cv2.aruco.detectMarkers(gray, aruco_dict, parameters=parameters)
    dista=distance(corners)
    id=arucodetect(corners,ids,aruco)
    return(id,dista)


cap.release()