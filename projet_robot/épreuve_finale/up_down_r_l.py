#! /usr/bin/env python3

import controller
import time
from math import*
import camapp
import requests
import final_naif


x,y,dire=75,-25,0
row_start,col_start="Z",1
def position():
    return x,y,dire
def case():
    return row_start,col_start


#appel : mouvement(c,distance en cm ou angle en degré si angle=True, rien si c'est pour avancer ou True si c'est pour un angle, rien si vitesse=40 sinon changer comme on veut
#ex : mouvement(c, -90,True) tournant à gauche de 90°
#ex : mouvement(c,-50) reculer de 50cm
def mouvement(c: controller.Controller,dist,angle=False,vit = 40):
    global x,y,dire
    nbtick=abs((dist*8900)/50)
    c.standby()
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
                speed[0] = sens*40
                speed[1] = sens*41
                c.set_raw_motor_speed(speed[0], speed[1])
            if ticks[1] > ticks[0]:
                speed[1] = sens*40
                speed[0] = sens*41
                c.set_raw_motor_speed(speed[0], speed[1])
            diff=time.time()-t
            if diff>1:
                diff=0
                t=time.time()
                if dire==0:
                    y=y+sens*12.5
                elif dire==180:
                    y=y-sens*12.5
                elif dire==90:
                    x=x+sens*12.5
                elif dire==270:
                    x=x-sens*12.5
                requests.post('http://proj103.r2.enst.fr/api/pos?x='+str(x)+'&y='+str(y))
        c.standby()

    else:    #tourner
        if abs(dist)==90:
            nbtick=1770
        elif abs(dist)==45:
            nbtick=700
        elif abs(dist)==360:
            nbtick=7850
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
    requests.post('http://proj103.r2.enst.fr/api/pos?x='+str(x)+'&y='+str(y))
    return jsonify({"message": f"Commande exécutée avec succès pour {col}"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=4444)
