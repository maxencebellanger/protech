import usb.core
import usb.util

def list_usb_devices():
    devices = usb.core.find(find_all=True)
    if not devices:
        print("Aucun dispositif USB trouvé.")
    else:
        for device in devices:
            print(f"Device: {device.idVendor:04x}:{device.idProduct:04x}")

def main():
    # Lister tous les dispositifs USB
    print("Dispositifs USB disponibles:")
    list_usb_devices()

    # Essayer de trouver votre webcam spécifique
    dev = usb.core.find(idVendor=0x322e, idProduct=0x202c) # ID de la webcam trouvé avec lsusb

    if dev is None:
        raise ValueError('Dispositif non trouvé')

    print(f"Dispositif trouvé: {dev.idVendor:04x}:{dev.idProduct:04x}")

    dev.set_configuration()

    cfg = dev.get_active_configuration()
    print(f"Configuration active: {cfg}")

    for intf in cfg:
        print(f"Interface: {intf.bInterfaceNumber}")
        for ep in intf:
            print(f"  Endpoint: {ep.bEndpointAddress:02x}, "
                  f"Direction: {'OUT' if usb.util.endpoint_direction(ep.bEndpointAddress) == usb.util.ENDPOINT_OUT else 'IN'}")

    intf = cfg[(0,0)]

    ep = usb.util.find_descriptor(
        intf,
        custom_match = lambda e: 
            usb.util.endpoint_direction(e.bEndpointAddress) == 
            usb.util.ENDPOINT_OUT)

    if ep is None:
        print("Impossible de trouver l'endpoint OUT")
    else:
        # Ecriture des données
        try:
            ep.write(b'test')
            print("Données écrites avec succès")
        except usb.core.USBError as e:
            print(f"Echec de l'écriture des données: {str(e)}")

if __name__ == "__main__":
    main()