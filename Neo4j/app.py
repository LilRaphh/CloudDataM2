from flask import Flask, render_template, jsonify
from neo4j import GraphDatabase

# ---------- CONFIG ----------
NEO4J_URI = "bolt://localhost:7687"
NEO4J_USER = "neo4j"
NEO4J_PASSWORD = "password123"

app = Flask(__name__)

driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))


# ---------- HELPERS NEO4J ----------
def get_characters():
    query = """
    MATCH (c:Character)
    RETURN id(c) AS id,
           c.name AS name,
           c.category AS category,
           c.type AS type,
           c.status AS status,
           c.introduced_season AS introduced_season,
           c.is_main AS is_main
    ORDER BY name
    """
    with driver.session() as session:
        result = session.run(query)
        return [record.data() for record in result]


def get_stats():
    query_nodes = "MATCH (c:Character) RETURN count(c) AS count"
    query_rels = "MATCH ()-[r]->() RETURN count(r) AS count"

    with driver.session() as session:
        nodes = session.run(query_nodes).single()["count"]
        rels = session.run(query_rels).single()["count"]
    return nodes, rels


def get_graph():
    # Nodes
    query_nodes = """
    MATCH (c:Character)
    RETURN id(c) AS id,
           c.name AS name,
           c.category AS category,
           c.type AS type,
           c.status AS status
    """

    # Relations
    query_rels = """
    MATCH (a:Character)-[r]->(b:Character)
    RETURN id(a) AS source,
           id(b) AS target,
           type(r) AS type
    """

    with driver.session() as session:
        nodes_res = session.run(query_nodes)
        rels_res = session.run(query_rels)

        nodes = []
        for record in nodes_res:
            nodes.append({
                "id": record["id"],
                "name": record["name"],
                "category": record["category"],
                "type": record["type"],
                "status": record["status"],
            })

        links = []
        for record in rels_res:
            links.append({
                "source": record["source"],  # id du nœud source
                "target": record["target"],  # id du nœud cible
                "type": record["type"],
            })

    return {"nodes": nodes, "links": links}



# ---------- ROUTES ----------
@app.route("/")
def index():
    nodes_count, rels_count = get_stats()
    characters = get_characters()
    return render_template(
        "index.html",
        nodes_count=nodes_count,
        rels_count=rels_count,
        characters=characters
    )


@app.route("/characters")
def characters():
    chars = get_characters()
    return render_template("characters.html", characters=chars)


@app.route("/graph")
def graph_page():
    return render_template("graph.html")


@app.route("/api/graph")
def graph_api():
    graph_data = get_graph()
    return jsonify(graph_data)


if __name__ == "__main__":
    app.run(
        debug=True,
        host="0.0.0.0",  # ou "127.0.0.1" si tu veux local only
        port=5001        # ou 8000, 5050, etc.
    )
