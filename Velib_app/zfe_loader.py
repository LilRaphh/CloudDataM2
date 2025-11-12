import requests
from pymongo import MongoClient
from datetime import datetime

# === Connexion MongoDB ===
client = MongoClient("mongodb://admin:admin123@localhost:27017/")
db = client["DATACLOUD"]
collection = db["zfe_data"]

# === URL API ZFE (Paris) ===
BASE_URL = "https://opendata.paris.fr/api/explore/v2.1/catalog/datasets/zone-a-faibles-emissions/records"

limit = 100
offset = 0
all_records = []
timestamp = datetime.utcnow().isoformat()  # Horodatage UTC pour historisation

# === Boucle de récupération ===
while True:
    params = {"limit": limit, "offset": offset}
    response = requests.get(BASE_URL, params=params)

    if response.status_code != 200:
        print(f"Erreur API {response.status_code} : {response.text}")
        break

    data = response.json()
    records = data.get("results", [])
    if not records:
        break

    # Ajout d’un champ d’historisation sur chaque record
    for r in records:
        r["import_timestamp"] = timestamp

    all_records.extend(records)
    print(f"→ {len(records)} zones récupérées (offset={offset})")

    if len(records) < limit:
        break
    offset += limit

# === Insertion Mongo sans suppression ===
if all_records:
    collection.insert_many(all_records)
    print(f"\n✅ {len(all_records)} zones ZFE insérées dans MongoDB avec timestamp {timestamp}")
else:
    print("Aucune donnée récupérée.")
