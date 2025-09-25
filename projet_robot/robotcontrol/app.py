#! /usr/bin/env python3

import controller
import time
from math import*
import camapp
import requests
import epreuve3

pos=[25,-25,0,0]

def check_move(c: controller.Controller, left, right,dist,pos):
    nbtick=(dist*8900)/50
    c.standby()
    c.get_encoder_ticks()
    speed = [left, right]
    c.set_raw_motor_speed(*speed)
    ticks = list(c.get_encoder_ticks())
    x, y,ori=pos[0],pos[1],pos[2]
    t=time.time()
    if right > 0 and left > 0 :    #avancer
        while (ticks[0] or ticks[1]) <= nbtick:
            temp = list(c.get_encoder_ticks())
            ticks[0], ticks[1] = ticks[0] + temp[0], ticks[1] + temp[1]
            if ticks[0] >= ticks[1]:
                speed[0] = 40
                speed[1] = 41
                c.set_raw_motor_speed(speed[0], speed[1])
            if ticks[1] > ticks[0]:
                speed[1] = 40
                speed[0] = 41
                c.set_raw_motor_speed(speed[0], speed[1])
            diff=time.time()-t
            if diff>1:
                diff=0
                t=time.time()
                if ori==0:
                    y+=8
                elif ori==2:
                    y-=8
                elif ori==1:
                    x+=8
                elif ori==3:
                    x-=8
                requests.post('http://proj103.r2.enst.fr/api/pos?x='+str(x)+'&y='+str(y))
        c.standby()
    elif right < 0 and left < 0 :   #reculer
        while (ticks[0] or ticks[1] )>= -nbtick:
            temp = list(c.get_encoder_ticks())
            ticks[0], ticks[1] = ticks[0] + temp[0], ticks[1] + temp[1]
            if ticks[0] >= ticks[1]:
                speed[0] = -41
                speed[1] = -40
                c.set_raw_motor_speed(speed[0], speed[1])
            if ticks[1] > ticks[0]:
                speed[1] = -41
                speed[0] = -40
                c.set_raw_motor_speed(speed[0], speed[1])
            diff=time.time()-t
            if diff>1:
                diff=0
                t=time.time()
                if ori==0:
                    y-=8
                elif ori==2:
                    y+=8
                elif ori==1:
                    x-=8
                elif ori==3:
                    x+=8
                requests.post('http://proj103.r2.enst.fr/api/pos?x='+str(x)+'&y='+str(y))
        c.standby()
    elif left< 0 and right>0:    #tourner à gauche
        while (ticks[0]>=-1850 or ticks[1] <=1850):
            temp = list(c.get_encoder_ticks())
            ticks[0], ticks[1] = ticks[0] + temp[0], ticks[1] + temp[1]
            c.set_raw_motor_speed(speed[0], speed[1])
        time.sleep(0.07)
        c.standby()
        ori=(ori-1)%4
    else:   #tourner à droite
        while (ticks[0]<=1850 or ticks[1] >=-1850):
            temp = list(c.get_encoder_ticks())
            ticks[0], ticks[1] = ticks[0] + temp[0], ticks[1] + temp[1]
            c.set_raw_motor_speed(speed[0], speed[1])
        time.sleep(0.07)
        c.standby()
        ori=(ori+1)%4
    return [x,y,ori,pos[3]]

def tourner_10(c: controller.Controller, left, right):
    c.standby()
    c.get_encoder_ticks()
    speed = [left, right]
    c.set_raw_motor_speed(*speed)
    ticks = list(c.get_encoder_ticks())
    if right > 0 and left <0:
        while (ticks[0]>=-20 or ticks[1]<=20):
            temp = list(c.get_encoder_ticks())
            ticks[0], ticks[1] = ticks[0] + temp[0], ticks[1] + temp[1]
            c.set_raw_motor_speed(speed[0], speed[1])
        time.sleep(0.07)
        c.standby()
    else:
        while (ticks[0]<=20 or ticks[1]>=-20):
            temp = list(c.get_encoder_ticks())
            ticks[0], ticks[1] = ticks[0] + temp[0], ticks[1] + temp[1]
            c.set_raw_motor_speed(speed[0], speed[1])
        time.sleep(0.07)
        c.standby()

