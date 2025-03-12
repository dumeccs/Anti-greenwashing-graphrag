"""
Script to create embedding for document chunks and saving to Weaviate DB
"""

import os
from dotenv import load_dotenv
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from weaviate.classes.data import DataObject

from rag.weaviate import Weaviate

load_dotenv()


wcd_url = os.getenv("WCD_URL")
wcd_api_key = os.getenv("WCD_API_KEY")


TYPE = "CMA"

type_to_source = {
    "FCA": "FCA-greenwashing.txt",
    "CMA": "CMAguideline (1).txt"
}

type_to_url = {
    "CMA": "https://www.gov.uk/government/publications/green-claims-code-making-environmental-claims/environmental-claims-on-goods-and-services",
    "FCA": "https://www.fca.org.uk/publications/finalised-guidance/fg24-3-finalised-non-handbook-guidance-anti-greenwashing-rule"
}

print("Opening", type_to_source[TYPE], "...")

with open(type_to_source[TYPE], 'r', encoding='utf-8') as file:
    content = file.read()

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
            'source': type_to_url[TYPE],
        },
        'chunk': t.model_dump()['page_content'], 
    }
    return DataObject(properties=properties)


chunks = list(map(model_to_data_object, texts))
with Weaviate() as w_conn:
    w_conn.add_chunks(chunks)
    # res = w_conn.search_vector("why is tackling greenwashing a priority for us?")
    # print(res)
