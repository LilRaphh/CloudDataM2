# 🚲💫 CloudDataM2 — Vélib' Analytics & Neo4j Stranger Graph

Projet intégrant **deux applications web** développées dans le cadre du M2 Big Data & IA :  
1) **Vélib Data** : Visualisation, historisation et analyse temps réel des stations Vélib'.  
2) **Stranger Graph (Neo4j)** : Exploration interactive du réseau de personnages de *Stranger Things* à partir d’une base de graphes.

Les deux applications sont conteneurisées via **Docker Compose**, partagent une organisation commune et sont hébergées dans ce même dépôt.

---

# 📦 Contenu du dépôt

```
CloudDataM2/
│
├── velib_app/                       # Application Vélib'
│   ├── app.py
│   ├── templates/
│   ├── static/
│   ├── velib_to_mongo.py
│   └── ...
│
├── neo4j_stranger_graph/            # Application Neo4j Stranger Things
│   ├── app.py
│   ├── templates/
│   ├── static/
│   ├── queries.cypher
│   └── ...
│
├── docker-compose.yml               # Stack globale (Flask + MongoDB + Neo4j)
├── requirements.txt
└── README.md                        # Vous êtes ici
```

---

# 🎯 Objectifs des applications

## 1) 🚲 Vélib Data — Analyse & Historisation
- Carte interactive des **stations Vélib'** en temps réel.  
- Superposition des **zones ZFE**.  
- **Historisation MongoDB** sans écrasement.  
- Visualisation des données, filtrage, mise à jour.  
- Base d’analyse pour la mobilité urbaine.

## 2) 💫 Stranger Graph — Exploration Neo4j
- Visualisation des **personnages de Stranger Things**.  
- Navigation dans les **relations du graphe** (amitié, famille, interactions).  
- Pages HTML stylisées "Upside Down".  
- Statistiques des **nœuds et relations** en base.  
- Exploration filtrée (type de relation, saison, etc. – si activé).

---

# 🧠 Stack technique globale

| Composant | Usage |
|----------|--------|
| **Flask** | Serveur web / API pour les deux apps |
| **MongoDB** | Historique des relevés Vélib' |
| **Neo4j** | Base graph orientée Stranger Things |
| **Cypher** | Requêtes sur le graphe Neo4j |
| **Leaflet.js** | Carte interactive Vélib' |
| **Docker Compose** | Orchestration des services |
| **HTML/CSS/JS + Jinja2** | Interfaces web |

---

# 🗂️ Structure détaillée des deux projets

## 📁 Vélib'
```
velib_app/
│
├── app.py                     # Backend Flask
├── templates/
│   ├── base.html
│   ├── index.html
│   ├── map.html
│   └── zfe.html
├── static/
│   ├── style.css
│   └── scripts.js
├── velib_to_mongo.py          # Script d’historisation MongoDB
└── data/                      # Optionnel : dumps, exports
```

## 📁 Stranger Graph (Neo4j)
```
neo4j_stranger_graph/
│
├── app.py                     # Backend Flask + connexion Neo4j
├── queries.cypher             # Requêtes centralisées
├── templates/
│   ├── base.html
│   ├── index.html
│   ├── characters.html
│   └── relations.html
├── static/
│   ├── style.css
│   ├── upside.css
│   └── scripts.js
```

---

# ⚙️ Installation & Lancement

## 1) Cloner le dépôt

```bash
git clone https://github.com/LilRaphh/CloudDataM2.git
cd CloudDataM2
```

## 2) Lancer avec Docker

```bash
docker compose up -d
```

## 3) Accéder aux applications

| Service | URL |
|--------|-----|
| **Vélib App** | http://localhost:5000 |
| **Stranger Graph / Neo4j App** | http://localhost:5001 |
| **Neo4j Browser** | http://localhost:7474 |
| **Mongo Express** (si activé) | http://localhost:8081 |

---

# 🚲 Fonctionnalités Vélib'

### ✓ Carte interactive en temps réel
Affichage des stations avec icônes dynamiques :
- vélos mécaniques  
- vélos électriques  
- bornes disponibles  

### ✓ Overlay des zones ZFE
Chargées via Open Data Paris.

### ✓ Historisation MongoDB
Chaque mise à jour insère un nouvel enregistrement **sans écrasement des anciens**.

### Exemple
```python
existing = collection.find_one({"station_id": station_id})
if not existing or existing["last_update"] != new_data["last_update"]:
    collection.insert_one(new_data)
```

### ✓ Filtres, pagination, limite d’affichage, arrondissements

---

# 💫 Fonctionnalités Stranger Graph (Neo4j)

### ✓ Page d’accueil immersive "Upside Down"
- compteur des personnages  
- compteur des relations  
- ambiance visuelle Stranger Things  

### ✓ Liste des personnages
- cartes stylisées  
- rôle, saison, description  
- lien vers détail des relations  

### ✓ Exploration du graphe via Cypher
```cypher
MATCH (c:Character)-[r:RELATION]->(d:Character)
RETURN c, r, d
```

### ✓ Filtres possibles
- type de relation  
- saison  
- personnage source  

---

# 📸 Captures d’écran (à compléter)
### 📍 Vélib' Map  
<img width="3405" height="1298" alt="image"
src="https://github.com/user-attachments/assets/c7240279-bf90-4e97-8dbb-eaa452178df6" />


### 💀 Stranger Graph Home  
<img width="1672" height="1120" alt="image" src="https://github.com/user-attachments/assets/b514e9d7-3a65-418e-ae6b-a0814768daa0" />


---

# 🧰 Technologies utilisées

| Type | Outils |
|------|--------|
| Backend | Flask, Python, Requests |
| Base NoSQL | MongoDB |
| Base Graphe | Neo4j, Neo4j Driver |
| Frontend | HTML5, CSS3, JavaScript |
| Cartographie | Leaflet.js |
| Conteneurisation | Docker, Docker Compose |
| Données | OpenData Paris (Vélib', ZFE) & dataset Stranger Things |

---

# 👨‍💻 Auteur

**Raphaël COLNOT**  
*M2 Big Data & Intelligence Artificielle — CloudDataM2*

---

# 📄 Licence

Projet publié sous **licence MIT**.