def tourner_45(c: controller.Controller, left, right,pos):
    ori,demi_ori=pos[2],pos[3]
    c.standby()
    c.get_encoder_ticks()
    speed = [left, right]
    c.set_raw_motor_speed(*speed)
    ticks = list(c.get_encoder_ticks())
    if left< 0 and right>0:    #gauche
        while (ticks[0]>=-950 or ticks[1] <=950):
            temp = list(c.get_encoder_ticks())
            ticks[0], ticks[1] = ticks[0] + temp[0], ticks[1] + temp[1]
            c.set_raw_motor_speed(speed[0], speed[1])
        demi_ori-=1
        if demi_ori==-2:
            ori=(ori-1)%4
            demi_ori=0
        time.sleep(0.07)
        c.standby()
    else:    #droite
        while (ticks[0]<=1200 or ticks[1] >=-1200):
            temp = list(c.get_encoder_ticks())
            ticks[0], ticks[1] = ticks[0] + temp[0], ticks[1] + temp[1]
            c.set_raw_motor_speed(speed[0], speed[1])
        demi_ori+=1
        if demi_ori==2:
            ori=(ori+1)%4
            demi_ori=0
        time.sleep(0.07)
        c.standby()
    return [pos[0],pos[1],ori,demi_ori]

def tourner_x_degre(c: controller.Controller, deg):
    c.standby()
    nbticks=abs((850*deg)/45)
    c.get_encoder_ticks()
    ticks = list(c.get_encoder_ticks())
    if deg<0:    #gauche
        print(ticks,nbticks)
        speed=[-40,40]
        c.set_raw_motor_speed(*speed)
        while (ticks[0]>=-nbticks or ticks[1]<=nbticks):
            print(ticks)
            temp = list(c.get_encoder_ticks())
            ticks[0], ticks[1] = ticks[0] + temp[0], ticks[1] + temp[1]
            c.set_raw_motor_speed(speed[0], speed[1])
        time.sleep(0.07)
        c.standby()
    else:     #droite
        speed=[40,-40]
        c.set_raw_motor_speed(*speed)
        while (ticks[0]<=nbticks or ticks[1]>=-nbticks):
            temp = list(c.get_encoder_ticks())
            ticks[0], ticks[1] = ticks[0] + temp[0], ticks[1] + temp[1]
            c.set_raw_motor_speed(speed[0], speed[1])
        time.sleep(0.07)
        c.standby()


def automatique_x_y(c: controller.Controller, row, col):
    c.standby()
    l = ["F","E","D","C","B","A",""]
    i = -1
    x,y=75,-25
    ori, demi_ori = 0, 0
    pos=[x,y,ori,demi_ori]
    while(l[i] != row):
         print(row,col,i)
         pos=check_move(c, 30, 30,50,pos)
         i = i+1
         time.sleep(0.5)
    if col == 1:
        pos=check_move(c, -30, 30,50,pos)
        time.sleep(0.5)
        pos=check_move(c, 30, 30,50,pos)
        time.sleep(0.5)
        tour_complet_robot(c)
    elif col == 3:
        pos=check_move(c, 30, -30,50,pos)
        time.sleep(0.5)
        pos=check_move(c, 30, 30,50,pos)
        time.sleep(0.5)
        tour_complet_robot(c)
    else:
        tour_complet_robot(c)
        requests.post('http://proj103.r2.enst.fr/api/marker?id=5&col='+str(col)+'&row='+str(row))

