import cv2
import numpy as np
import controller
import requests


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
camera_matrix = np.array([[1.21863664e+03, 0.00000000e+00, 3.89606385e+02],[0.00000000e+00, 1.21604236e+03, 2.91523582e+02],[0.00000000e+00, 0.00000000e+00, 1.00000000e+00]])  # Exemple pour une caméra standard
dist_coeffs = np.array([[ 4.87005446e-01,  2.76682195e+00, -2.63558181e-03,  1.36492998e-02,-2.23536210e+00,  3.54899770e-01,  2.75318659e+00,  2.11062607e+00,0.00000000e+00,  0.00000000e+00,  0.00000000e+00,  0.00000000e+00,0.00000000e+00,  0.00000000e+00]])  # Aucun coefficient de distorsion, à remplacer si besoin
markerSizeInM = 0.02
#Données de base
m=-0.30241622381224764
b=169.53351615676857
# Ouvrir la caméra (ou spécifier un fichier vidéo)
cap = cv2.VideoCapture(0)  # Utilisez '0' pour la caméra par défaut, ou un chemin vers un fichier vidéo
    # Lire une image de la caméra ou de la vidéo

def distance(corners,num):
    if len(corners)>=1:
        #moyhaut=(np.abs(corners[0][0][0][1]-corners[0][0][3][1])+np.abs(corners[0][0][1][1]-corners[0][0][2][1]))/2 ancienne manière de calculer la distance
        #dist=m*moyhaut + b same
        rvec , tvec, _ = cv2.aruco.estimatePoseSingleMarkers(corners, markerSizeInM, camera_matrix, dist_coeffs)
        return(100*tvec[num][0][2])  #J'ai inversé num et 0      
    return(500)

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
    dist=distance(corners)
    id=arucodetect(corners,ids,aruco)
    print(dist)
    return(id,dist)

def distancesingle(corners):
    if len(corners)>=1:
        #moyhaut=(np.abs(corners[0][0][0][1]-corners[0][0][3][1])+np.abs(corners[0][0][1][1]-corners[0][0][2][1]))/2 ancienne manière de calculer la distance
        #dist=m*moyhaut + b same
        rvec , tvec, _ = cv2.aruco.estimatePoseSingleMarkers(corners, 2, camera_matrix, dist_coeffs)
        return(tvec[0][0][2])        
        return(dist)
    return(500)

def detection():
    cap = cv2.VideoCapture(0)
    ret,frame=cap.read()
    gray=cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    corners,ids,rejectedImgPoints = cv2.aruco.detectMarkers(gray, aruco_dict, parameters=parameters)
    if len(corners) > 0:
        dista=distancesingle(corners)
        indexa=0
        for i in range(len(corners)):
            if distance(corners,i)<dista:
                dista=distance(corners,i)
                indexa=i
        print("Nouveau aruco détecté : ",ids[indexa][0])
        return ids[indexa][0], dista

    return 500, 500


cap.release()