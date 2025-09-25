#! /usr/bin/env python3

import controller
import time
from math import*
import camapp
import requests
import cv2
import json

x,y,dire=275,-25,0
row_start,col_start="Z",6
def position():
    return x,y,dire


#appel : mouvement(c,distance en cm ou angle en degré si angle=True, rien si c'est pour avancer ou True si c'est pour un angle, rien si vitesse=40 sinon changer comme on veut
#ex : mouvement(c, -90,True) tournant à gauche de 90°
#ex : mouvement(c,-50) reculer de 50cm
def mouvement(c: controller.Controller,dist,angle=False,vit = 30):
    global x,y,dire
    nbtick=abs((dist*9200)/50)
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
        while (abs(ticks[0]) and abs(ticks[1])) <= nbtick:
            temp = list(c.get_encoder_ticks())
            ticks[0], ticks[1] = abs(ticks[0]) + abs(temp[0]), abs(ticks[1]) + abs(temp[1] )
            if ticks[0] >= ticks[1]:
                speed[0] = sens*25
                speed[1] = sens*31
                c.set_raw_motor_speed(speed[0], speed[1])
            if ticks[1] > ticks[0]:
                speed[1] = sens*25
                speed[0] = sens*30
                c.set_raw_motor_speed(speed[0], speed[1])
            diff=time.time()-t
            if diff>1:
                diff=0
                t=time.time()
                if dire==0:
                    y=y+sens*7.1
                elif dire==180:
                    y=y-sens*7.1
                elif dire==90:
                    x=x+sens*7.1
                elif dire==270:
                    x=x-sens*7.1
                requests.post('http://proj103.r2.enst.fr/api/pos?x='+str(x)+'&y='+str(y))
        #c.set_raw_motor_speed(0,60)
        c.standby()

    else:    #tourner
        if abs(dist)==90:
            nbtick=2000
        elif abs(dist)==45:
            nbtick=900
        elif abs(dist)==360:
            nbtick=8800
        else:
            nbtick=abs((dist*1700)/90)
        while (abs(ticks[0])<=nbtick and abs(ticks[1]) <=nbtick):
            temp = list(c.get_encoder_ticks())
            ticks[0], ticks[1] = abs(ticks[0]) + abs(temp[0]), abs(ticks[1]) + abs(temp[1])
            #if nbtick-ticks[0]<100 and speed[0]>20:
             #   speed = [speed[0]-sens*1,speed[1]+sens*1]
              #  c.set_raw_motor_speed(*speed)
        time.sleep(0.07)
        c.standby()
        dire=(dire+dist)%360
    time.sleep(0.5)


def approximation(x_robot,y_robot,orientation):
    if orientation == "SW":
        aruco_x = x_robot + 25
        aruco_y = y_robot + 25
    if orientation == "SE":
        aruco_x = x_robot - 25
        aruco_y = y_robot + 25
    if orientation == "NE":
        aruco_x = x_robot - 25
        aruco_y = y_robot - 25
    if orientation == "NW":
        aruco_x = x_robot + 25
        aruco_y = y_robot - 25
    corrected_x = round(aruco_x / 50) * 50
    corrected_y = round(aruco_y / 50) * 50
    return corrected_x, corrected_y


def alphabet(i):
    if i == 0:
        return "G"
    if i == 1:
        return "F"
    if i == 2:
        return "E"
    if i == 3:
        return "D"
    if i == 4:
        return "C"
    if i == 5:
        return "B"
    if i == 6:
        return "A"

