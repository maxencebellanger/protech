import cv2
import sys

def try_capture(index):
    cap = cv2.VideoCapture(index)
    if cap.isOpened():
        print(f"Camera {index} ouverte avec succes")
        return cap
    else:
        print(f"Echec de l'ouverture de la Camera {index} ")
        return None

def main():
    # Pour tester les differentes cameras connectés a WSL
    for index in range(10):  # Essayer les indices de 0 a 9
        cap = try_capture(index)
        if cap is not None:
            break
    
    if cap is None:
        print("Aucune camera n'a été trouvée")
        return

    # Récupérer les propriétés de la camera
    width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
    height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
    fps = cap.get(cv2.CAP_PROP_FPS)
    print(f"Propriétés de la camera: {width}x{height} @ {fps}fps")

    while True:
        # Enregistrer les frames dans un fichier video
        ret, frame = cap.read()

        if not ret:
            print("Impossible de recevoir la frame (fin du stream ?). Sortie.")
            break

        # Montrer les frames
        cv2.imshow('frame', frame)
        if cv2.waitKey(1) == ord('q'):
            break

    # Lorsque tout est terminé, libérer la camer
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    print(f"Version d'OpenCV: {cv2.__version__}")
    print(f"Version de Python: {sys.version}")
    main()