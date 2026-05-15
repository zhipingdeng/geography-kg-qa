"""Import OwnThink data into all 4 domain projects' Neo4j containers."""
import asyncio
import csv
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from app.data.parser import OwnThinkParser
from app.data.importer import GraphImporter
from app.database.neo4j_client import Neo4jClient

OWNTHINK_PATH = "/mnt/e/hermes_code_workspace/dataset/通用百科数据集/OwnThink_KG/ownthink_v2.csv"

PROJECTS = {
    "geography": {
        "uri": "bolt://localhost:7688",
        "tags": ["地理", "旅游", "景点", "山脉", "河流", "湖泊", "国家", "城市"],
    },
    "education": {
        "uri": "bolt://localhost:7689",
        "tags": ["教育", "学校", "大学", "学院", "学科", "学术"],
    },
    "technology": {
        "uri": "bolt://localhost:7690",
        "tags": ["科技", "互联网", "计算机", "软件", "硬件", "人工智能", "IT"],
    },
}


async def import_project(name: str, uri: str, tags: list[str], limit: int = 100000):
    print(f"\n{'='*60}")
    print(f"Importing: {name}")
    print(f"Neo4j: {uri}")
    print(f"Tags: {tags}")
    print(f"{'='*60}")

    client = Neo4jClient(uri, "neo4j", os.getenv("NEO4J_PASSWORD", ""))
    await client.connect()

    parser = OwnThinkParser()
    importer = GraphImporter(client)

    # Phase 1: Find matching entities
    matching_entities = set()
    print(f"Scanning for entities with tags: {tags}")
    with open(OWNTHINK_PATH, "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        next(reader, None)
        for row in reader:
            if len(row) < 3:
                continue
            entity, attr, value = row[0].strip(), row[1].strip(), row[2].strip()
            if attr == "标签" and value in tags:
                matching_entities.add(entity)

    print(f"Found {len(matching_entities)} entities")
    if not matching_entities:
        print("No matching entities. Skipping.")
        await client.close()
        return 0

    # Phase 2: Parse triples
    triples = []
    with open(OWNTHINK_PATH, "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        next(reader, None)
        for row in reader:
            if len(row) < 3:
                continue
            line = ",".join(row)
            t = parser.parse_line(line)
            if not t:
                continue
            if t.entity not in matching_entities:
                continue
            triples.append(t)
            if len(triples) >= limit:
                break

    print(f"Parsed {len(triples)} triples")

    # Phase 3: Import
    imported = await importer.import_triples(triples, source="ownthink")
    print(f"Imported {imported} records")

    result = await client.execute("MATCH (n:Entity {source: 'ownthink'}) RETURN count(n) AS cnt")
    print(f"Neo4j entity count: {result[0]['cnt']}")
    await client.close()
    return imported


async def main():
    project = sys.argv[1] if len(sys.argv) > 1 else "all"
    
    if project == "all":
        for name, config in PROJECTS.items():
            await import_project(name, config["uri"], config["tags"])
    elif project in PROJECTS:
        config = PROJECTS[project]
        await import_project(project, config["uri"], config["tags"])
    else:
        print(f"Unknown project: {project}. Use: geography, education, technology, or all")
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
