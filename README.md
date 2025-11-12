# ☁️ CloudDataM2

Projet de Master 2 Big Data & IA -- Architecture distribuée et pipeline
de données Cloud.

------------------------------------------------------------------------

## 🚀 Objectif du projet

Développer une plateforme de **collecte, stockage, traitement et
visualisation** de données en environnement cloud et conteneurisé
(Docker), intégrant des services de data engineering, data analytics et
machine learning.

------------------------------------------------------------------------

## 🧱 Architecture technique

  -----------------------------------------------------------------------
  Composant                          Description
  ---------------------------------- ------------------------------------
  **PostgreSQL / PostGIS**           Base de données relationnelle et
                                     géospatiale pour le stockage
                                     structuré

  **Apache NiFi**                    Ingestion et orchestration des flux
                                     de données

  **Kafka**                          Gestion des événements et streaming
                                     temps réel

  **Cassandra**                      Stockage NoSQL distribué

  **Spark**                          Traitement distribué et analytique

  **FastAPI**                        Exposition des APIs de données et
                                     modèles

  **Streamlit**                      Interface de visualisation

  **Docker Compose**                 Orchestration et déploiement
                                     multi-conteneurs
  -----------------------------------------------------------------------

------------------------------------------------------------------------

## 🧩 Structure du projet

    CloudDataM2/
    │
    ├── docker-compose.yml          # Stack complète (NiFi, Postgres, Spark, etc.)
    ├── requirements.txt            # Dépendances Python
    ├── src/                        # Code source principal
    │   ├── api/                    # Endpoints FastAPI
    │   ├── connectors/             # Connexions (Postgres, Kafka, etc.)
    │   ├── notebooks/              # Analyses exploratoires
    │   ├── visualization/          # Dashboards Streamlit
    │   └── tests/                  # Tests unitaires
    │
    ├── data/                       # Données brutes et traitées
    ├── README.md                   # Documentation principale
    └── .env                        # Variables d'environnement

------------------------------------------------------------------------

## ⚙️ Installation et lancement

### 1. Cloner le projet

``` bash
git clone https://github.com/LilRaphh/CloudDataM2.git
cd CloudDataM2
```

### 2. Lancer l'environnement Docker

``` bash
docker compose up -d
```

### 3. Vérifier les services

-   NiFi : <http://localhost:8080>
-   PGAdmin : <http://localhost:5050>
-   API FastAPI : <http://localhost:8000/docs>
-   Streamlit : <http://localhost:8501>

------------------------------------------------------------------------

## 🧠 Données manipulées

Le pipeline traite plusieurs sources : - **OpenSky API** → données
aéronautiques temps réel\
- **ORS API** → calculs d'itinéraires\
- **Sources CSV / Parquet locales** → données historiques

------------------------------------------------------------------------

## 🧮 Fonctions principales

-   **Ingestion automatisée** via NiFi et Kafka\
-   **Nettoyage et enrichissement** des données\
-   **Stockage** dans PostgreSQL et Cassandra\
-   **Traitement distribué** avec Spark\
-   **Exposition API** (FastAPI)\
-   **Visualisation** via Streamlit

------------------------------------------------------------------------

## 🧰 Technologies principales

  Catégorie          Outils
  ------------------ ----------------------------
  Conteneurisation   Docker, Docker Compose
  ETL / Ingestion    Apache NiFi
  Messaging          Kafka
  Traitement         Spark, PySpark
  Stockage           PostgreSQL, Cassandra
  API                FastAPI
  Visualisation      Streamlit
  CI/CD              GitHub Actions (optionnel)

------------------------------------------------------------------------

## 👥 Auteurs

**Raphaël COLNOT**\
*M2 Big Data & Intelligence Artificielle -- 2025*

------------------------------------------------------------------------

## 📄 Licence

Ce projet est distribué sous licence MIT.
