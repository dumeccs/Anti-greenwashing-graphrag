"""
This module contains the class which is used to interact with the Neo4j database.
"""
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

    def __enter__(self):
        """
        Runs when entering `with` block
        """
        print("initializing neo4j")
        return self

    def __exit__(self, exc_type, exc_val, traceback):
        """
        Runs when exiting `with` block
        """
        print(f"Exception Type: {exc_type}")
        print(f"Exception Value: {exc_val}")
        print(f"Traceback: {traceback}")
        self.close()

    

    def run_cypher(self, cypher_query):
        """
        Run a cypher query on the database
        """
        with self._driver.session() as session:
            try:
                result = session.run(cypher_query)
                return result.data()
            except Exception as e:
                print("failed to run cypher query. error:",e, "query:", cypher_query)
                return "No Relationship"
