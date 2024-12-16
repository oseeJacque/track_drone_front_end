import streamlit as st
import matplotlib.pyplot as plt
import numpy as np


# URL de l'image
image_url = "/home/osee/projects/dronetrack_front_end-master/pages/drone_track1.png"  # Remplacez par l'URL de l'image directe


# Centrage du titre avec HTML
st.markdown("<h1 style='text-align: center;'>Détection et Tracking de Drones dans des Images et Vidéos</h1>", unsafe_allow_html=True)

# Affichage de l'image
st.image(image_url, caption="Image de Détection de Drone", use_column_width=True)

# Centrer "Contexte du Projet"
st.markdown("<h2 style='text-align: center;'>Contexte du Projet</h2>", unsafe_allow_html=True) 

# Création de deux colonnes
col1, col2 = st.columns(2)

with col1:
    st.markdown("""
        **Dans un monde où l'utilisation des drônes connaît une croissance rapide et devient omniprésente dans divers secteurs, leur rôle évolue et varie considérablement selon les contextes d'application. Autrefois utilisés principalement à des fins récréatives, les drônes jouent désormais un rôle crucial dans des domaines aussi variés que la surveillance, l'agriculture, la logistique, et bien plus encore. Cependant, cette expansion soulève aussi de nouvelles préoccupations liées à leur utilisation malveillante.**
        - **Utilisations récréatives** : Les amateurs utilisent les drônes pour capturer des paysages, réaliser des vidéos créatives ou simplement s’amuser.
        - **Applications commerciales** : Les drônes servent dans des secteurs comme l’agriculture (surveillance des cultures), la livraison (transport rapide de colis), et la cartographie.
        - **Menaces potentielles** : Les drônes peuvent également être utilisés à des fins malveillantes, comme la violation de la vie privée, le transport d’objets illicites ou des intrusions dans des zones sécurisées.
    """)

# Texte dans la deuxième colonne
with col2:
    st.markdown("""
        **Face à cette montée en puissance des drônes, il est essentiel de disposer de solutions technologiques avancées pour :**
        - **Détecter la présence de drônes** : Identifier rapidement et avec précision tout drône dans des images ou des vidéos, quelle que soit leur complexité visuelle (environnements urbains, ruraux, ou ciel dégagé).
        - **Suivre leurs trajectoires** : Grâce à une fonctionnalité de tracking, surveiller le déplacement des drônes détectés et anticiper leurs trajectoires pour des actions préventives.
        
        **Objectifs spécifiques :**
        Ce projet se propose d’offrir une solution robuste et précise, répondant aux besoins des :
        - Systèmes de sécurité périmétrique : Surveillance des infrastructures critiques comme les aéroports, les prisons ou les centrales électriques.
        - Organisateurs d’événements sensibles : Protection des rassemblements publics ou privés contre les intrusions non autorisées.
        - Forces de l’ordre : Suivi des activités suspectes impliquant des drônes dans des enquêtes criminelles ou des interventions de sécurité.
    """)

# Ajouter un séparateur
st.markdown("---")

# Titre centré pour "Méthodologie"
st.markdown("<h2 style='text-align: center;'>2. Méthodologie</h2>", unsafe_allow_html=True) 

# 2.1 Détection avec YOLOv11
st.markdown("<h3 >2.1 Détection avec YOLOv11</h3>", unsafe_allow_html=True)

st.write("""
YOLO (You Only Look Once) est une méthode de détection d'objets en temps réel largement utilisée en vision par ordinateur. Elle combine détection et classification en temps réel, offrant ainsi une grande précision et une rapidité remarquable. Nous avons utilisé YOLOv11, une version avancée, pour les raisons suivantes :
- **Architecture optimisée** : blocs CSP (Cross Stage Partial) pour une extraction de caractéristiques améliorée.
- **Ancrage dynamique** : ajustement automatique des boîtes englobantes.
- **Gestion des petits objets** : utile pour détecter des drones de petite taille.

Le modèle a été entraîné sur un jeu de données de 10 000 images annotées, représentant des drones dans divers environnements (urbains, forestiers, etc.).

### Répartition des données :
- 31,55% pour l'entraînement
- 39,06% pour la validation
- 29,36% pour les tests

Cette répartition permet un bon équilibre entre l’entraînement et la validation.
""")

# Affichage du graphique de répartition des données (graphique en secteurs)
labels = ['Entraînement (31.55%)', 'Validation (39.06%)', 'Test (29.36%)']
sizes = [3155, 3906, 2936]
colors = ['#ff9999','#66b3ff','#99ff99']

fig, ax = plt.subplots()
ax.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90, wedgeprops={'edgecolor': 'black'})
ax.axis('equal')  # Pour que le graphique soit un cercle

st.pyplot(fig)

