from neo4j import GraphDatabase

# ---------- CONFIG ----------
NEO4J_URI = "bolt://localhost:7687"
NEO4J_USER = "neo4j"
NEO4J_PASSWORD = "password123"


# ---------- DATA : PERSONNAGES ----------
# Principaux + récurrents + quelques créatures
CHARACTERS = [
    # Kids / Party
    {"name": "Eleven", "category": "Kid", "type": "Human", "status": "Alive", "introduced_season": 1, "is_main": True},
    {"name": "Mike Wheeler", "category": "Kid", "type": "Human", "status": "Alive", "introduced_season": 1, "is_main": True},
    {"name": "Dustin Henderson", "category": "Kid", "type": "Human", "status": "Alive", "introduced_season": 1, "is_main": True},
    {"name": "Lucas Sinclair", "category": "Kid", "type": "Human", "status": "Alive", "introduced_season": 1, "is_main": True},
    {"name": "Will Byers", "category": "Kid", "type": "Human", "status": "Alive", "introduced_season": 1, "is_main": True},
    {"name": "Max Mayfield", "category": "Kid", "type": "Human", "status": "Alive", "introduced_season": 2, "is_main": True},
    {"name": "Erica Sinclair", "category": "Kid", "type": "Human", "status": "Alive", "introduced_season": 2, "is_main": False},
    {"name": "Suzie Bingham", "category": "Kid", "type": "Human", "status": "Alive", "introduced_season": 3, "is_main": False},

    # Teens
    {"name": "Nancy Wheeler", "category": "Teen", "type": "Human", "status": "Alive", "introduced_season": 1, "is_main": True},
    {"name": "Jonathan Byers", "category": "Teen", "type": "Human", "status": "Alive", "introduced_season": 1, "is_main": True},
    {"name": "Steve Harrington", "category": "Teen", "type": "Human", "status": "Alive", "introduced_season": 1, "is_main": True},
    {"name": "Robin Buckley", "category": "Teen", "type": "Human", "status": "Alive", "introduced_season": 3, "is_main": True},
    {"name": "Eddie Munson", "category": "Teen", "type": "Human", "status": "Dead", "introduced_season": 4, "is_main": False},
    {"name": "Billy Hargrove", "category": "Teen", "type": "Human", "status": "Dead", "introduced_season": 2, "is_main": False},
    {"name": "Chrissy Cunningham", "category": "Teen", "type": "Human", "status": "Dead", "introduced_season": 4, "is_main": False},

    # Adults
    {"name": "Joyce Byers", "category": "Adult", "type": "Human", "status": "Alive", "introduced_season": 1, "is_main": True},
    {"name": "Jim Hopper", "category": "Adult", "type": "Human", "status": "Alive", "introduced_season": 1, "is_main": True},
    {"name": "Karen Wheeler", "category": "Adult", "type": "Human", "status": "Alive", "introduced_season": 1, "is_main": False},
    {"name": "Ted Wheeler", "category": "Adult", "type": "Human", "status": "Alive", "introduced_season": 1, "is_main": False},
    {"name": "Murray Bauman", "category": "Adult", "type": "Human", "status": "Alive", "introduced_season": 2, "is_main": False},
    {"name": "Dr. Sam Owens", "category": "Adult", "type": "Human", "status": "Alive", "introduced_season": 2, "is_main": False},
    {"name": "Dr. Martin Brenner", "category": "Adult", "type": "Human", "status": "Dead", "introduced_season": 1, "is_main": False},
    {"name": "Bob Newby", "category": "Adult", "type": "Human", "status": "Dead", "introduced_season": 2, "is_main": False},
    {"name": "Argyle", "category": "Adult", "type": "Human", "status": "Alive", "introduced_season": 4, "is_main": False},
    {"name": "Scott Clarke", "category": "Adult", "type": "Human", "status": "Alive", "introduced_season": 1, "is_main": False},

    # Famille élargie / enfants
    {"name": "Holly Wheeler", "category": "Kid", "type": "Human", "status": "Alive", "introduced_season": 1, "is_main": False},

    # Expérimentés / surnaturels
    {"name": "Kali Prasad", "category": "Experiment", "type": "Human", "status": "Alive", "introduced_season": 2, "is_main": False},  # 008
    {"name": "Henry Creel", "category": "Experiment", "type": "Human", "status": "Alive", "introduced_season": 4, "is_main": False},
    {"name": "Vecna", "category": "Entity", "type": "Creature", "status": "Active", "introduced_season": 4, "is_main": True},
    {"name": "The Mind Flayer", "category": "Entity", "type": "Creature", "status": "Active", "introduced_season": 2, "is_main": True},
    {"name": "Demogorgon", "category": "Entity", "type": "Creature", "status": "Active", "introduced_season": 1, "is_main": True},
]


