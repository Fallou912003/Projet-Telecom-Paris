import math

def correct_aruco_position(robot_x, robot_y, robot_orientation, detected_distance):
    """
    Corrige la position approximative de l'ArUco en la plaçant précisément sur la grille.

    :param robot_x: Position x du robot (en cm)
    :param robot_y: Position y du robot (en cm)
    :param robot_orientation: Orientation du robot ('nord-est', 'nord-ouest', 'sud-est', 'sud-ouest')
    :param detected_distance: Distance détectée approximative de l'ArUco (en cm)
    :return: Tuple (x_corrigé, y_corrigé) de la position corrigée de l'ArUco
    """
    # Détermine l'angle de l'orientation du robot
    if robot_orientation == 'nord-est':
        angle = math.radians(45)
    elif robot_orientation == 'nord-ouest':
        angle = math.radians(135)
    elif robot_orientation == 'sud-ouest':
        angle = math.radians(225)
    elif robot_orientation == 'sud-est':
        angle = math.radians(315)
    else:
        raise ValueError("Orientation invalide. Les orientations valides sont : 'nord-est', 'nord-ouest', 'sud-est', 'sud-ouest'.")

    # Calcule la position approximative de l'ArUco
    aruco_x = robot_x + detected_distance * math.cos(angle)
    aruco_y = robot_y + detected_distance * math.sin(angle)

    # Corrige la position en alignant sur la grille de 50 cm x 50 cm
    corrected_x = round(aruco_x / 50) * 50
    corrected_y = round(aruco_y / 50) * 50

    return corrected_x, corrected_y

# Exemple d'utilisation
robot_x = 100  # Position x du robot
robot_y = 150  # Position y du robot
robot_orientation = 'nord-est'  # Orientation du robot
detected_distance = 47.9  # Distance détectée approximative

corrected_position = correct_aruco_position(robot_x, robot_y, robot_orientation, detected_distance)
print("Position corrigée de l'ArUco :", corrected_position)
