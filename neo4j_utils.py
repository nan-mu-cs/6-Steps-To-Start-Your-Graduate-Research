from neo4j import GraphDatabase

neo_db = GraphDatabase.driver('bolt://127.0.0.1:7687', auth=("neo4j", "cs411"))


def get_related_publication(title):
    records, summary, keys = neo_db.execute_query(
        "MATCH (p:PUBLICATION)<-[:PUBLISH]-()-[:PUBLISH]->(p0:PUBLICATION) WHERE p0.title = $title RETURN p.title as title, p.venue as venue, p.year as year LIMIT 5",
        {"title": title},
        routing_="r",  # or just "r"
        database_="academicworld",
    )
    return records
