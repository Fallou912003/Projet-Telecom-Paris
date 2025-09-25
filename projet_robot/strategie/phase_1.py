#! /usr/bin/env python3

import controller
import time
from math import*
import camapp
import requests
import cv2
import json

x,y,dire=75,-25,0
def position():
    return x,y,dire


#appel : mouvement(c,distance en cm ou angle en degré si angle=True, rien si c'est pour avancer ou True si c'est pour un angle, rien si vitesse=40 sinon changer comme on veut
#ex : mouvement(c, -90,True) tournant à gauche de 90°
#ex : mouvement(c,-50) reculer de 50cm
def mouvement(c: controller.Controller,dist,angle=False,vit = 30):
    global x,y,dire
    nbtick=abs((dist*9500)/50)
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
                speed[1] = sens*33
                c.set_raw_motor_speed(speed[0], speed[1])
            if ticks[1] > ticks[0]:
                speed[1] = sens*30
                speed[0] = sens*33
                c.set_raw_motor_speed(speed[0], speed[1])
            diff=time.time()-t
            if diff>1:
                diff=0
                t=time.time()
                if dire==0:
                    y=y+sens*10
                elif dire==180:
                    y=y-sens*10
                elif dire==90:
                    x=x+sens*10
                elif dire==270:
                    x=x-sens*10
                requests.post('http://proj103.r2.enst.fr/api/pos?x='+str(x)+'&y='+str(y))
        c.standby()

    else:    #tourner
        if abs(dist)==90:
            nbtick=1850
        elif abs(dist)==45:
            nbtick=800
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


def strategie_phase_1(c:controller.Controller):
    arucos_captures=[]
    aruco_simple = {}
    aruco=[]
    aruco_dict = cv2.aruco.Dictionary_get(cv2.aruco.DICT_6X6_50)
    parameters = cv2.aruco.DetectorParameters_create()
    ref=[1,2,3,4]
    global x,y
    nb_captures = 0
    for i in range(7):
        mouvement(c,45,True)
        time.sleep(0.5)
        id, dist = camapp.detect(aruco)
        x_aruco, y_aruco = approximation(x,y,"SW")
        row, col = x_aruco//50, y_aruco//50
        if dist < 50:
            if id != 0 and id != 500:
                if nb_captures < 2:
                    nb_captures += 1 
                    aruco_simple = {"x" : x_aruco,"y" : y_aruco,"dir" : "SW","marker_id" : id,"captured" : True}
                    arucos_captures.append(aruco_simple)
                    requests.post('http://proj103.r2.enst.fr/api/marker?id='+str(id)+'&col='+str(col)+'&row='+str(row))
                    print("je suis la")
                    mouvement(c,360,True)
                    time.sleep(0.5)
                else:
                    aruco_simple = {"x" : x_aruco,"y" : y_aruco,"dir" : "SW","marker_id" : id,"captured" : False}
                    arucos_captures.append(aruco_simple)
                    requests.post('http://proj103.r2.enst.fr/api/marker?id='+str(id)+'&col='+str(col)+'&row='+str(row)+'&scan=1')
            if id == 0:
                aruco_simple = {"x" : x_aruco,"y" : y_aruco,"dir" : "SW","marker_id" : id,"captured" : False}
                arucos_captures.append(aruco_simple)

        mouvement(c,-90,True)
        time.sleep(0.5)

        id, dist = camapp.detect(aruco)
        x_aruco, y_aruco = approximation(x,y,"SE")
        row, col = x_aruco//50, y_aruco//50
        if dist < 50:
            if id != 0 and id != 500:
                if nb_captures < 2:
                    aruco_simple = {"x" : x_aruco,"y" : y_aruco,"dir" : "SE","marker_id" : id,"captured" : True}
                    arucos_captures.append(aruco_simple)
                    requests.post('http://proj103.r2.enst.fr/api/marker?id='+str(id)+'&col='+str(col)+'&row='+str(row))
                    mouvement(c,360,True)
                    time.sleep(0.5)
                else:
                    aruco_simple = {"x" : x_aruco,"y" : y_aruco,"dir" : "SE","marker_id" : id,"captured" : False}
                    arucos_captures.append(aruco_simple)
                    requests.post('http://proj103.r2.enst.fr/api/marker?id='+str(id)+'&col='+str(col)+'&row='+str(row)+'&scan=1')
            if id == 0:
                aruco_simple = {"x" : x_aruco,"y" : y_aruco,"dir" : "SE","marker_id" : id,"captured" : False}
                arucos_captures.append(aruco_simple)
        
        mouvement(c,45,True)
        time.sleep(0.5)
        mouvement(c,50)
        time.sleep(0.5)

    response = requests.post("http://proj103.r2.enst.fr/api/udta?idx=1", data=json.dumps(arucos_captures))
    print("je suis la")
    print(response.status_code)
    print(response.content)

from flask import Flask, render_template,request,jsonify
import RPi.GPIO as GPIO

app = Flask(__name__)

# Configurer les broches GPIO ici
GPIO.setmode(GPIO.BCM)

@app.route('/')
def index():
    return render_template('index.html')

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

@app.route('/strategie')
def strategie():
    c = controller.Controller()
    strategie_phase_1(c)
    return jsonify({"message": "Tourner un peu à gauche : commande exécutée avec succès"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5555)