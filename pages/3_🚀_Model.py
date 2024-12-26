import io
import os
import tempfile
from io import BytesIO
import subprocess

import numpy as np
import pandas as pd

import cv2
import requests
import streamlit as st
from PIL import Image

from src.config import image_path , base_url
from src.utils.upload import download_video_from_url, send_image, send_video
from src.utils.utils import save_csv_file


is_run = True
image_input = Image.new("RGB", (500, 500))# Get image detect
outputs = {} #To get detection coordonnate
nbr = 0 #Number of object detecting
img_url = ""
video_url = "temp.mp4"
is_video = False
video_path = ""
error_message = "Something is rong"
csv_file_url = "" 
input_video_path = "temp_video.mp4"
output_video_path = "converted_video.mp4"

if "image_path" not in st.session_state:
    st.session_state["image_path"] = os.path.join(os.path.dirname(__file__), '2.jpg')

with st.sidebar:
    st.sidebar.image(Image.open(os.path.join(os.getcwd(), "src/testdata/13.jpg")), use_column_width=True, width=st.sidebar.width)

with open(os.path.join(os.getcwd(), "styles/style1.css")) as css_source:
    st.markdown(f"<style>{css_source.read()}</style>", unsafe_allow_html=True)

frame1, frame2, frame3 = st.columns([2, 3, 2])
# Frame1
with frame1:
    st.markdown("<h5 style='text-align:center;'>SAMPLES FROM TEST SET</h5>", unsafe_allow_html=True)
    with st.container():
        col1, col2 = st.columns(2)
        with col1:
            st.image(Image.open(os.path.join(os.getcwd(), "src/testdata/2.jpg")), use_column_width=True,)
        with col2:
            st.image(Image.open(os.path.join(os.getcwd(), "src/testdata/5.jpg")), use_column_width=True)

    with st.container():
        col1, col2 = st.columns(2)
        with col1:
            st.image(Image.open(os.path.join(os.getcwd(), "src/testdata/3.jpg")), use_column_width=True)
        with col2:
            st.image(Image.open(os.path.join(os.getcwd(), "src/testdata/4.jpeg")), use_column_width=True)

        # Text button with yellow text

        if st.button(
                label="Visualize >>",
                key="button1",
                help="Visualize data set",
                on_click=None,
                args=None,
                kwargs=None,
        ):
            # Execute this code when w
            st.write("Button is pressed")

        # Diver to upload video or image
    st.divider()
    # Create another container with a title
    with st.container():
        with st.container():
            st.markdown("<h6 style='text-align:center;'>Drop image/Video file</h6>", unsafe_allow_html=True)
            st.write("<h6 style='text-align:center;color:##EEEEEE;'>or</h6>", unsafe_allow_html=True)
            st.write("<h6 style='text-align:center;'>Paste youtube / image url</h6>", unsafe_allow_html=True)
            # Input text to get the link
            link = st.text_input("", placeholder="Link")

            # Container to upload image or Vide
        with st.container():
            uploaded_file = st.file_uploader("Choose image or Video", type=["jpg", "jpeg", "png", "mp4"])
        
            if uploaded_file is not None:
                st.session_state["image_path"] = ""  # Réinitialise l'état de l'image
                try:
                    if uploaded_file.name.endswith(".mp4"):
                        # Gestion des vidéos
                        is_video = True

                        # Sauvegarde temporaire du fichier uploadé
                        temp_video_path = "temp.mp4"
                        with open(temp_video_path, "wb") as f:
                            f.write(uploaded_file.getbuffer())
                        
                        # Envoi de la vidéo au backend Flask
                        responses = send_video(uploaded_file)

                        # Vérifie la réponse
                        if responses and 'video' in responses:
                            video_url = responses['video']
                            st.success("Processing complete! Downloading video...")

                            # Télécharger la vidéo depuis l'URL
                            response2 = requests.get(video_url)

                            # Sauvegarder la vidéo téléchargée localement
                            with open(input_video_path, 'wb') as file:
                                file.write(response2.content)

                            # Commande FFmpeg pour convertir la vidéo en MP4 avec codec H.264 et AAC
                            command = [
                                "ffmpeg",
                                "-y",
                                "-i", input_video_path,  # Fichier source
                                "-vcodec", "libx264",     # Codec vidéo H.264
                                "-acodec", "aac",         # Codec audio AAC
                                "-strict", "experimental",  # Pour permettre l'utilisation de certains codecs expérimentaux
                                output_video_path        # Fichier de sortie
                            ]
                            
                            # Exécution de la commande FFmpeg
                            subprocess.run(command)

                            # Vérifiez si le fichier de sortie existe et est lisible
                            if os.path.exists(output_video_path):
                                st.write("Vidéo convertie avec succès !")
                                video_url = output_video_path

                        elif 'error' in responses:
                            st.error(f"Server error: {responses['error']}")
                        else:
                            st.error("Unexpected server response.")
                        
                    else:
                        is_video = False

                        responses = send_image(uploaded_file)
                        if responses is None:
                            error_message = "No drone detect in your file "
                        else:
                            outputs = responses["coordinates"]
                            nbr = responses["num_objects"]
                            img_url = responses["image"]

                except Exception as e:
                    error_message = "La vidéo doit être au format MP4. Veuillez charger un fichier valide."
            else:
                if st.session_state["image_path"] != "":
                    pil_image = Image.open(st.session_state["image_path"])
                    image_bytes = io.BytesIO()
                    pil_image.save(image_bytes, format="PNG")
                    image_bytes.seek(0)

                    files = {'file': ('image.png', image_bytes, 'image/png')}
                    response = requests.post(base_url +'/detect/upload/image', files=files)

                    if response is None or response.status_code == 500:
                        error_message = "No drone detect in your file "
                    else:
                        
                        print(response)
                        data = response.json()
                        outputs = data["coordinates"]
                        nbr = data["num_objects"]
                        img_url = data["image"]
                        print(img_url)



        #Dispplay image detecting in second frame
        
# Column 2
with frame2:
    if is_video:

    # Afficher la vidéo depuis le fichier temporaire
        st.video(video_url)
        st.markdown(
    f"""
    <div style="display: flex; align-items: center; font-size: 18px;">
        <span>Télécharger la vidéo :</span>
        <a href="{video_url}" download="processed_video.mp4" style="margin-left: 10px; text-decoration: none;">
            <img src="https://cdn-icons-png.flaticon.com/512/1828/1828817.png" alt="Download Icon" width="24" height="24" style="filter: hue-rotate(90deg);">
        </a>
    </div>
    """,
    unsafe_allow_html=True,
)


    else:
        if img_url == "":
            if st.session_state["image_path"] == os.path.join(os.getcwd(), "src/testdata/11.png"):
                st.image(Image.open(st.session_state["image_path"]), use_column_width=True, width=100)
                #st.write(error_message)
        else:
            print(img_url)
            response = requests.get(img_url)
            response.raise_for_status()
            image = Image.open(BytesIO(response.content))
            st.image(image, use_column_width=True,)
    with st.container():
        lambda_function = lambda x: 's' if x > 1 else ''
        st.write(f"{nbr} drone{lambda_function(nbr)} detecté{lambda_function(nbr)}")

    #Display  image detect coordonnate
    # Column 3
with frame3:
        # Affichage des données scrollables dans la colonne
    with st.expander("Drone coordinates"):

        st.write(outputs)
