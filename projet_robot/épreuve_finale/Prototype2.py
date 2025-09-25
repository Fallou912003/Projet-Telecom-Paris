import time
import cv2
import numpy as np
import requests
import controller
import json

c=controller.Controller()
x,y,dire=75,-25,0
row_start,col_start="Z",1

def mouvement(c: controller.Controller,dist,angle=False,vit = 30):
    global x,y,dire
    nbtick=np.abs((dist*9000)/50)
    c.get_encoder_ticks()
    sens=np.copysign(1,dist)
    if not angle:
        speed = [sens*vit,sens*vit]
    else:
        speed = [sens*vit,-sens*vit]
    c.set_raw_motor_speed(*speed)
    ticks = list(c.get_encoder_ticks())
    t=time.time()

    if not angle :    #avancer
        while (np.abs(ticks[0]) or np.abs(ticks[1])) <= nbtick:
            temp = list(c.get_encoder_ticks())
            ticks[0], ticks[1] = np.abs(ticks[0]) + np.abs(temp[0]), np.abs(ticks[1]) + np.abs(temp[1] )
            if ticks[0] >= ticks[1]:
                speed[0] = sens*vit
                speed[1] = sens*(vit+4)
                c.set_raw_motor_speed(speed[0], speed[1])
            if ticks[1] > ticks[0]:
                speed[1] = sens*vit
                speed[0] = sens*(vit+4)
                c.set_raw_motor_speed(speed[0], speed[1])
            diff=time.time()-t
            if diff>1:
                diff=0
                t=time.time()
                if dire==0:
                    y=y+sens*8
                elif dire==180:
                    y=y-sens*8
                elif dire==90:
                    x=x+sens*8
                elif dire==270:
                    x=x-sens*8
                requests.post('http://proj103.r2.enst.fr/api/pos?x='+str(x)+'&y='+str(y))
        c.standby()

    else:    #tourner
        if np.abs(dist)==90:
            nbtick=1875
        elif np.abs(dist)==45:
            nbtick=847
        elif np.abs(dist)==360:
            nbtick=7970
        else:
            nbtick=np.abs((dist*1700)/90)
        while (np.abs(ticks[0])<=nbtick or np.abs(ticks[1]) <=nbtick):
            temp = list(c.get_encoder_ticks())
            ticks[0], ticks[1] = np.abs(ticks[0]) + np.abs(temp[0]), np.abs(ticks[1]) + np.abs(temp[1])
            #if nbtick-ticks[0]<100 and speed[0]>20:
             #   speed = [speed[0]-sens*1,speed[1]+sens*1]
              #  c.set_raw_motor_speed(*speed)
        time.sleep(0.07)
        c.standby()
        dire=(dire+dist)%360
    time.sleep(0.5)

from flask import Flask, render_template,request,jsonify
import RPi.GPIO as GPIO

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
    mouvement(c,360,True)
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

@app.route('/depart', methods=['POST'])
def depart():
    global col_start,row_start,x,y,dire
    col = request.form.get('y')
    row= request.form.get('x')
    if not (row.isalpha() and row.isupper()):
        return jsonify({"error": "Erreur : X doit être une lettre majuscule."}), 400
    if not col.isdigit():
        return jsonify({"error": "Erreur : Y doit être un numéro."}), 400
    col_start,row_start = int(col),row
    lettre=["G","F","E","D","C","B","A","Z"]
    x,y=(col_start-1)*50+25,lettre.index(row_start)*50-25
    return jsonify({"message": f"Commande exécutée avec succès pour {col}"})

@app.route('/strategie')
def strategie():
    c = controller.Controller()
    requests.post('http://proj103.r2.enst.fr/api/start')
    strategiemouv3()
    phase2(c)
    requests.post('http://proj103.r2.enst.fr/api/stop')
    return jsonify({"message": "Tourner un peu à gauche : commande exécutée avec succès"})

