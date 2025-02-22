import sys
import os
# Add the project root directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


from rag.weaviate import Weaviate
from rag.neo4j import Neo4jConnection
from rag.llm import LLM


class AppLogic:
    def __init__(self):
        # Initialize application components
        uri = os.getenv("NEO4J_URI")
        user = os.getenv("NEO4J_USERNAME")
        password = os.getenv("NEO4J_PASSWORD")

        self.model = LLM()
        self.w = Weaviate()
        self.conn = Neo4jConnection(uri, user, password)

    def query(self, question: str):
        # Step 1: Retrieve vector context from Weaviate
        vector_context = self.w.search_vector(query=question)

        print("Vector Context:\n\n", vector_context)

        # Step 2: Generate Cypher query using the LLM
        # cypher_query = self.model.generate_cypher(query=question)
        # print("Generated Cypher Query:\n\n", cypher_query)

        # # # # # # Step 3: Retrieve graph context from Neo4j
        # graph_context = self.conn.run_cypher(cypher_query)
        # print("Graph Context:\n\n", graph_context)

        # Step 4: Generate a response using the LLM
        response_stream = self.model.respond(question=question, graph_context="", vector_context=vector_context)

    
        # Validate the response stream
        if response_stream is None:
            raise ValueError("Response stream is None. Check the LLM's respond method.")

        # Collect the generator's output into a string
        try:
            response = "".join([chunk.text for chunk in response_stream])
        except TypeError as e:
            raise ValueError(f"Invalid response stream: {e}")

        return {
            "answer": response,
            "documents": vector_context
        }

        # Collect the generator's output into a string
        

    def close(self):
        # Close connections
        self.w.close()
        self.conn.close()