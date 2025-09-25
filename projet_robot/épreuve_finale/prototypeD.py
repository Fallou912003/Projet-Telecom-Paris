import time
import cv2
import numpy as np
from math import*
import requests
import controller
import json

c=controller.Controller()
x,y,dire=175,25,0


def position():
    return x,y,dire


#appel : mouvement(c,distance en cm ou angle en degré si angle=True, rien si c'est pour avancer ou True si c'est pour un angle, rien si vitesse=40 sinon changer comme on veut
#ex : mouvement(c, -90,True) tournant à gauche de 90°
#ex : mouvement(c,-50) reculer de 50cm
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
            nbtick=1915
        elif abs(dist)==45:
            nbtick=850
        elif abs(dist)==360:
            nbtick=8035
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


from flask import Flask, render_template,request,jsonify
import RPi.GPIO as GPIO
'''
app = Flask(__name__)

# Configurer les broches GPIO ici
GPIO.setmode(GPIO.BCM)

@app.route('/')
def index():
    return render_template('index2.html')

# Exemple d'endpoint pour contrôler le robot
@app.route('/avant')
def move_forward():
    c = controller.Controller()
    mouvement(c,50)
    return jsonify({"message": "Avancer : commande exécutée avec succès"})

@app.route('/arriere')
def move_backward():
    c = controller.Controller()
    mouvement(c,-50)
    return jsonify({"message": "Reculer : commande exécutée avec succès"})

@app.route('/gauche')
def turn_left():
    c = controller.Controller()
    mouvement(c,-90,True)
    return jsonify({"message": "Tourner à gauche : commande exécutée avec succès"})

@app.route('/droite')
def turn_right():
    c = controller.Controller()
    mouvement(c,90,True)
    return jsonify({"message": "Tourner à droite : commande exécutée avec succès"})

@app.route('/tour')
def tour_complet():
    c = controller.Controller()
    #mouvement(c,360,True)
    final_naif.parcours_final(c)
    print(x,y,ori,demi_ori)
    return jsonify({"message": "Tour complet : commande exécutée avec succès"})

@app.route('/tourner_peu_droite')
def tourner_droite():
    c = controller.Controller()
    mouvement(c,10,True)
    return jsonify({"message": "Tourner un peu à droite : commande exécutée avec succès"})

@app.route('/tourner_peu_gauche')
def tourner_gauche():
    c = controller.Controller()
    mouvement(c,-10,True)
    return jsonify({"message": "Tourner un peu à gauche : commande exécutée avec succès"})

@app.route('/x_degre', methods=['POST'])
def x_degre():
    deg = request.form.get('deg')
    deg = int(deg)
    c = controller.Controller()
    mouvement(c,deg,True)
    return jsonify({"message": f"Commande exécutée avec succès pour {deg}"})

@app.route('/x_cm', methods=['POST'])
def x_cm():
    cm = request.form.get('cm')
    cm = int(cm)
    c = controller.Controller()
    mouvement(c,cm)
    return jsonify({"message": f"Commande exécutée avec succès pour {cm}"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=4444)
'''
############## Partie du code stratégie finale

aruco_dict = cv2.aruco.Dictionary_get(cv2.aruco.DICT_6X6_50)
parameters = cv2.aruco.DetectorParameters_create()
camera_matrix = np.array([[1.21863664e+03, 0.00000000e+00, 3.89606385e+02],[0.00000000e+00, 1.21604236e+03, 2.91523582e+02],[0.00000000e+00, 0.00000000e+00, 1.00000000e+00]])  # Exemple pour une caméra standard
dist_coeffs = np.array([[ 4.87005446e-01,  2.76682195e+00, -2.63558181e-03,  1.36492998e-02,-2.23536210e+00,  3.54899770e-01,  2.75318659e+00,  2.11062607e+00,0.00000000e+00,  0.00000000e+00,  0.00000000e+00,  0.00000000e+00,0.00000000e+00,  0.00000000e+00]])  # Aucun coefficient de distorsion, à remplacer si besoin
markerSizeInM = 0.02

#1 c'est nord-ouest, 2 c'est nord-est, 3 sud-est, 4 sud-ouest

#Donc le robot doit check les deux premiers corners nord-ouest et nord-est
#Si il détecte un aruco, il le capture. Si il détecte un 0, il le sauvegarde en mémoire.
#Il avance, il regarde encore nord-est et nord-ouest et capture si il le faut. 

