from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient


app = Flask(__name__)

client = MongoClient("mongodb://admin:admin123@localhost:27017/")
db = client["DATACLOUD"]
collection = db["velib_data"]
zfe_collection = db["zfe_data"]

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/stations')
def stations():
    query = request.args.get('q', '')
    arrondissement = request.args.get('arr', '')
    limit = int(request.args.get('limit', 100))

    filters = {}
    if query:
        filters["name"] = {"$regex": query, "$options": "i"}
    if arrondissement and arrondissement != "Tous":
        filters["nom_arrondissement_communes"] = arrondissement

    data = list(collection.find(filters, {"_id": 0}).limit(limit))

    # Liste des arrondissements pour le menu déroulant
    arrondissements = collection.distinct("nom_arrondissement_communes")
    arrondissements = sorted([a for a in arrondissements if a])

    return render_template(
        'stations.html',
        records=data,
        query=query,
        limit=limit,
        arrondissements=arrondissements,
        arrondissement=arrondissement
    )

@app.route('/map')
def map_view():
    limit = int(request.args.get('limit', 200))
    arrondissement = request.args.get('arr', '')

    filters = {}
    if arrondissement and arrondissement != "Tous":
        filters["nom_arrondissement_communes"] = arrondissement

    data = list(collection.find(filters, {"_id": 0}).limit(limit))
    arrondissements = collection.distinct("nom_arrondissement_communes")
    arrondissements = sorted([a for a in arrondissements if a])

    return render_template('map.html',
                           records=data,
                           limit=limit,
                           arrondissements=arrondissements,
                           arrondissement=arrondissement)

    return render_template('map.html', records=data, limit=limit)

@app.route("/api/zfe")
def get_zfe():
    """Retourne les zones ZFE depuis Mongo au format GeoJSON."""
    zfe_docs = list(zfe_collection.find({}, {"_id": 0}))  # Supprimer le champ _id
    features = []

    for doc in zfe_docs:
        geo = doc.get("geo_shape", {}).get("geometry")
        if geo:
            feature = {
                "type": "Feature",
                "geometry": geo,
                "properties": {
                    "id": doc.get("id"),
                    "vp_critair": doc.get("vp_critair"),
                    "vul_critair": doc.get("vul_critair"),
                    "vp_horaires": doc.get("vp_horaires"),
                    "url_site_information": doc.get("url_site_information"),
                },
            }
            features.append(feature)

    return jsonify({"type": "FeatureCollection", "features": features})

@app.route('/zfe')
def zfe_view():
    """Affichage des zones ZFE avec historisation."""
    zfe_collection = db["zfe_data"]

    # Récupération de tous les documents (tu pourras limiter si besoin)
    zfe_docs = list(zfe_collection.find({}, {"_id": 0}))

    # Extraire les dates de mise à jour si dispo
    for doc in zfe_docs:
        if "date_debut" in doc and isinstance(doc["date_debut"], str):
            doc["date_debut"] = doc["date_debut"].split("T")[0]
        if "date_fin" in doc and isinstance(doc["date_fin"], str):
            doc["date_fin"] = doc["date_fin"].split("T")[0]

    # Tri par date (desc)
    zfe_docs.sort(key=lambda d: d.get("date_debut", ""), reverse=True)

    return render_template("zfe.html", records=zfe_docs)



if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)



