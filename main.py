"""
App Entry
"""
from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from dotenv import load_dotenv
from rag.weaviate import Weaviate
from rag.neo4j import Neo4jConnection
from rag.llm import LLM
import os, json
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

def handle_stream(content, sources):
    for chunk in content:
        s = f"event: message\ndata: {repr(chunk.text)}\n\n"
        yield s
    yield "event: message\ndata: <SOURCES>" + json.dumps(list(sources)) + "\n\n"
    yield "event: message\ndata: END\n\n"


@app.get("/chat")
async def chat(query: str):
    """
    Responds to user's query
    """

    with Weaviate() as w:
        vector_res = w.search_vector(query=query)
        vector_context = "\n".join([x['chunk'] for x in vector_res])
        sources = set([source['metadata']['source'] for source in vector_res])
        print("Vector Context:\n\n", vector_context)

    cypher_query = model.generate_cypher(query=query)
    print("Generated Cypher Query:\n\n", cypher_query)

    with Neo4jConnection(uri, user, password) as conn:
        graph_context = conn.run_cypher(cypher_query)
        print("Graph Context:\n\n", graph_context)

    stream = model.respond(
        question=query,
        graph_context=graph_context,
        vector_context=vector_context
    )

    return StreamingResponse(
        handle_stream(stream, sources),
        headers={
            'Content-Type':'text/event-stream'
        },
        media_type='text/event-stream'
    )
