"""
App Entry
"""
from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from dotenv import load_dotenv
from rag.weaviate import Weaviate
from rag.neo4j import Neo4jConnection
from rag.llm import LLM
import os
from fastapi.middleware.cors import CORSMiddleware

load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def read_root():
    """
    Index Route
    """
    return {"Hello": "World"}


uri = os.getenv("NEO4J_URI")
user = os.getenv("NEO4J_USERNAME")
password = os.getenv("NEO4J_PASSWORD")

model = LLM()

def handle_stream(content):
    for chunk in content:
        yield f"event: message\ndata: {chunk.text}\n\n"
    yield "event: message\ndata: END\n\n"


@app.get("/chat")
async def chat(query: str):
    """
    Responds to user's query
    """
    w = Weaviate()
    conn = Neo4jConnection(uri, user, password)

    vector_context = w.search_vector(query=query)
    print("Vector Context:\n\n", vector_context)
    cypher_query = model.generate_cypher(query=query)
    print("Generated Cypher Query:\n\n", cypher_query)
    graph_context = conn.run_cypher(cypher_query)
    print("Graph Context:\n\n", graph_context)

    stream = model.respond(question=query, graph_context=graph_context, vector_context=vector_context)

    w.close()
    conn.close()
    return StreamingResponse(handle_stream(stream), headers={'Content-Type':'text/event-stream'}, media_type='text/event-stream')