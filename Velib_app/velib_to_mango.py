import requests
from pymongo import MongoClient

# Connexion MongoDB
client = MongoClient("mongodb://admin:admin123@localhost:27017/")
db = client["DATACLOUD"]
collection = db["velib_data"]

# URL de base
BASE_URL = "https://opendata.paris.fr/api/explore/v2.1/catalog/datasets/velib-disponibilite-en-temps-reel/records"

limit = 100
offset = 0
total_inserted = 0
all_records = []

while True:
    url = f"{BASE_URL}?limit={limit}&offset={offset}"
    response = requests.get(url)

    if response.status_code != 200:
        print(f"Erreur API {response.status_code}")
        break

    data = response.json()
    records = data.get("results") or data.get("records") or []

    if not records:
        break

    all_records.extend(records)
    print(f"→ {len(records)} stations récupérées (offset={offset})")

    # Si moins de 100 résultats, on est à la fin
    if len(records) < limit:
        break

    offset += limit

# Nettoyage et enregistrement
if all_records:
    collection.delete_many({})
    collection.insert_many(all_records)
    total_inserted = len(all_records)
    print(f"\n✅ {total_inserted} stations insérées dans MongoDB")
else:
    print("Aucune donnée récupérée.")
