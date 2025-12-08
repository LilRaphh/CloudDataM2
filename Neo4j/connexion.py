from pymongo import MongoClient
from neo4j import GraphDatabase
import re

# ---------- CONFIG ----------
MONGO_URI = "mongodb://admin:admin123@localhost:27017/?authSource=admin"
MONGO_DB = "DATACLOUD"

NEO4J_URI = "bolt://localhost:7687"
NEO4J_USER = "neo4j"
NEO4J_PASSWORD = "password123"


# ---------- UTIL ----------
def clean_label(name):
    """Transforme 'velib_data' -> 'VelibData'"""
    return "".join(word.capitalize() for word in re.split(r"[_\- ]", name))


def flatten_props(doc):
    """Convertit un document Mongo en dict compatible Neo4j"""
    props = {}
    for k, v in doc.items():
        if k == "_id":
            continue
        if isinstance(v, (dict, list)):
            props[k] = str(v)
        else:
            props[k] = v
    return props


# ---------- CONNECT ----------
mongo = MongoClient(MONGO_URI)
db = mongo[MONGO_DB]

neo4j = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))


# ---------- IMPORT ----------
def insert_document(tx, label, doc):
    tx.run(
        f"""
        MERGE (n:{label} {{ _id: $id }})
        SET n += $props
        """,
        id=str(doc["_id"]),
        props=flatten_props(doc)
    )


print("=== Import MongoDB → Neo4j ===")

with neo4j.session() as session:
    for collection_name in db.list_collection_names():
        collection = db[collection_name]

        label = clean_label(collection_name)
        print(f"⟹ Import collection: {collection_name} → label Neo4j: {label}")

        for doc in collection.find():
            session.execute_write(insert_document, label, doc)

print("=== Import terminé ===")

neo4j.close()
mongo.close()
