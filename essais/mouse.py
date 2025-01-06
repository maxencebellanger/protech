import usb.core
import usb.util
import sys

# Trouver la souris USB (dispositif HID)
dev = usb.core.find(idVendor=0x3923, idProduct=0x76c6)  # Souris USB Logitech (exemple)

if dev is None:
    raise ValueError("Souris non trouvée. Assurez-vous qu'elle est connectée.")

# Vérifier si le pilote du noyau est actif sur l'interface 0 et le détacher si nécessaire
if dev.is_kernel_driver_active(0):
    try:
        dev.detach_kernel_driver(0)  # Détacher le pilote du noyau
        print("Pilote du noyau détaché")
    except usb.core.USBError as e:
        raise RuntimeError(f"Impossible de détacher le pilote du noyau : {str(e)}")

# Configurer la configuration active (nécessaire pour certains dispositifs pour commencer la communication)
dev.set_configuration()

# Obtenir le premier point de terminaison (endpoint)
cfg = dev.get_active_configuration()
interface = cfg[(0, 0)]  # Sélectionner l'interface 0, configuration 0

print(interface)


### Les dispositifs USB HID ont généralement au moins un point de terminaison IN (réception)
##endpoint = usb.util.find_descriptor(
##    interface,
##    custom_match=lambda e: usb.util.endpoint_direction(e.bEndpointAddress) == usb.util.ENDPOINT_IN  # Chercher un point IN
##)
##
##if endpoint is None:
##    raise ValueError("Point de terminaison non trouvé.")

# Boucle principale pour lire les données de la souris
print("Lecture des données de la souris... (appuyez sur Ctrl+C pour arrêter)")
try:
    while True:
        try:
            for endpoint in interface:
                print("Adresse de l'endpoint : ", endpoint.bEndpointAddress)

                # Lire les données à partir du point de terminaison
                data = dev.read(endpoint.bEndpointAddress, endpoint.wMaxPacketSize)  # Lire les paquets de données HID
                # Analyser les données (rapport brut HID)
                print(f"Données brutes : {data}")
        except usb.core.USBError as e:
            if e.errno == 110:  # Erreur de timeout (aucune donnée reçue)
                continue  # Continuer à attendre les données
            else:
                raise e  # Remonter d'autres erreurs USB
except KeyboardInterrupt:
    print("\nFermeture du programme...")

# Libérer le dispositif et rattacher le pilote du noyau
usb.util.dispose_resources(dev)
try:
    dev.attach_kernel_driver(0)  # Rattacher le pilote du noyau pour que la souris fonctionne à nouveau
    print("Pilote du noyau rattaché")
except usb.core.USBError as e:
    print(f"Impossible de rattacher le pilote du noyau : {str(e)}")