@app.route('/strategie_2')
def strategie_2():
    c = controller.Controller()
    phase2(c)
    requests.post('http://proj103.r2.enst.fr/api/stop')
    return jsonify({"message": "Tourner un peu à gauche : commande exécutée avec succès"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=6666)

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
        dista=distance(corners,0)
        indexa=0
        for i in range(len(corners)):
            if distance(corners,i)<dista:
                dista=distance(corners,i)
                indexa=i
        if ids[indexa][0] not in [liste_arucos[i]["marker_id"] for i in range(len(liste_arucos))] and capturecounter < 2 and dista<50 and ids[indexa][0]!=0 : #Regarde si l'aruco n'est pas déjà dans la liste des aruco, et capture si jamais bien <50 
            captured = True
            capturecounter +=1
            mouvement(c,360,True) #Danser oui
            time.sleep(0.3)
        posx,posy = correct_aruco_position(x,y,dire,dista) #Il faut possiblement faire l'inverse de la direction dépendamment de si dir est la direction où regarde le robot
        if captured==True:
            row,col=posy//50,posx//50
            lettre=["F","E","D","C","B","A"]
            row_lettre=lettre[row]
            requests.post('http://proj103.r2.enst.fr/api/marker?id='+str(int(ids[indexa][0]))+'&col='+str(col)+'&row='+str(row))
        liste_arucos.append({"x" : posx,"y" : posy,"dir" : orientationaruco2(dire),"marker_id" : int(ids[indexa][0]),"captured" : captured}) #L'orientation est en angles
    cap.release()

def is0():
    cap = cv2.VideoCapture(0)
    ret,frame=cap.read()
    if not ret:
        print("Error")
    gray=cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    corners,ids,rejectedImgPoints = cv2.aruco.detectMarkers(gray, aruco_dict, parameters=parameters)
    if len(corners) >0:
        if ids[0][0]==0 and distance(corners,0)<50:
            return True
    return False

def scandevant3():
    cap = cv2.VideoCapture(0)
    listecorners=[]
    listeids=[]
    for i in range(150):
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
            if ids[i] not in [[1],[2],[3],[4]] and distance(corners,i):
                arucodetect.append(distance(corners,i))ls
    arucodetect=np.sort(arucodetect)
    cap.release()
    print(arucodetect)
    return arucodetect





#Fonction qui retourne la position d'un aruco
def correct_aruco_position(robot_x, robot_y, robot_orientation, detected_distance):
    # Calcule la position approximative de l'ArUco
    aruco_x = robot_x + detected_distance * np.cos(np.radians(robot_orientation))
    aruco_y = robot_y + detected_distance * np.sin(np.radians(robot_orientation))

    # Corrige la position en alignant sur la grille de 50 cm x 50 cm
    corrected_x = round(aruco_x / 50) * 50
    corrected_y = round(aruco_y / 50) * 50

    return corrected_x, corrected_y


#La stratégie consiste à faire reculer le robot au début, et scanner à distance pour éviter de faire des rotations.

def strategiemouv3():
    requests.post('http://proj103.r2.enst.fr/api/pos?x='+str(x)+'&y='+str(y))
    #go_to("G",1) #A CHANGER ABSOLUMENT AVANT LA PHASE 1 
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
    response = requests.post("http://proj103.r2.enst.fr/api/udta?idx=1", data=json.dumps(liste_arucos))
    print(response.status_code)
    print(response.content)
    
    


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
    return(500)

def go_to(row,col):
    alpha={"Z":7,"A":6,"B":5,"C":4,"D":3,"E":2,"F":1,"G":0}
    delta_y=(alpha[row]-1)*50-y-25
    for i in range(delta_y//50):
        mouvement(c,delta_y)
    delta_x=col*50-x-25
    if delta_x!=0:
        mouvement(c,90,True)
    for i in range(abs(delta_x)):
        mouvement(c,delta_x)
    if delta_x!=0:
        mouvement(c,-90,True)



def phase2(c:controller.Controller):
    response = requests.get("http://proj103.r2.enst.fr/api/udta?idx=2") #vous lisez dans le registre
    if(response.status_code == 200 and response.content != b''):
        data = json.parse(response.content)
        for i in range(len(data["instructions"])):
            # Split the string and add spaces back as separate elements
            res = [part if part.strip() else " " for part in data["instructions"][i].split(" ")]
            if res[0]=="CAPTURE":
                go_to(res[1][:1],int(res[1][1:]))
                mouvement(c,360,True)
                time.sleep(0.3)
                requests.post('http://proj103.r2.enst.fr/api/marker?id='+res[2]+'&col='+res[1][:1]+'&row='+res[1][1:])
            elif res[0]=="CHECK":
                x1=res[1]//50
                x2=x1+1
                y1=res[2]//50
                y2=y1-1
                lettre=["F","E","D","C","B","A"]
                y1,y2=lettre[y1],lettre[y2]
                for j in range(len(res)-3):
                    if res[3+j]=="SW":
                        go_to(x2,y2)
                        mouvement(c,-90,True)
                        time.sleep(0.3)
                        mouvement(c,-45,True)
                        time.sleep(0.3)
                        captureflag()
                        mouvement(c,90,True)
                        time.sleep(0.3)
                        mouvement(c,45,True)
                        time.sleep(0.3)
                    if res[3+j]=="NW":
                        go_to(x2,y1)
                        mouvement(c,-45,True)
                        time.sleep(0.3)
                        captureflag()
                        mouvement(c,45,True)
                        time.sleep(0.3)
                    if res[3+j]=="SE":
                        go_to(x1,y2)
                        mouvement(c,90,True)
                        time.sleep(0.3)
                        mouvement(c,45,True)
                        time.sleep(0.3)
                        captureflag()
                        mouvement(c,-90,True)
                        time.sleep(0.3)
                        mouvement(c,-45,True)
                        time.sleep(0.3)
                    if res[3+j]=="NE":
                        go_to(x1,y1)
                        mouvement(c,45,True)
                        time.sleep(0.3)
                        captureflag()
                        mouvement(c,-45,True)
                        time.sleep(0.3)

    go_to("Z",0)
