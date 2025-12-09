from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient
import math

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
        geo = doc.get("geo_shape")
        if not geo:
            continue

        # Deux cas possibles selon la structure renvoyée par l'API Paris :
        # 1) geo_shape = { "type": "Feature", "geometry": {...} }
        # 2) geo_shape = { "type": "Polygon" / "MultiPolygon", "coordinates": [...] }
        if isinstance(geo, dict) and geo.get("type") == "Feature" and "geometry" in geo:
            geometry = geo["geometry"]
        else:
            geometry = geo  # on considère que c'est déjà une geometry valide

        feature = {
            "type": "Feature",
            "geometry": geometry,
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

def haversine(lat1, lon1, lat2, lon2):
    R = 6371
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = (math.sin(dlat / 2)**2 +
         math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) *
         math.sin(dlon / 2)**2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c

@app.route("/nearest_station")
def nearest_station():
    user_lat = float(request.args.get("lat"))
    user_lon = float(request.args.get("lon"))

    # Récupération depuis TA collection MongoDB
    stations = list(collection.find({}, {"_id": 0}))

    # Fonction pour extraire les coordonnées comme dans map.html
    def extract_coords(station):
        c = station.get("coordonnees_geo")
        if not c:
            return None
        if isinstance(c, list) and len(c) == 2:
            return float(c[0]), float(c[1])
        if isinstance(c, dict):
            if "lat" in c and "lon" in c:
                return float(c["lat"]), float(c["lon"])
            if "latitude" in c and "longitude" in c:
                return float(c["latitude"]), float(c["longitude"])
        return None

    nearest = None
    min_dist = float("inf")

    for s in stations:
        coords = extract_coords(s)
        if not coords:
            continue

        slat, slon = coords
        dist = haversine(user_lat, user_lon, slat, slon)

        if dist < min_dist:
            min_dist = dist
            nearest = (s, slat, slon)

    if nearest is None:
        return jsonify({"error": "No valid station coordinates found"}), 500

    s, slat, slon = nearest

    return jsonify({
        "name": s.get("name"),
        "lat": slat,
        "lon": slon,
        "numbikes": s.get("numbikesavailable"),
        "numdocks": s.get("numdocksavailable"),
        "arrondissement": s.get("nom_arrondissement_communes"),
        "distance_km": round(min_dist, 3)
    })

@app.route('/grafana')
def grafana():
    return render_template('grafana.html')



if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)



