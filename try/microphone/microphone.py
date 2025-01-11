import usb.core
import usb.util
import numpy as np

# Le VENDOR_ID et le PRODUCT_ID du microphone Philips utilisé
VENDOR_ID = 0x046d 
PRODUCT_ID = 0x0a4d 
print("Recherche du microphone...")
dev = usb.core.find(idVendor=VENDOR_ID, idProduct=PRODUCT_ID)

if dev is None:
    raise ValueError("Microphone non trouvé...")

# Si nécéssaire (Une des raisons de l'erreur Ressource Busy) 
if dev.is_kernel_driver_active(0):
    try:
        dev.detach_kernel_driver(0)
        print("Kernel driver detached.")
    except usb.core.USBError as e:
        raise RuntimeError(f"Impossible de détacher le pilote du noyau : {str(e)}")

# Configurer la configuration active (nécessaire pour certains dispositifs pour commencer la communication)
dev.set_configuration()

# Définit l'interface et l'endpoint du microphone (le Microphone n'ayant qu'une prise jack, nous avons utilisé un adaptateur jack/USB d'un casque Logitech. 
interface_number = 1 
endpoint_address = 0x82 

# Saisie de l'interface
usb.util.claim_interface(dev, interface_number)

# Ouverture d'un fichier texte
log_file_name = "Micrologs.txt"
print(f"Début de la capture des données répertoriées dans le fichier {log_file_name}.")
with open(log_file_name, "w") as log_file:
    try:
        while True:
            # Lecture des données
            data = dev.read(endpoint_address, 1024, timeout=1000)
            # On le convertit en tableau numpy 
            audio_data = np.array(data)
            
            # Écriture des données dans le fichier (avec un séparateur).
            log_file.write(" ".join(map(str, audio_data)) + "\n")
            log_file.write("------\n")
            log_file.flush()  # On s'ssure que les données sont bien écrites
            
            print(f"Capture des {len(audio_data)} échantillons.")
    except KeyboardInterrupt:
        print("Arrêt de la capture")
    except usb.core.USBError as e:
        print(f"Erreur USB : {e}")

# On relâche l'interface 
usb.util.release_interface(dev, interface_number)
print("Interface relanchée avec succes")