liste_arucos = []
capturecounter = 0
#Contient la position
#Etape 1 : Regarde nord-ouest et nord-est et

#Fonction qui permet de capturer un drapeau une fois que le robot est lock-in place
#!!! Nécessité de traiter les cas où c'est des 0

'''
cap = cv2.VideoCapture(0)
ret,frame=cap.read()
if not ret:
    print(ret)
cap.release()

'''
def captureflag(): #Besoin de la position, juste liste des flags
    cap = cv2.VideoCapture(0)
    global x,y,dire,capturecounter
    ret,frame=cap.read()
    if not ret:
        return("Error")
    gray=cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    corners,ids,rejectedImgPoints = cv2.aruco.detectMarkers(gray, aruco_dict, parameters=parameters)
    captured=False
    if len(corners) > 0:
        dista=distancesingle(corners)
        if ids[0][0] not in [liste_arucos[i]["marker_id"] for i in range(len(liste_arucos))] and capturecounter < 2 and dista<50 and ids[0][0]!=0 : #Regarde si l'aruco n'est pas déjà dans la liste des aruco, et capture si jamais bien <50 
            captured = True
            capturecounter +=1
            mouvement(c,360,True) #Danser oui
        posx,posy = correct_aruco_position(x,y,dire,dista) #Il faut possiblement faire l'inverse de la direction dépendamment de si dir est la direction où regarde le robot
        if captured==True:
            row,col=posy//50,posx//50
            lettre=["F","E","D","C","B","A"]
            row_lettre=lettre[row]
            requests.post('http://proj103.r2.enst.fr/api/marker?id='+str(ids[0][0])+'&col='+str(col)+'&row='+str(row))
        liste_arucos.append({"x" : posx,"y" : posy,"dir" : orientationaruco2(dire),"marker_id" : ids[0][0],"captured" : captured}) #L'orientation est en angles
    cap.release()

def is0():
    cap = cv2.VideoCapture(0)
    ret,frame=cap.read()
    if not ret:
        print("Error")
    gray=cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    corners,ids,rejectedImgPoints = cv2.aruco.detectMarkers(gray, aruco_dict, parameters=parameters)
    if len(corners) >0:
        if ids[0][0]==0 and distancesingle(corners)<50:
            return True
    return False

def scandevant2():
    cap = cv2.VideoCapture(0)
    ret,frame=cap.read()
    if not ret:
        print("wtf")
    gray=cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    corners,ids,rejectedImgPoints = cv2.aruco.detectMarkers(gray, aruco_dict, parameters=parameters)
    arucodetect=[]
    print(corners)
    print(ids)
    if len(corners) > 0:
        rvecs, tvecs, _ = cv2.aruco.estimatePoseSingleMarkers(corners, markerSizeInM, camera_matrix, dist_coeffs)
        print(tvecs)
        for i in range(len(ids)):
            if ids[i] not in [[1],[2],[3],[4]] and distancesingle(corners[i]):
                arucodetect.append(distance(corners,i))
    arucodetect=np.sort(arucodetect)
    cap.release()
    return(arucodetect)

def scandevant3():
    cap = cv2.VideoCapture(0)
    listecorners=[]
    listeids=[]
    for i in range(200):
        ret,frame=cap.read()
        gray=cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        corners,ids,rejectedImgPoints = cv2.aruco.detectMarkers(gray, aruco_dict, parameters=parameters)
        if len(corners) > 0:
            listecorners.append(corners)
            listeids.append(ids)
    maxi=0
    id=-1
    arucodetect=[]
    for i in range(len(listeids)):
        if len(listeids[i])>=maxi:
            id=i
    if id==-1:
        return arucodetect
    corners=listecorners[id]
    ids=listeids[id]
    if len(corners) > 0:
        rvecs, tvecs, _ = cv2.aruco.estimatePoseSingleMarkers(corners, markerSizeInM, camera_matrix, dist_coeffs)
        for i in range(len(ids)):
            if ids[i] not in [[1],[2],[3],[4]] and distancesingle(corners[i]):
                arucodetect.append(distance(corners,i))
    arucodetect=np.sort(arucodetect)
    cap.release()
    print(arucodetect)
    return arucodetect