# ---------- DATA : RELATIONS ----------

# Amitiés / groupe kids + entourage
FRIEND_RELATIONS = [
    # Party
    ("Mike Wheeler", "Dustin Henderson"),
    ("Mike Wheeler", "Lucas Sinclair"),
    ("Mike Wheeler", "Will Byers"),
    ("Dustin Henderson", "Lucas Sinclair"),
    ("Dustin Henderson", "Will Byers"),
    ("Lucas Sinclair", "Will Byers"),
    ("Max Mayfield", "Lucas Sinclair"),
    ("Max Mayfield", "Eleven"),
    ("Eleven", "Mike Wheeler"),
    ("Erica Sinclair", "Dustin Henderson"),
    ("Erica Sinclair", "Lucas Sinclair"),

    # Teens
    ("Nancy Wheeler", "Jonathan Byers"),
    ("Nancy Wheeler", "Steve Harrington"),
    ("Steve Harrington", "Robin Buckley"),
    ("Steve Harrington", "Dustin Henderson"),
    ("Robin Buckley", "Nancy Wheeler"),
    ("Eddie Munson", "Dustin Henderson"),

    # Autres
    ("Argyle", "Jonathan Byers"),
    ("Argyle", "Argyle"),  # auto ref possible à virer si tu veux garder tout clean
]

# Famille
FAMILY_RELATIONS = [
    ("Joyce Byers", "Will Byers"),
    ("Joyce Byers", "Jonathan Byers"),
    ("Jim Hopper", "Eleven"),  # adoption
    ("Karen Wheeler", "Mike Wheeler"),
    ("Karen Wheeler", "Nancy Wheeler"),
    ("Karen Wheeler", "Holly Wheeler"),
    ("Ted Wheeler", "Mike Wheeler"),
    ("Ted Wheeler", "Nancy Wheeler"),
    ("Ted Wheeler", "Holly Wheeler"),
    ("Lucas Sinclair", "Erica Sinclair"),  # fratrie
]

# Romantique (sens relationnel, pas besoin d’être encore ensemble)
ROMANTIC_RELATIONS = [
    ("Mike Wheeler", "Eleven"),
    ("Lucas Sinclair", "Max Mayfield"),
    ("Nancy Wheeler", "Steve Harrington"),
    ("Nancy Wheeler", "Jonathan Byers"),
    ("Joyce Byers", "Bob Newby"),
    ("Joyce Byers", "Jim Hopper"),
]

# Alliances / bosse ensemble
ALLY_RELATIONS = [
    ("Jim Hopper", "Joyce Byers"),
    ("Jim Hopper", "Nancy Wheeler"),
    ("Jim Hopper", "Jonathan Byers"),
    ("Jim Hopper", "Steve Harrington"),
    ("Jim Hopper", "Murray Bauman"),
    ("Joyce Byers", "Murray Bauman"),
    ("Murray Bauman", "Nancy Wheeler"),
    ("Murray Bauman", "Jonathan Byers"),
    ("Dr. Sam Owens", "Jim Hopper"),
    ("Dr. Sam Owens", "Eleven"),
    ("Robin Buckley", "Steve Harrington"),
    ("Robin Buckley", "Nancy Wheeler"),
    ("Erica Sinclair", "Eddie Munson"),

    # Alliances côté Monde à l'envers
    ("Vecna", "Demogorgon"),
    ("Vecna", "The Mind Flayer"),
]

