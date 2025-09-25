def approximation(x_robot,y_robot,orientation):
    if orientation == 45:
        aruco_x = x_robot + 25
        aruco_y = y_robot + 25
    if orientation == 315:
        aruco_x = x_robot - 25
        aruco_y = y_robot + 25
    if orientation == 225:
        aruco_x = x_robot - 25
        aruco_y = y_robot - 25
    if orientation == 135:
        aruco_x = x_robot + 25
        aruco_y = y_robot - 25
    corrected_x = round(aruco_x / 50) * 50
    corrected_y = round(aruco_y / 50) * 50
    return corrected_x, corrected_y

def alphabet(i):
    if i == 0:
        return "A"
    if i == 1:
        return "B"
    if i == 2:
        return "C"
    if i == 3:
        return "D"
    if i == 4:
        return "E"
    if i == 5:
        return "F"

def strategie_phase_1(c:controller.Controller):
    arucos_captures=[]
    aruco_simple = {}
    aruco=[]
    aruco_dict = cv2.aruco.Dictionary_get(cv2.aruco.DICT_6X6_50)
    parameters = cv2.aruco.DetectorParameters_create()
    ref=[1,2,3,4]
    global x,y,dire
    nb_captures = 0
    non_capture_suivant = False
    for i in range(7):
        mouvement(c,45,True)
        time.sleep(0.5)
        id, dist = camapp.detect(aruco)
        x_aruco, y_aruco = approximation(x,y,dire)
        col, row = x_aruco//50, y_aruco//50
        print(row)
        row = alphabet(row)
        non_capture_courant = False
        if dist < 50:
            if id != 0 and id != 500:
                if nb_captures<2:
                    nb_captures += 1
                    aruco_simple = {"x" : x_aruco,"y" : y_aruco,"dir" : "SW","marker_id" : int(id),"captured" : True}
                    arucos_captures.append(aruco_simple)
                    print(str(int(id)))
                    a = int(id)
                    requests.post('http://proj103.r2.enst.fr/api/marker?id='+str(a)+'&col='+str(col)+'&row='+row)
                    print("je suis la")
                    mouvement(c,360,True)
                    time.sleep(0.5)
                else:
                    aruco_simple = {"x" : x_aruco,"y" : y_aruco,"dir" : "SW","marker_id" : int(id),"captured" : False}
                    arucos_captures.append(aruco_simple)
                    requests.post('http://proj103.r2.enst.fr/api/marker?id='+str(id)+'&col='+str(col)+'&row='+row+'&scan=1')
            if id == 0:
                non_capture_courant = True

        mouvement(c,-90,True)
        time.sleep(0.5)

        id, dist = camapp.detect(aruco)
        x_aruco, y_aruco = approximation(x,y,dire)
        col, row = x_aruco//50, y_aruco//50
        print(row)
        row = alphabet(row)
        if dist < 50:
            if id != 0 and id != 500:
                if nb_captures<2:
                    nb_captures += 1
                    aruco_simple = {"x" : x_aruco,"y" : y_aruco,"dir" : "SE","marker_id" : int(id),"captured" : True}
                    arucos_captures.append(aruco_simple)
                    requests.post('http://proj103.r2.enst.fr/api/marker?id='+str(id)+'&col='+str(col)+'&row='+row)
                    mouvement(c,360,True)
                    time.sleep(0.5)
                else:
                    aruco_simple = {"x" : x_aruco,"y" : y_aruco,"dir" : "SE","marker_id" : int(id),"captured" : False}
                    arucos_captures.append(aruco_simple)
                    requests.post('http://proj103.r2.enst.fr/api/marker?id='+str(id)+'&col='+str(col)+'&row='+row+'&scan=1')
            if id == 0:
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
            id, dist = camapp.detect(aruco)
            x_aruco, y_aruco = approximation(x,y,dire)
            col, row = x_aruco//50, y_aruco//50
            print(row)
            row = alphabet(row)
            if dist < 50:
                if id != 0 and id != 500:
                    if nb_captures<2:
                        nb_captures = nb_captures+1
                        aruco_simple = {"x" : int(x_aruco),"y" : int(y_aruco),"dir" : "NE","marker_id" : int(id),"captured" : True}
                        arucos_captures.append(aruco_simple)
                        #response = requests.post("http://proj103.r2.enst.fr/api/udta?idx=1", data=aruco_simple)
                        requests.post('http://proj103.r2.enst.fr/api/marker?id='+str(id)+'&col='+str(col)+'&row='+row)
                        mouvement(c,360,True)
                        time.sleep(0.5)
                    else:
                        aruco_simple = {"x" : x_aruco,"y" : y_aruco,"dir" : "NE","marker_id" : int(id),"captured" : False}
                        arucos_captures.append(aruco_simple)
                        requests.post('http://proj103.r2.enst.fr/api/marker?id='+str(id)+'&col='+str(col)+'&row='+row+'&scan=1')
                if id == 0:
                    aruco_simple = {"x" : x_aruco,"y" : y_aruco,"dir" : "NE","marker_id" : int(id),"captured" : False}
                    arucos_captures.append(aruco_simple)

            mouvement(c,-90,True)
            time.sleep(0.5)

            id, dist = camapp.detect(aruco)
            x_aruco, y_aruco = approximation(x,y,dire)
            col, row = x_aruco//50, y_aruco//50
            print(row)
            row = alphabet(row)
            if dist < 50:
                if id != 0 and id != 500:
                    if nb_captures<2:
                        nb_captures=nb_captures+1
                        aruco_simple = {"x" : x_aruco,"y" : y_aruco,"dir" : "NW","marker_id" : int(id),"captured" : True}
                        arucos_captures.append(aruco_simple)
                        requests.post('http://proj103.r2.enst.fr/api/marker?id='+str(id)+'&col='+str(col)+'&row='+row)
                        mouvement(c,360,True)
                        time.sleep(0.5)
                    else:
                        aruco_simple = {"x" : x_aruco,"y" : y_aruco,"dir" : "NW","marker_id" : int(id),"captured" : False}
                        arucos_captures.append(aruco_simple)
                        requests.post('http://proj103.r2.enst.fr/api/marker?id='+str(id)+'&col='+str(col)+'&row='+row+'&scan=1')
                if id == 0:
                    aruco_simple = {"x" : x_aruco,"y" : y_aruco,"dir" : "NW","marker_id" : int(id),"captured" : False}
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
        time.sleep(0.5)

    print(arucos_captures)
    response = requests.post("http://proj103.r2.enst.fr/api/udta?idx=1", data=json.dumps(arucos_captures))
    print(response.status_code)
    print(response.content)
