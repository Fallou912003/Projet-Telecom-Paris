import cv2
import numpy as np

# Charger le dictionnaire ArUco standard (par exemple, DICT_6X6_250)
aruco_dict = cv2.aruco.Dictionary_get(cv2.aruco.DICT_6X6_250)
parameters = cv2.aruco.DetectorParameters_create()

# Ouvrir la caméra (ou spécifier un fichier vidéo)
cap = cv2.VideoCapture(4)  # Utilisez '0' pour la caméra par défaut, ou un chemin vers un fichier vidéo

while True:
    # Lire une image de la caméra ou de la vidéo
    ret, frame = cap.read()
    if not ret:
        break
    
    # Convertir l'image en niveau de gris (les détecteurs ArUco fonctionnent mieux sur des images en niveaux de gris)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    # Détecter les coins des marqueurs ArUco
    corners, ids, rejectedImgPoints = cv2.aruco.detectMarkers(gray, aruco_dict, parameters=parameters)

    # Si des marqueurs sont détectés
    if len(corners) > 0:
        # Dessiner les marqueurs détectés
        frame = cv2.aruco.drawDetectedMarkers(frame, corners, ids)

        # Vous pouvez aussi dessiner des axes ou d'autres informations pour chaque marqueur
        for i in range(len(ids)):
            # Détection des axes 3D pour chaque marqueur (nécessite une calibration de caméra, ici on ne l'utilise pas)
            # Afficher l'ID du marqueur sur l'image
            font = cv2.FONT_HERSHEY_SIMPLEX
            cv2.putText(frame, f"ID: {ids[i][0]}", tuple(corners[i][0][0].astype(int)), font, 0.5, (0, 255, 0), 2)

    # Afficher l'image avec les marqueurs détectés
    cv2.imshow('ArUco Marker Detection', frame)
    
    # Quitter la boucle avec la touche 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Libérer la caméra et fermer les fenêtres OpenCV
cap.release()
cv2.destroyAllWindows()