#Fonction qui retourne la position d'un aruco
def correct_aruco_position(robot_x, robot_y, robot_orientation, detected_distance):
    """
    Corrige la position approximative de l'ArUco en la plaçant précisément sur la grille.

    :param robot_x: Position x du robot (en cm)
    :param robot_y: Position y du robot (en cm)
    :param robot_orientation: Orientation du robot ('nord-est', 'nord-ouest', 'sud-est', 'sud-ouest')
    :param detected_distance: Distance détectée approximative de l'ArUco (en cm)
    :return: Tuple (x_corrigé, y_corrigé) de la position corrigée de l'ArUco
    """
    # Calcule la position approximative de l'ArUco
    aruco_x = robot_x + detected_distance * np.cos(np.radians(robot_orientation))
    aruco_y = robot_y + detected_distance * np.sin(np.radians(robot_orientation))

    # Corrige la position en alignant sur la grille de 50 cm x 50 cm
    corrected_x = round(aruco_x / 50) * 50
    corrected_y = round(aruco_y / 50) * 50

    return corrected_x, corrected_y

def strategiemouv():
    mouvement(c,-45,True)
    captureflag() #Pour scanner la balise à gauche
    mouvement(c,90,True)
    captureflag() #Pour scanner la balise à droite
    while y < 250:
        L=scandevant()
        if L==[]:
            mouvement(c,100,False)
        elif L!=[]:
            if L[0]<100: #79
                mouvement(c,50,False)
                time.sleep(0.5)
                mouvement(c,45,True)
                captureflag() #Ajouter une ligne pour le cas où c'est un 0
                mouvement(c,-90,True)
                captureflag() #Encore une fois ajouter une ligne pour le cas où c'est un 0
                mouvement(c,45,True)
            elif L[0]<150: #127
                mouvement(c,50,False)
                time.sleep(0.5)
                mouvement(c,45,True)
                captureflag() #Ajouter une ligne pour le cas où c'est un 0
                mouvement(c,-90,True)
                captureflag() #Encore une fois ajouter une ligne pour le cas où c'est un 0
                mouvement(c,45,True)
            else:
                mouvement(c,100,False)
    mouvemeent(c,50,False)
    response = requests.post("http://proj103.r2.enst.fr/api/udta?idx=1", data=json.dumps(liste_arucos))
    print(response.status_code)
    print(response.content)
#Potentiellement le faire avancer un peu quoi
def strategiemouv2():
    f1=0
    f2=0
    L1=scandevant2()
    mouvement(c,-45,True)
    time.sleep(0.5)
    A=is0()
    captureflag()
    mouvement(c,90,True)
    time.sleep(0.5)
    captureflag()
    B=is0()
    mouvement(c,-45,True)
    time.sleep(0.5)
    if len(L1)>0:
        if L1[0]<150:
            f1=1
    mouvement(c,50)
    time.sleep(0.5)
    L2=scandevant2()
    mouvement(c,-45,True)
    time.sleep(0.5)
    captureflag()
    C=is0()
    mouvement(c,90,True)
    time.sleep(0.5)
    captureflag()
    D=is0()
    if A==True and B==True:
        mouvement(c,90,True)
        time.sleep(0.5)
        captureflag()
        mouvement(c,90,True)
        time.sleep(0.5)
        capture(flag)
        mouvement(c,90,True)
        mouvement(c,45,True)
    elif A==True and B==False:
        mouvement(c,90,True)
        time.sleep(0.5)
        mouvement(c,90,True)
        time.sleep(0.5)
        captureflag()
        mouvement(c,90,True)
        mouvement(c,45,True)
        time.sleep(0.5)
    elif A==False and B==True:
        mouvement(c,90,True)
        time.sleep(0.5)
        captureflag()
        mouvement(c,-90,True)
        time.sleep(0.5)
        mouvement(c,-45,True)
        time.sleep(0.5)
    else:
        mouvement(c,-45,True)
        time.sleep(0.5)
    if len(L2)>0:
        if L2[0]<150:
            f2=1
    mouvement(c,50)
    time.sleep(0.5)
    L1=scandevant2()
    A,B = seretournercar0(f1,A,B)
    f1=0
    if len(L1)>0:
        if L1[0]<150:
            f1=1
    mouvement(c,50)
    time.sleep(0.5)
    L2=scandevant2()
    C,D = seretournercar0(f2,C,D)
    f2=0
    if len(L2)>0:
        if L2[0]<150:
            f2=1
    L1=scandevant2()
    A,B = seretournercar0(f1,A,B)
    f1=0
    if len(L1)>0:
        if L1[0]<150:
            f1=1
    mouvement(c,50)
    time.sleep(0.5)
    L2=scandevant2()
    C,D = seretournercar0(f2,C,D)
    f2=0
    if len(L2)>0:
        if L2[0]<150:
            f2=1
    A,B= seretournercar0(f1,A,B)
    f1=0
    mouvement(c,50)
    time.sleep(0.5)
    C,D= seretournercar0(f2,C,D)
    f2=0
    mouvement(c,50)
    time.sleep(0.5)
    response = requests.post("http://proj103.r2.enst.fr/api/udta?idx=1", data=json.dumps(liste_arucos))
    print(response.status_code)
    print(response.content)

