import cv2
import requests 

from src.config import base_url

def send_image(file):

    #http://13.48.57.180
    url = base_url + "/detect/upload/image"  # URL de l'API pour envoyer le fichier
    file_path= "temp.mp4"
    try:
        files = {'file': file}
        response = requests.post(url, files=files)  # Envoie la requête POST avec le contenu du fichier 
        return response.json()  # Renvoie la réponse du serveur (si nécessaire)

    except requests.exceptions.RequestException as e:
        print("Erreur lors de l'envoi du fichier :", e)



def send_video(uploaded_file):
    """Envoie directement la vidéo à l'API Flask."""
    url = base_url  +"/detect/upload/video"  # URL de l'API Flask
    try:
        # Prépare le fichier pour l'envoi
        files = {'file': (uploaded_file.name, uploaded_file.read(), uploaded_file.type)}
        
        # Effectue la requête POST avec le fichier
        response = requests.post(url, files=files)

        # Vérifie la réponse
        if response.status_code == 200:
            # print("Le résultat"*10)
            # print(response.json())
            return response.json()
        else:
            print(f"Erreur: {response.status_code}, {response.text}")
            return None
    except requests.exceptions.RequestException as e:
        print("Erreur lors de l'envoi du fichier :", e)
        return None





def download_video_from_url(url, save_path):
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()

        with open(save_path, 'wb') as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)
            return True
        print(f"La vidéo a été téléchargée avec succès : {save_path}")
    except requests.exceptions.RequestException as e:
        print(f"Une erreur est survenue lors du téléchargement : {e}")
        return False


def convert_frame_to_png(frame):
    _, encoded_frame = cv2.imencode(".png", frame)
    return encoded_frame.tobytes()