# 🚲 Vélib Data -- CloudDataM2

Application web de visualisation et d'analyse des données **Vélib'** à
Paris, avec intégration des **zones ZFE** et d'un **historique de
relevés** stocké dans MongoDB.\
Développé en **Flask** et conteneurisé avec **Docker Compose**.

------------------------------------------------------------------------

## 🌍 Objectif

L'application permet de : - Visualiser en temps réel les **stations
Vélib'** sur une carte interactive. - Afficher les **zones à faibles
émissions (ZFE)** en overlay. - Consulter les **données historiques**
des stations grâce à MongoDB. - Mettre à jour et historiser les relevés
sans écraser les précédents. - Fournir une base pour l'analyse de la
mobilité urbaine.

------------------------------------------------------------------------

## 🧠 Stack technique

  Composant              Description
  ---------------------- --------------------------------------------------------
  **Flask**              Framework web Python servant l'API et les pages HTML
  **MongoDB**            Base NoSQL pour stocker les relevés Vélib (historique)
  **Leaflet.js**         Librairie JavaScript pour la carte interactive
  **Docker Compose**     Orchestration du backend Flask + MongoDB
  **HTML / CSS / JS**    Interface utilisateur et carte interactive
  **Open Data Vélib'**   Source de données en temps réel

------------------------------------------------------------------------

## 🗂️ Structure du projet

    CloudDataM2/
    │
    ├── app.py                     # Point d’entrée Flask
    ├── requirements.txt            # Dépendances Python
    ├── docker-compose.yml          # Stack Flask + MongoDB
    │
    ├── templates/                  # Pages HTML (Jinja2)
    │   ├── base.html
    │   ├── index.html
    │   ├── map.html
    │   └── zfe.html
    │
    ├── static/                     # Fichiers statiques
    │   ├── style.css
    │   └── scripts.js
    │
    ├── data/                       # (Optionnel) dumps JSON/CSV des relevés
    └── README.md

------------------------------------------------------------------------

## ⚙️ Installation et exécution

### 1. Cloner le projet

``` bash
git clone https://github.com/LilRaphh/CloudDataM2.git
cd CloudDataM2
```

### 2. Lancer avec Docker

``` bash
docker compose up -d
```

### 3. Accéder à l'application

-   Interface : <http://localhost:5000>
-   Mongo Express (si configuré) : <http://localhost:8081>

------------------------------------------------------------------------

## 🧾 Fonctionnalités principales

✅ **Carte interactive** :\
Affiche les stations Vélib' avec statut (vélos disponibles, bornes
libres, etc.).

✅ **Overlay ZFE** :\
Superposition dynamique des zones à faibles émissions de Paris.

✅ **Historisation MongoDB** :\
Les relevés sont enregistrés sans écrasement, avec horodatage
automatique.

✅ **Filtrage et mises à jour** :\
Actualisation manuelle ou automatique des données via le script Python.

------------------------------------------------------------------------

## 🧩 Exemple de logique d'historisation

Chaque exécution du script insère les nouveaux relevés :

``` python
existing = collection.find_one({"station_id": station_id})
if not existing or existing["last_update"] != new_data["last_update"]:
    collection.insert_one(new_data)
```

Ainsi, les anciennes valeurs sont conservées pour analyses temporelles.

------------------------------------------------------------------------

## 🧰 Technologies utilisées

  Type               Outils
  ------------------ ----------------------------------
  Backend            Flask, Requests
  Base de données    MongoDB
  Frontend           HTML5, CSS3, JavaScript, Leaflet
  Conteneurisation   Docker, Docker Compose
  Données            OpenData Paris -- Vélib', ZFE

------------------------------------------------------------------------

## 🧑‍💻 Auteur

**Raphaël COLNOT**\
*M2 Big Data & Intelligence Artificielle -- Projet CloudDataM2*

------------------------------------------------------------------------

## 📄 Licence

Projet libre sous licence MIT.