# 2.2 Suivi (Tracking) avec DeepSORT
st.markdown("<h3>2.2 Suivi (Tracking) avec DeepSORT</h3>", unsafe_allow_html=True)

st.write("""
Le suivi des drones détectés a été effectué avec **DeepSORT** (Simple Online and Realtime Tracking), un algorithme permettant de suivre les objets dans des vidéos en temps réel.

### Fonctionnement de DeepSORT :
- **Réidentification (ReID)** : attribution d'un identifiant unique basé sur les caractéristiques visuelles (couleur, texture) pour un suivi précis, même lors des occlusions.
- **Filtre de Kalman** : prédit les positions futures des drones, permettant de gérer les occlusions temporaires.
- **Association de données** : permet d'associer correctement les objets détectés entre les images successives.

### Avantages pour ce projet :
- Suivi simultané de plusieurs drones.
- Gestion des occlusions et déplacements rapides.
- Intégration fluide avec YOLOv11 pour un traitement en temps réel.
""")

# Affichage d'un graphique pour visualiser le suivi (Exemple avec 2 drones suivis)
# Création d'un simple graphique de trajectoire des drones
fig, ax = plt.subplots()
time = np.arange(0, 10, 1)
drone_1_x = np.sin(time) * 10 + 50  # Trajectoire du drone 1
drone_2_x = np.cos(time) * 10 + 50  # Trajectoire du drone 2
drone_1_y = np.cos(time) * 10 + 50
drone_2_y = np.sin(time) * 10 + 50

ax.plot(drone_1_x, drone_1_y, label='Drone 1', color='blue')
ax.plot(drone_2_x, drone_2_y, label='Drone 2', color='red')
ax.set_xlabel("Position X")
ax.set_ylabel("Position Y")
ax.set_title("Suivi des Drones avec DeepSORT")
ax.legend()

st.pyplot(fig) 

# Ajouter un séparateur
st.markdown("---") 
# Titre centré pour "Méthodologie"
st.markdown("<h2 style='text-align: center;'>3. Résultats</h2>", unsafe_allow_html=True) 

st.write("""
Les résultats obtenus démontrent l’efficacité et la précision du modèle pour détecter et suivre les drones dans des images et des vidéos. Cette section présente une analyse détaillée des performances, illustrée par des visualisations clés.
""")

# Titre pour la section "Visualisation des performances"
st.markdown("<h3>3.1 Images d’entraînement </h3>", unsafe_allow_html=True) 
st.write("""
Nous commençons par une présentation des données utilisées pour entraîner et évaluer le modèle.
""")

# Section Matrice de confusion
st.markdown("<h3>1. Matrice de confusion</h3>", unsafe_allow_html=True)

st.write("""
La matrice de confusion illustre les performances du modèle pour classifier correctement les drones. Elle met en évidence le taux de vrais positifs (TP), de faux positifs (FP) et de faux négatifs (FN).

**Interprétation** : Un haut taux de TP (valeurs sur la diagonale principale) reflète une excellente capacité de détection. Les autres valeurs indiquent les erreurs de classification (faux positifs et faux négatifs).
""")

# Créer deux colonnes pour les images
col1, col2 = st.columns(2)

# Affichage de l'image de la matrice de confusion brute dans la première colonne
with col1:
    st.image("/home/osee/projects/dronetrack_front_end-master/pages/confusion_matrix.png", caption="Matrice de confusion", use_column_width=True)

# Affichage de l'image de la matrice de confusion normalisée dans la deuxième colonne
with col2:
    st.image("/home/osee/projects/dronetrack_front_end-master/pages/confusion_matrix.png", caption="Matrice de confusion normalisée", use_column_width=True)


# Conclusion de la section
st.write("""
Les matrices de confusion permettent de visualiser les erreurs de classification, et la version normalisée offre une meilleure compréhension des taux de détection par rapport aux échantillons totaux. L'analyse de ces matrices aide à identifier les points faibles du modèle pour de futures améliorations.
""") 

# Titre centré pour "Courbes de performance"
st.markdown("<h2>2. Courbes F1, Recall (R), et Précision (Pr)</h2>", unsafe_allow_html=True)

# Introduction des courbes
st.write("""
- **Courbe F1** : Elle montre l’équilibre entre précision et rappel pour différents seuils. Une F1 élevée indique que le modèle excelle à minimiser à la fois FP et FN.
- **Courbe Rappel (Recall)** : Illustre la capacité du modèle à détecter tous les drones présents dans les images.
- **Courbe de Précision (Précision)** : Mesure la proportion de vraies détections parmi toutes les détections effectuées.
""")

# Créer trois colonnes pour afficher les courbes
col1, col2, col3 = st.columns(3)

