import qrcode
from PIL import Image
import cv2
from pyzbar.pyzbar import decode
import numpy as np

def generate_qr_code(data, file_path="qrcode.png", size=8, border=2):
    """
    Génère un QR code à partir des données fournies et l'enregistre dans un fichier image.
    
    :param data: Données à encoder dans le QR code.
    :param file_path: Chemin de sauvegarde du fichier image.
    :param size: Taille de chaque boîte du QR code.
    :param border: Bordure autour du QR code.
    :return: True si réussi, False sinon.
    """
    try:
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=size,
            border=border,
        )
        qr.add_data(data)
        qr.make(fit=True)

        img = qr.make_image(fill_color="black", back_color="white").convert('RGB')
        img.save(file_path)
        return True
    except Exception as e:
        print(f"Erreur lors de la génération du QR code : {e}")
        return False

def read_qr_code_from_image(image_path):
    """
    Lit un QR code à partir d'une image et renvoie les données décodées.
    
    :param image_path: Chemin de l'image contenant le QR code.
    :return: Données décodées ou None si échec.
    """
    try:
        img = cv2.imread(image_path)
        if img is None:
            raise FileNotFoundError(f"L'image n'a pas pu être chargée : {image_path}")

        # Convertir l’image en niveaux de gris (pyzbar fonctionne mieux avec du grayscale)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        decoded_objects = decode(gray)
        if decoded_objects:
            return decoded_objects[0].data.decode('utf-8')
        else:
            return None
    except Exception as e:
        print(f"Erreur lors de la lecture du QR code depuis l'image : {e}")
        return None