def strategie_phase_1(c:controller.Controller):
    arucos_captures=[]
    aruco_simple = {}
    aruco=[]
    aruco_dict = cv2.aruco.Dictionary_get(cv2.aruco.DICT_6X6_50)
    parameters = cv2.aruco.DetectorParameters_create()
    ref=[1,2,3,4]
    global x,y
    nb_captures = 0
    non_capture_suivant = False
    case_y = 1
    go_to("G",6)
    for i in range(7):
        mouvement(c,45,True)
        time.sleep(0.5)
        id, dist = camapp.detection()
        x_aruco, y_aruco = approximation(x,y,"SW")
        col, row = x_aruco//50, y_aruco//50
        row = alphabet(case_y)
        non_capture_courant = False
        if dist < 50:
            if id != 0 and id != 500:
                if nb_captures<2: 
                    nb_captures += 1
                    aruco_simple = {"x" : x_aruco,"y" : case_y*50,"dir" : "SW","marker_id" : int(id),"captured" : True}
                    arucos_captures.append(aruco_simple)
                    print(str(int(id)))
                    a = int(id)
                    requests.post('http://proj103.r2.enst.fr/api/marker?id='+str(a)+'&col='+str(col)+'&row='+row)
                    print("je suis la")
                    mouvement(c,360,True)
                    time.sleep(0.5)
                else:
                    aruco_simple = {"x" : x_aruco,"y" : case_y*50,"dir" : "SW","marker_id" : int(id),"captured" : False}
                    arucos_captures.append(aruco_simple)
                    requests.post('http://proj103.r2.enst.fr/api/marker?id='+str(id)+'&col='+str(col)+'&row='+row+'&scan=1')
            if id == 0:
                aruco_simple = {"x" : x_aruco,"y" : case_y*50,"dir" : "SE","marker_id" : int(id),"captured" : False}
                arucos_captures.append(aruco_simple)
                requests.post('http://proj103.r2.enst.fr/api/marker?id='+str(id)+'&col='+str(col)+'&row='+row+'&scan=1')
                non_capture_courant = True

        mouvement(c,-90,True)
        time.sleep(0.5)

        id, dist = camapp.detection()
        x_aruco, y_aruco = approximation(x,y,"SE")
        col, row = x_aruco//50, y_aruco//50
        row = alphabet(case_y)
        if dist < 50:
            if id != 0 and id != 500:
                if nb_captures<2:
                    nb_captures += 1
                    aruco_simple = {"x" : x_aruco,"y" : case_y*50,"dir" : "SE","marker_id" : int(id),"captured" : True}
                    arucos_captures.append(aruco_simple)
                    requests.post('http://proj103.r2.enst.fr/api/marker?id='+str(id)+'&col='+str(col)+'&row='+row)
                    mouvement(c,360,True)
                    time.sleep(0.5)
                else:
                    aruco_simple = {"x" : x_aruco,"y" : case_y*50,"dir" : "SE","marker_id" : int(id),"captured" : False}
                    arucos_captures.append(aruco_simple)
                    requests.post('http://proj103.r2.enst.fr/api/marker?id='+str(id)+'&col='+str(col)+'&row='+row+'&scan=1')
            if id == 0:
                aruco_simple = {"x" : x_aruco,"y" : case_y*50,"dir" : "SE","marker_id" : int(id),"captured" : False}
                arucos_captures.append(aruco_simple)
                non_capture_courant = True
        
        mouvement(c,45,True)
        time.sleep(0.5)


        if non_capture_suivant: #étape où grace à l'aruco 0 détecté on scanne le bas de la case suivante
            mouvement(c,90,True)
            time.sleep(0.2)
            mouvement(c,90,True)
            time.sleep(0.5)
            mouvement(c,45,True)
            time.sleep(0.5)
            id, dist = camapp.detection()
            x_aruco, y_aruco = approximation(x,y,"NE")
            col, row = x_aruco//50, y_aruco//50
            row = alphabet(case_y-1)
            if dist < 50:
                if id != 0 and id != 500:
                    if nb_captures<2: 
                        nb_captures = nb_captures + 1
                        aruco_simple = {"x" : int(x_aruco),"y" : (case_y-1)*50,"dir" : "NE","marker_id" : int(id),"captured" : True}
                        arucos_captures.append(aruco_simple)
                        #response = requests.post("http://proj103.r2.enst.fr/api/udta?idx=1", data=aruco_simple)
                        requests.post('http://proj103.r2.enst.fr/api/marker?id='+str(id)+'&col='+str(col)+'&row='+row)
                        mouvement(c,360,True)
                        time.sleep(0.5)
                    else:
                        aruco_simple = {"x" : x_aruco,"y" : (case_y-1)*50,"dir" : "NE","marker_id" : int(id),"captured" : False}
                        arucos_captures.append(aruco_simple)
                        requests.post('http://proj103.r2.enst.fr/api/marker?id='+str(id)+'&col='+str(col)+'&row='+row+'&scan=1')
                if id == 0:
                    aruco_simple = {"x" : x_aruco,"y" : (case_y-1)*50,"dir" : "NE","marker_id" : int(id),"captured" : False}
                    arucos_captures.append(aruco_simple)

            mouvement(c,-90,True)
            time.sleep(0.5)

            id, dist = camapp.detection()
            x_aruco, y_aruco = approximation(x,y,"NW")
            col, row = x_aruco//50, y_aruco//50
            row = alphabet(case_y-1)
            if dist < 50:
                if id != 0 and id != 500:
                    if nb_captures<2:
                        nb_captures = nb_captures + 1
                        aruco_simple = {"x" : x_aruco,"y" : (case_y-1)*50,"dir" : "NW","marker_id" : int(id),"captured" : True}
                        arucos_captures.append(aruco_simple)
                        requests.post('http://proj103.r2.enst.fr/api/marker?id='+str(id)+'&col='+str(col)+'&row='+row)
                        mouvement(c,360,True)
                        time.sleep(0.5)
                    else:
                        aruco_simple = {"x" : x_aruco,"y" : (case_y-1)*50,"dir" : "NW","marker_id" : int(id),"captured" : False} 
                        arucos_captures.append(aruco_simple)
                        requests.post('http://proj103.r2.enst.fr/api/marker?id='+str(id)+'&col='+str(col)+'&row='+row+'&scan=1')
                if id == 0:
                    aruco_simple = {"x" : x_aruco,"y" : (case_y-1)*50,"dir" : "NW","marker_id" : int(id),"captured" : False}
                    arucos_captures.append(aruco_simple)
            mouvement(c,-45,True)
            time.sleep(0.2)
            mouvement(c,-90,True)
            time.sleep(0.5)
        if non_capture_courant:
            non_capture_suivant = True
        else:
            non_capture_suivant = False


        mouvement(c,50)
        case_y = case_y + 1
        time.sleep(0.5)
        
    print(arucos_captures)
    response = requests.post("http://proj103.r2.enst.fr/api/udta?idx=1", data=json.dumps(arucos_captures))
    print(response.status_code)
    print(response.content)


