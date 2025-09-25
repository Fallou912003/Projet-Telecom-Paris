import numpy as np
import cv2
import camapp
import controller 
import time
import app
from scipy.optimize import minimize

reper = [1,2,3,4] #ids des aruco repères

def triangulate_position_robust(A, B, C, d1, d2, d3):
    """
    Triangule la position d'un point P dans un plan 2D en minimisant les erreurs
    avec des distances imparfaites.

    Arguments :
    - A, B, C : Coordonnées des points fixes sous forme (x, y)
    - d1, d2, d3 : Distances respectives de P à A, B et C

    Retourne :
    - (x, y) : Coordonnées estimées du point P
    """

    # Coordonnées des points fixes
    x1, y1 = A
    x2, y2 = B
    x3, y3 = C

    # Fonction de coût : somme des erreurs quadratiques entre distances observées et calculées
    def cost_function(P):
        x, y = P
        error1 = (np.sqrt((x - x1)**2 + (y - y1)**2) - d1)**2
        error2 = (np.sqrt((x - x2)**2 + (y - y2)**2) - d2)**2
        error3 = (np.sqrt((x - x3)**2 + (y - y3)**2) - d3)**2
        return error1 + error2 + error3

    # Point initial pour l'optimisation (barycentre des trois points)
    initial_guess = np.mean([A, B, C], axis=0)

    # Résolution du problème d'optimisation
    result = minimize(cost_function, initial_guess, method='BFGS')

    # Vérification du succès de l'optimisation
    if result.success:
        return result.x[0], result.x[1]  # Coordonnées estimées
    else:
        raise RuntimeError("L'optimisation a échoué : " + result.message)

# Exemple d'utilisation
A1 = (0, 350)  # Repère fixe 1
B2 = (150, 350)  # Repère fixe 2
C3 = (150, 0)  # Repère fixe 3
D4 = (0,0) # Repère fixe 4
Posbalise=(A1,B2,C3,D4) # Affectation des coordonnées des balises à un tuple

#x, y = triangulate_position_robust(A, B, C, d1, d2, d3)
def triangularisation():
    i = 0
    d=[500,500,500,500]
    app.tourner_45(50,-50)
    for k in range(4):
        time.sleep(0.5)
        app.turn_left()
        time.sleep(0.5)
        cap = cv2.VideoCapture(0)
        ret, frame = cap.read()
        corners, ids, rejectedImgPoints = cv2.aruco.detectMarkers(gray, aruco_dict, parameters=parameters)
        if len(corners)>0:
            for id in ids:
                if id in reper and if d[id-1]==500:
                    d[id-1]=camapp.distance(corners,id)
    app.tourner_45(-50,50)
    a = []
    for l in range(4):
        if d[l]!=500:
            a.append(l)
    if len(a)>2:
        x,y= triangulate_position_robust(Posbalise[a[0]],Posbalise[a[1]],Posbalise[a[2]],d[a[0]],d[a[1]],d[a[2]])
        print("Coordonnées estimées :(",x,",",y,")")
        return(x,y)
    else:
        return(500,500) # Retourne une valeur par défaut si pas assez de aruco repères détectés pour triangulariser la position