# Liens créatures ↔ humains (ennemis)
ENEMY_RELATIONS = [
    ("Demogorgon", "Eleven"),
    ("Demogorgon", "Jim Hopper"),
    ("Demogorgon", "Joyce Byers"),
    ("The Mind Flayer", "Will Byers"),
    ("The Mind Flayer", "Eleven"),
    ("The Mind Flayer", "Mike Wheeler"),
    ("The Mind Flayer", "Lucas Sinclair"),
    ("The Mind Flayer", "Dustin Henderson"),
    ("The Mind Flayer", "Max Mayfield"),
    ("Vecna", "Max Mayfield"),
    ("Vecna", "Nancy Wheeler"),
    ("Vecna", "Eddie Munson"),
    ("Vecna", "Chrissy Cunningham"),
    ("Vecna", "Erica Sinclair"),
    ("Vecna", "Robin Buckley"),
]

# Relations de travail / labo / gouvernement
WORK_RELATIONS = [
    ("Dr. Martin Brenner", "Eleven"),
    ("Dr. Martin Brenner", "Kali Prasad"),
    ("Dr. Martin Brenner", "Henry Creel"),
    ("Dr. Sam Owens", "Dr. Martin Brenner"),
    ("Dr. Sam Owens", "Murray Bauman"),
]

# Identités multiples
ALTER_EGO_RELATIONS = [
    ("Henry Creel", "Vecna"),
]


# ---------- FONCTIONS NEO4J ----------

def create_constraints(tx):
    # Unicité sur le nom
    tx.run("""
        CREATE CONSTRAINT character_name_unique IF NOT EXISTS
        FOR (c:Character)
        REQUIRE c.name IS UNIQUE
    """)


def insert_characters(tx, characters):
    tx.run(
        """
        UNWIND $characters AS ch
        MERGE (c:Character {name: ch.name})
        SET c.category = ch.category,
            c.type = ch.type,
            c.status = ch.status,
            c.introduced_season = ch.introduced_season,
            c.is_main = ch.is_main
        """,
        characters=characters,
    )


def insert_relations_simple(tx, rels, rel_type):
    """
    rels : liste de tuples (from, to)
    rel_type : string, ex 'FRIEND_OF'
    """
    if not rels:
        return
    query = f"""
    UNWIND $rels AS rel
    MATCH (a:Character {{name: rel.from}}),
          (b:Character {{name: rel.to}})
    MERGE (a)-[r:{rel_type}]->(b)
    """
    tx.run(
        query,
        rels=[{"from": r[0], "to": r[1]} for r in rels]
    )


def main():
    driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))

    print("=== Connexion à Neo4j ===")
    with driver.session() as session:
        print("→ Création des contraintes")
        session.execute_write(create_constraints)

        print("→ Insertion des personnages (principaux + récurrents + créatures)")
        session.execute_write(insert_characters, CHARACTERS)

        print("→ Insertion des relations FRIEND_OF")
        session.execute_write(insert_relations_simple, FRIEND_RELATIONS, "FRIEND_OF")

        print("→ Insertion des relations FAMILY")
        session.execute_write(insert_relations_simple, FAMILY_RELATIONS, "FAMILY")

        print("→ Insertion des relations ROMANTIC")
        session.execute_write(insert_relations_simple, ROMANTIC_RELATIONS, "ROMANTIC")

        print("→ Insertion des relations ALLY_OF")
        session.execute_write(insert_relations_simple, ALLY_RELATIONS, "ALLY_OF")

        print("→ Insertion des relations ENEMY_OF")
        session.execute_write(insert_relations_simple, ENEMY_RELATIONS, "ENEMY_OF")

        print("→ Insertion des relations WORKS_WITH")
        session.execute_write(insert_relations_simple, WORK_RELATIONS, "WORKS_WITH")

        print("→ Insertion des relations ALTER_EGO_OF")
        session.execute_write(insert_relations_simple, ALTER_EGO_RELATIONS, "ALTER_EGO_OF")

    driver.close()
    print("=== Fini ===")


if __name__ == "__main__":
    main()