def tour_complet_robot(c: controller.Controller):
    c.standby()
    c.get_encoder_ticks()
    speed = [-40, 40]
    c.set_raw_motor_speed(*speed)
    ticks = list(c.get_encoder_ticks())
    while (ticks[0]>=-8050 or ticks[1] <=8050):
         temp = list(c.get_encoder_ticks())
         ticks[0], ticks[1] = ticks[0] + temp[0], ticks[1] + temp[1]
         c.set_raw_motor_speed(speed[0], speed[1])
    time.sleep(0.07)
    c.standby()


def bolzano(aruco,pos):
    ide,distan=camapp.detect(aruco)
    if ide!=500: #aruco non detecte
        if ide!=0 and distan<50:
            aruco=camapp.captureflag(aruco,ide)
            row,col=round(y)//50,round(x)//50
            lettre=["F","E","D","C","B","A"]
            row_lettre=lettre[row]
            requests.post('http://proj103.r2.enst.fr/api/marker?id='+str(ide)+'&col='+str(col)+'&row='+str(row))
            return True
    return False


def check_procedure(i,user_value,pos):
    c = controller.Controller()
    c.standby()
    if i == 0:
        pos=check_move(c, 30, 30,user_value,pos)
    elif i == 1:
        pos=check_move(c, -30, -30,user_value,pos)
    elif i == 2:
        pos=check_move(c, -30, 30, 0,pos)
    elif i == 3:
        pos=check_move(c, 30, -30, 0,pos)


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
    pos=[0,0,0,0]
    check_procedure(0,5,pos)
    return jsonify({"message": "Avancer : commande exécutée avec succès"})

@app.route('/arriere')
def move_backward():
    pos=[0,0,0,0]
    check_procedure(1,5,pos)
    return jsonify({"message": "Reculer : commande exécutée avec succès"})

@app.route('/gauche')
def turn_left():
    pos=[0,0,0,0]
    check_procedure(2,0,pos)
    return jsonify({"message": "Tourner à gauche : commande exécutée avec succès"})

@app.route('/droite')
def turn_right():
    pos=[0,0,0,0]
    check_procedure(3,0,pos)
    return jsonify({"message": "Tourner à droite : commande exécutée avec succès"})

@app.route('/tour')
def tour_complet():
    c = controller.Controller()
    tour_complet_robot(c)
    return jsonify({"message": "Tour complet : commande exécutée avec succès"})

@app.route('/tourner_peu_droite')
def tourner_droite():
    c = controller.Controller()
    tourner_10(c, 30, -30)
    return jsonify({"message": "Tourner un peu à droite : commande exécutée avec succès"})

@app.route('/tourner_peu_gauche')
def tourner_gauche():
    c = controller.Controller()
    tourner_10(c, -30, 30)
    return jsonify({"message": "Tourner un peu à gauche : commande exécutée avec succès"})

@app.route('/automatique_cord', methods=['POST'])
def automatique_cord():
    row = request.form.get('x')
    col = request.form.get('y')
    if not (row.isalpha() and row.isupper()):
        return jsonify({"error": "Erreur : X doit être une lettre majuscule."}), 400
    if not col.isdigit():
        return jsonify({"error": "Erreur : Y doit être un numéro."}), 400
    col = int(col)
    c = controller.Controller()
    automatique_x_y(c, row, col)
    return jsonify({"message": f"Commande exécutée avec succès pour {row} et {col}"})

@app.route('/capture_automatique')
def automatique():
    c = controller.Controller()
    epreuve3.automatique_parcours(c)
    return jsonify({"message": "Parcours automatique : commande exécutée avec succès"})

@app.route('/x_degre', methods=['POST'])
def x_degre():
    deg = request.form.get('deg')
    deg = int(deg)
    c = controller.Controller()
    tourner_x_degre(c,deg)
    return jsonify({"message": f"Commande exécutée avec succès pour {deg}"})

@app.route('/x_cm', methods=['POST'])
def x_cm():
    cm = request.form.get('cm')
    cm = int(cm)
    c = controller.Controller()
    pos=[0,0,0,0]
    pos=check_move(c,30,30,cm,pos)
    return jsonify({"message": f"Commande exécutée avec succès pour {cm}"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=7777)