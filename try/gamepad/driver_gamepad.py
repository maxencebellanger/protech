import subprocess
import usb.core
import usb.util
import time
import os
import matplotlib.pyplot as plt
import numpy as np
import time
from math import cos, sin, radians
from draw import * 


def interpret_angle(valueX, valueY):
    if valueX>127:
        valueX = ((valueX - 128)/127) - 1 
    elif valueX == 0:
        pass
    else:
        valueX = 1 - (127-valueX)/127

    if valueY>127:
        valueY = ((valueY - 128)/127) - 1 
    elif valueY == 0:
        pass
    else:
        valueY = 1 - (127 - valueY)/127

    return(valueX, valueY)

# Real-time joystick plotting
def plot_joystick_with_calibration(dev, endpoint):
    """
    Plots joystick position in real-time with proper calibration for corners.
    """
    plt.ion()
    fig, ax = plt.subplots()
    
    ax.set_xlim(-1, 1)
    ax.set_ylim(-1, 1)
    ax.grid(True)
    ax.set_title("Joystick Position with Calibration")
    ax.set_xlabel("X-axis")
    ax.set_ylabel("Y-axis")

    # Plot
    point, = ax.plot([], [], 'ro')

    while True:
        try:
            # Read joystick data
            raw_data = dev.read(endpoint.bEndpointAddress, endpoint.wMaxPacketSize)
            print(raw_data)
            data = raw_data[10:14]
            X_angle, Y_angle = interpret_angle(data[1],data[3])

            # Update plot
            point.set_data(X_angle, Y_angle)
            plt.draw()
            plt.pause(0.00001)

        except Exception as e:
            print(f"Error reading joystick data: {e}")
            plt.pause(0.1)  # Retry delay

    

def main():



    # Trouver la manette USB (périphérique HID)
    dev = usb.core.find(idVendor=0x2f24, idProduct=0x00b7)  # Exemple : Manette EasySMX

    if dev is None:
        raise ValueError("Manette non trouvée. Assurez-vous qu'elle est connectée.")

    # Vérifier si le pilote du noyau est actif sur l'interface 0 et le détacher
    if dev.is_kernel_driver_active(0):
        try:
            dev.detach_kernel_driver(0)
            print("Pilote du noyau détaché")
        except usb.core.USBError as e:
            raise RuntimeError(f"Impossible de détacher le pilote du noyau : {str(e)}")

    # Définir la configuration active (certains périphériques en ont besoin pour commencer la communication)
    dev.set_configuration()

    # Obtenir le premier point de terminaison
    cfg = dev.get_active_configuration()
    interface = cfg[(0, 0)]

    # Les périphériques HID USB ont généralement au moins un point de terminaison IN
    endpoint = usb.util.find_descriptor(
        interface,
        custom_match=lambda e: usb.util.endpoint_direction(e.bEndpointAddress) == usb.util.ENDPOINT_IN
    )

    if endpoint is None:
        raise ValueError("Point de terminaison non trouvé.")
    
    drawturtle(dev, endpoint)

    # Boucle principale pour lire les données de la manette
    print("Lecture des données de la manette... (appuyez sur Ctrl+C pour arrêter)")
    try:
        while True:
            try:
                print("----------")
                # Lire les données depuis le point de terminaison
                data = dev.read(endpoint.bEndpointAddress, endpoint.wMaxPacketSize)
                print(data)
                # Analyser les données (rapport HID brut)
                print(data[4])
                if not (data[4] == 0):
                    print(f"La gachette LT est enfoncé avec un niveau de {data[4]}/255")
                if not (data[5] == 0):
                    print(f"La gachette RT est enfoncé avec un niveau de {data[5]}/255")



                boutons = bin(data[3]+ 256)
                if boutons[3] == '1': 
                    print("Le bouton Y est enfoncé")
                if boutons[4] == '1':
                    print("Le bouton X est enfoncé")
                if boutons[5] == '1':
                    print("Le bouton B est enfoncé")
                if boutons[6] == '1':
                    print("Le bouton A est enfoncé")
                if boutons[8] == '1':
                    print("Le bouton Home est enfoncé")
                if boutons[9] == '1':
                    print("Le bouton RB est enfoncé")
                if boutons[10] == '1':
                    print("Le bouton LB est enfoncé")

                croix = bin(data[2]+ 256)
                if croix[3] == '1': 
                    print("Le bouton du joystick droit est enfoncé")
                if croix[4] == '1': 
                    print("Le bouton du joystick gauche est enfoncé")
                if croix[5] == '1': 
                    print("Le bouton back est enfoncé")
                if croix[6] == '1': 
                    print("Le bouton start est enfoncé")
                if croix[7] == '1': 
                    print("Le bouton → est enfoncé")
                if croix[8] == '1':
                    print("Le bouton ← est enfoncé")
                if croix[9] == '1':
                    print("Le bouton ↓ est enfoncé")
                if croix[10] == '1':
                    print("Le bouton ↑ est enfoncé")

                X_raw = data[7]
                Y_raw = data[9]
                print(X_raw)
                print(Y_raw)


            except usb.core.USBError as e:
                if e.errno == 110:  # Erreur de délai d'attente (aucune donnée reçue)
                    continue
                else:
                    raise e
    except KeyboardInterrupt:
        print("\nSortie...")

    # Libérer le périphérique et rattacher le pilote du noyau
    usb.util.dispose_resources(dev)
    try:
        dev.attach_kernel_driver(0)
        print("Pilote du noyau rattacher")
    except usb.core.USBError as e:
        print(f"Impossible de rattacher le pilote du noyau : {str(e)}")

if __name__ == "__main__":
    main()


