import cv2
import numpy as np

# Charger le dictionnaire ArUco standard (par exemple, DICT_6X6_250)
aruco_dict = cv2.aruco.Dictionary_get(cv2.aruco.DICT_6X6_50)
parameters = cv2.aruco.DetectorParameters_create()

# Ouvrir la caméra (ou spécifier un fichier vidéo)
cap = cv2.VideoCapture(0)  # Utilisez '0' pour la caméra par défaut, ou un chemin vers un fichier vidéo
markersizecm = 2
    # Lire une image de la caméra ou de la vidéo
ret, frame = cap.read()
    
    # Convertir l'image en niveau de gris (les détecteurs ArUco fonctionnent mieux sur des images en niveaux de gris)
gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    # Détecter les coins des marqueurs ArUco et print la hauteur "moyenne" de l'Aruco detecté
corners, ids, rejectedImgPoints = cv2.aruco.detectMarkers(gray, aruco_dict, parameters=parameters)
print((np.abs(corners[0][0][0][1]-corners[0][0][3][1])+np.abs(corners[0][0][1][1]-corners[0][0][2][1]))/2)
    
    # Afficher l'image avec les marqueurs détectés
    # Quitter la boucle avec la touche 'q'

# Libérer la caméra et fermer les fenêtres OpenCV
cap.release()
cv2.destroyAllWindows()