#La stratégie consiste à faire reculer le robot au début, et scanner à distance pour éviter de faire des rotations.

def strategiemouv3():
    mouvement(c,-50)
    time.sleep(0.3)
    mouvement(c,-50)
    time.sleep(0.3)
    F=[0,0]
    Leu=[]
    A,B=False,False
    L1=scandevant3()
    mouvement(c,50)
    L2=scandevant3()
    mouvement(c,50)
    Leu.append(L1)
    Leu.append(L2)
    for i in range(7):
        m=i%2
        F[m] = fautscanner(Leu[m])
        Leu[m]=scandevant3()
        A,B = seretournercar0(F[m],A,B)
        mouvement(c,50)
        time.sleep(0.3)
    
    
    


def fautscanner(L):
    if len(L) > 0:
        if L[0]<150:
            return 1
    return 0



def seretournercar0(F,l1,l2):
    if F==1:
        mouvement(c,-45,True)
        time.sleep(0.3)
        captureflag()
        A=is0()
        mouvement(c,90,True)
        time.sleep(0.3)
        captureflag()
        B=is0()
        if l1==True and l2==True:
            mouvement(c,90,True)
            time.sleep(0.3)
            captureflag()
            mouvement(c,90,True)
            time.sleep(0.3)
            capture(flag)
            mouvement(c,90,True)
            time.sleep(0.3)
            mouvement(c,45,True)
            time.sleep(0.3)
        elif l1==True and l2==False:
            mouvement(c,90,True)
            time.sleep(0.3)
            mouvement(c,90,True)
            time.sleep(0.3)
            captureflag()
            mouvement(c,90,True)
            time.sleep(0.3)
            mouvement(c,45,True)
            time.sleep(0.3)
        elif l1==False and l2==True:
            mouvement(c,90,True)
            time.sleep(0.3)
            captureflag()
            mouvement(c,-90,True)
            time.sleep(0.3)
            mouvement(c,-45,True)
            time.sleep(0.3)
        elif l1==False and l2==False:
            mouvement(c,-45,True)
            time.sleep(0.3)
        return A,B
    else:
        if l1==True and l2==True:
            mouvement(c,90,True)
            time.sleep(0.3)
            mouvement(c,45,True)
            time.sleep(0.3)
            captureflag()
            mouvement(c,90,True)
            time.sleep(0.3)
            captureflag()
            mouvement(c,90,True)
            time.sleep(0.3)
            mouvement(c,45,True)
        elif l1==True and l2==False:
            mouvement(c,-90,True)
            time.sleep(0.3)
            mouvement(c,-45,True)
            time.sleep(0.3)
            captureflag()
            mouvement(c,45,True)
            time.sleep(0.3)
            mouvement(c,90,True)
            time.sleep(0.3)
        elif l1==False and l2==True:
            mouvement(c,90,True)
            time.sleep(0.3)
            mouvement(c,45,True)
            time.sleep(0.3)
            captureflag()
            mouvement(c,-45,True)
            time.sleep(0.3)
            mouvement(c,-90,True)
            time.sleep(0.3)
        return False,False


    

#Retourne l'orientation de l'aruco vis-à-vis du robot

def orientationaruco(direction): 
    if direction == 45:
        return(225)
    elif direction == 135:
        return(315)
    elif direction == 225:
        return(45)
    elif direction == 315:
        return(135)

def orientationaruco2(direction):
    if direction == 45:
        return("SO")
    elif direction == 135:
        return("NO")
    elif direction == 225:
        return("NE")
    elif direction == 315:
        return("SE")

#Fonction qui va nous permettre de scanner les aruco à potentiellement détecter, renvoie la distance aux aruco de manière approximative

#Pourquoi je multiplie par 100 ????
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

strategiemouv3()