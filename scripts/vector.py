"""
Script to create embedding for document chunks and saving to Weaviate DB
"""

import os
from typing import List

from dotenv import load_dotenv
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from weaviate.classes.query import MetadataQuery

# from rag.weaviate import Weaviate

import weaviate
from weaviate.classes.config import Configure, Property, DataType
from weaviate.classes.data import DataObject
from weaviate.classes.init import Auth

load_dotenv()


wcd_url = os.getenv("WCD_URL")
wcd_api_key = os.getenv("WCD_API_KEY")


class Weaviate:
    """
    Class to interact with Weaviate DB
    """
    def __init__(self):
        gemini_key = os.getenv("GEMINI_API_KEY")
        headers = {
            "X-Goog-Studio-Api-Key": gemini_key,
            # "X-Vectorizer": "text2vec-gemini"
        }

        self.client = weaviate.connect_to_weaviate_cloud(
            cluster_url=wcd_url,
            auth_credentials=Auth.api_key(wcd_api_key),
            skip_init_checks=True,
            headers=headers
        )

        print(self.client.is_ready(), "Hello ready")

        COLLECTION_NAME = "GreenWashing_Collection"
        if self.client.collections.exists(COLLECTION_NAME):
            self.collection = self.client.collections.get(COLLECTION_NAME)
            return
        
        self.collection = self.client.collections.create(
            name = COLLECTION_NAME,
            vectorizer_config=Configure.Vectorizer.text2vec_google_aistudio(),
            properties=[
                Property(name="chunk", data_type=DataType.TEXT),
            ]
        )

    def close(self):
        """
        Closes the connection to the database
        """
        self.client.close()


    def search_vector(self, query: str):
        """
        Creates a document in the database
        """
        res = self.collection.query.near_text(
            query=query,
            limit=5,
            return_metadata=MetadataQuery(
                distance=True,
                certainty=True,
                score=True,
                explain_score=True,
                is_consistent=True
            ),
        )

        context: List[str] = []
        for r in res.objects:
            context.append(r.properties.get("chunk"))

        return context


    def add_chunks(self, content: List[dict]):
        """
        Creates a document in the database
        """
        res = self.collection.data.insert_many(content)
        print(f"Chunks added in {res.elapsed_seconds}")


w_conn = Weaviate()

print("Opening file...")
with open('FCA-greenwashing.txt', 'r', encoding='utf-8') as file:
    content = file.read().replace('\n', '')

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=100,
    length_function=len,
    is_separator_regex=False,
)

texts = text_splitter.create_documents([content])

def model_to_data_object(t: Document):
    """
    Converts Document dump to proper chunk entity
    """
    properties = {
        'metadata': {
            'source': 'FCA-greenwashing.txt'
        },
        'chunk': t.model_dump()['page_content'], 
    }
    return DataObject(properties=properties)


chunks = list(map(model_to_data_object, texts))

# w_conn.add_chunks(chunks)

# w_conn.search_query("what are the rules for making anti-greenwashing claims?")

w_conn.close()