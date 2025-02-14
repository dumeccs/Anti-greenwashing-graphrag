"""
Script to create graph ontology
"""
import os
from google import genai
from rdflib import Graph
from langchain_text_splitters import RecursiveCharacterTextSplitter
# from rag.neo4j import Neo4jConnection
from dotenv import load_dotenv

load_dotenv()

from neo4j import GraphDatabase

class Neo4jConnection:
    """
    Defines the Neo4j database connection class
    """
    def __init__(self, uri, username, password):
        self._driver = GraphDatabase.driver(uri, auth=(username, password))

    def close(self):
        """
        Close the connection to the database
        """
        self._driver.close()

    def run_cypher(self, cypher_query):
        """
        Run a cypher query on the database
        """
        with self._driver.session() as session:
            try:
                result = session.run(cypher_query)
                return result.data()
            except Exception as e:
                print("An error occurred while running:", e)



with open('FCA-greenwashing.txt', 'r', encoding='utf-8') as file:
    content = file.read().replace('\n', '')

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=100,
    length_function=len,
    is_separator_regex=False,
)

print("creating documents...")
texts = text_splitter.create_documents([content])
print("DOCUMENTS ->", len(texts))

g = Graph()
g.parse("greenwashing.ttl")

# Ontology in standard serialisation
ontology = g.serialize(format="ttl")

client = genai.Client(
    api_key=(os.getenv("GEMINI_API_KEY")),
)


SYSTEM = (
    "You are an expert in extracting structured information out of natural language text. "
    "You extract entities with their attributes and relationships between entities. "
    "You can produce the output as RDF triples or as Cypher write statements on request. "      
)

cypher_scripts = []

for chunk in texts:
    prompt = (
        "Given the ontology below, run your best entity extraction over the content. "
        "The extracted entities and relationships must be described using exclusively the terms in the ontology "
        "and in the way they are defined. This means that for attributes and relationships you will respect the domain and range constraints. "
        "You will never use terms not defined in the ontology. "
        "Return the output as Cypher using MERGE to allow for linkage of nodes from multiple passes. "
        "Absolutely no comments on the output. Just the structured output. "
        f"\n\nONTOLOGY:\n {ontology}\n\nCONTENT:\n {chunk}"
    )
    
    response = client.models.generate_content(model="gemini-2.0-flash-001",
        contents=[
            SYSTEM,
            prompt
        ],
    )

    print(response.text)
    # cypher_script = chat_completion.choices[0].message.content.strip().strip("```\ncypher").strip("```")

    # cypher_scripts.append(cypher_script)

os._exit(1)

# Combine Cypher scripts
final_cypher_script = "\n\n---------\n\n".join(cypher_scripts)

with open('cypher.txt', "w", encoding= "utf-8") as f:
    f.write(final_cypher_script)
    print(final_cypher_script)


# with open("cypher.txt", "w", encoding="utf-8") as file:
#     final_cypher_script = file.read()

uri = os.getenv("NEO4J_URI")
user = os.getenv("NEO4J_USERNAME")
password = os.getenv("NEO4J_PASSWORD")

# create a connection to the Neo4j database
conn = Neo4jConnection(uri, user, password)

conn.run_cypher(final_cypher_script)

# Run the Cypher script and get the results
# for script in cypher_script:
#     print(script)


# Close the connection
conn.close()