def go_to(row,col):
    c = controller.Controller()
    alpha={"Z":7,"A":6,"B":5,"C":4,"D":3,"E":2,"F":1,"G":0}
    delta_y=alpha[row]*50-y-25
    for i in range(abs(delta_y)//50):
        mouvement(c,50)
    delta_x=col*50-x-25
    if delta_x!=0:
        mouvement(c,90,True)
    for i in range(abs(delta_x)//50):
        mouvement(c,50)
    if delta_x!=0:
        mouvement(c,-90,True)



def strategie_phase_2(c:controller.Controller):
    aruco = []
    response = requests.get("http://proj103.r2.enst.fr/api/udta?idx=2") #vous lisez dans le registre
    if(response.status_code == 200 and response.content != ''):
        data = json.parse(response.content)
        for i in range(len(data["instructions"])):
            # Split the string and add spaces back as separate elements
            res = [part if part.strip() else " " for part in data["instructions"][i].split(" ")]
            if res[0]=="CAPTURE":
                go_to(res[1][:1],int(res[1][1:]))
                mouvement(c,360,True)
                time.sleep(0.5)
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
                        go_to(y2,x2)
                        mouvement(c,-90,True)
                        time.sleep(0.5)
                        mouvement(c,-45,True)
                        time.sleep(0.5)
                        id, dist = camapp.detection()
                        x_aruco, y_aruco = approximation(x,y,"SW")
                        col, row = x_aruco//50, y_aruco//50
                        row = alphabet(row)
                        if dist < 50:
                            if id != 0 and id != 500:
                                requests.post('http://proj103.r2.enst.fr/api/marker?id='+str(id)+'&col='+str(col)+'&row='+row)
                                mouvement(c,360,True)
                                time.sleep(0.5)
                        mouvement(c,90,True)
                        time.sleep(0.5)
                        mouvement(c,45,True)
                        time.sleep(0.5)
                    if res[3+j]=="NW":
                        go_to(y1,x2)
                        mouvement(c,-45,True)
                        id, dist = camapp.detection()
                        x_aruco, y_aruco = approximation(x,y,"NW")
                        col, row = x_aruco//50, y_aruco//50
                        row = alphabet(row)
                        if dist < 50:
                            if id != 0 and id != 500:
                                requests.post('http://proj103.r2.enst.fr/api/marker?id='+str(id)+'&col='+str(col)+'&row='+row)
                                mouvement(c,360,True)
                                time.sleep(0.5)
                        mouvement(c,45,True)
                    if res[3+j]=="SE":
                        go_to(y2,x1)
                        mouvement(c,90,True)
                        time.sleep(0.5)
                        mouvement(c,45,True)
                        time.sleep(0.5)
                        id, dist = camapp.detection()
                        x_aruco, y_aruco = approximation(x,y,"SE")
                        col, row = x_aruco//50, y_aruco//50
                        row = alphabet(row)
                        if dist < 50:
                            if id != 0 and id != 500:
                                requests.post('http://proj103.r2.enst.fr/api/marker?id='+str(id)+'&col='+str(col)+'&row='+row)
                                mouvement(c,360,True)
                                time.sleep(0.5)
                        mouvement(c,-90,True)
                        time.sleep(0.5)
                        mouvement(c,-45,True)
                        time.sleep(0.5)
                    if res[3+j]=="NE":
                        go_to(y1,x1)
                        mouvement(c,45,True)
                        time.sleep(0.5)
                        id, dist = camapp.detection()
                        x_aruco, y_aruco = approximation(x,y,"NE")
                        col, row = x_aruco//50, y_aruco//50
                        row = alphabet(row)
                        if dist < 50:
                            if id != 0 and id != 500:
                                requests.post('http://proj103.r2.enst.fr/api/marker?id='+str(id)+'&col='+str(col)+'&row='+row)
                                mouvement(c,360,True)
                                time.sleep(0.5)
                        mouvement(c,-45,True)
                        time.sleep(0.5)
    
    go_to("G",0)


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
    requests.post('http://proj103.r2.enst.fr/api/stop')
    time.sleep(1)
    requests.post('http://proj103.r2.enst.fr/api/start')
    strategie_phase_1(c)
    time.sleep(5)
    strategie_phase_2(c)
    requests.post('http://proj103.r2.enst.fr/api/stop')
    return jsonify({"message": "Tourner un peu à gauche : commande exécutée avec succès"})

@app.route('/strategie_2')
def strategie_2():
    c = controller.Controller()
    strategie_phase_2(c)
    requests.post('http://proj103.r2.enst.fr/api/stop')
    return jsonify({"message": "Tourner un peu à gauche : commande exécutée avec succès"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3333)