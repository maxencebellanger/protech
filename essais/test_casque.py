import usb.core
import usb.util

# Trouver le périphérique
dev = usb.core.find(idVendor=0x046d, idProduct=0x0aaa)

if dev is None:
    raise ValueError("Périphérique non trouvé")

# Configurer le périphérique
#dev.set_configuration()

# Accéder à l'interface et au premier endpoint de l'interface 2
interface_number = 1
alternate_setting = 1
interface = dev[0][(interface_number, alternate_setting)]
endpoint = interface[0]

# Détacher le pilote kernel si nécessaire
if dev.is_kernel_driver_active(interface_number):
    dev.detach_kernel_driver(interface_number)
    print("Pilote kernel détaché")

# Réclamer l'interface
usb.util.claim_interface(dev, interface_number)
print("Interface réclamée")

# Lire des données depuis l'endpoint
try:
    data = dev.read(endpoint.bEndpointAddress, endpoint.wMaxPacketSize, timeout=1000)
    print(f"Données lues : {data}")
except usb.core.USBError as e:
    print(f"Erreur lors de la lecture : {e}")

# Libérer l'interface après usage
usb.util.release_interface(dev, interface_number)
print("Interface libérée")