# Affichage de la courbe F1 dans la première colonne
with col1:
    st.image("/home/osee/projects/dronetrack_front_end-master/pages/F1_curve.png", caption="Courbe F1", use_column_width=True)

# Affichage de la courbe Recall dans la deuxième colonne
with col2:
    st.image("/home/osee/projects/dronetrack_front_end-master/pages/R_curve.png", caption="Courbe Recall", use_column_width=True)

# Affichage de la courbe Précision dans la troisième colonne
with col3:
    st.image("/home/osee/projects/dronetrack_front_end-master/pages/P_curve.png", caption="Courbe Précision", use_column_width=True)

# Conclusion de la section
st.write("""
Les courbes F1, Recall et Précision fournissent des informations détaillées sur les performances du modèle. Elles aident à comprendre comment le modèle gère les compromis entre les différents types d'erreurs et son efficacité globale.
""")


# Titre centré pour "Graphiques des batchs"
st.markdown("<h2 style='text-align: center;'>3. Graphiques des Batchs (Train Batch et Validation Batch)</h2>", unsafe_allow_html=True)

# Introduction des graphiques
st.write("""
Ces graphiques montrent les performances du modèle sur les données d’entraînement et de validation au fil des itérations.
Les résultats visuels incluent :
- Les prédictions sur des exemples d’images d’entraînement.
- Les comparaisons entre prédictions et annotations pour valider la cohérence du modèle.
""")

# Créer des colonnes pour afficher les images côte à côte
col1, col2, = st.columns(2)

# Affichage des images dans les 4 colonnes
with col1:
    st.image("/home/osee/projects/dronetrack_front_end-master/pages/train_batch0.jpg", caption="Train Batch 1", use_column_width=True)

with col2:
    st.image("/home/osee/projects/dronetrack_front_end-master/pages/train_batch3960.jpg", caption="Train Batch 2", use_column_width=True)

col3, col4 = st.columns(2)
with col3:
    st.image("/home/osee/projects/dronetrack_front_end-master/pages/val_batch1_pred.jpg", caption="Validation Batch 1", use_column_width=True)

with col4:
    st.image("/home/osee/projects/dronetrack_front_end-master/pages/val_batch2_pred.jpg", caption="Validation Batch 2", use_column_width=True)

# Conclusion de la section
st.write("""
Les graphiques montrent comment les performances du modèle évoluent au fil des itérations sur les données d'entraînement et de validation. Cela permet d'observer la convergence du modèle et d'identifier d'éventuelles zones d'amélioration.
""")

# Titre pour la section "Visualisation des performances"
st.markdown("<h3>3.2 Visualisation des performances</h3>", unsafe_allow_html=True)

# Affichage des résultats de performance avec une visualisation
st.write("""
Les performances du modèle de détection YOLOv11 et de suivi DeepSORT ont été évaluées à l’aide de diverses métriques :
- **Précision** : 91,86 %
- **Rappel** : 90,26 %
- **mAP50** : 93,87 %
- **mAP50-95** : 64,30 %
""")

# Graphique de précision et rappel
fig, ax = plt.subplots()
metrics = ['Précision', 'Rappel', 'mAP50', 'mAP50-95']
values = [91.86, 90.26, 93.87, 64.30]
ax.barh(metrics, values, color=['#66b3ff', '#99ff99', '#ffcc99', '#ff6666'])
ax.set_xlabel('Pourcentage')
ax.set_title('Comparaison des performances du modèle')

st.pyplot(fig)

# Titre pour la visualisation des prédictions
st.write("""
Voici une illustration de la capacité du modèle à détecter et suivre les drones dans des images et vidéos réelles. Le modèle a détecté et suivi plusieurs drones en temps réel dans des environnements variés.
""")

st.write("""
L’analyse des résultats montre que le modèle YOLOv11 associé à DeepSORT est capable de détecter et suivre les drones avec une grande précision, même dans des environnements complexes. La haute précision et le rappel élevé indiquent que le modèle identifie correctement la majorité des drones, tandis que le mAP50 élevé démontre que les prédictions sont proches des véritables positions des drones. Les tests sur différents types d'images ont permis de valider la robustesse du modèle.
""")


# Titre centré pour "Résultats sur usage du modèle"
st.markdown("<h2 style='text-align: center;'>Résultats sur usage du modèle</h2>", unsafe_allow_html=True)

# Créer deux colonnes pour afficher une image et une vidéo côte à côte
col1, col2 = st.columns(2)


st.image("/home/osee/projects/dronetrack_front_end-master/pages/track_drone_in_image.jpg", 
             caption="Illustration de l'usage du modèle", 
             use_column_width=True)
             
st.video("/home/osee/projects/dronetrack_front_end-master/pages/fixed_video.mp4", 
             format="video/mp4")