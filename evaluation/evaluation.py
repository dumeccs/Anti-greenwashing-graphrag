import os
from langchain_google_genai import ChatGoogleGenerativeAI
from datasets import Dataset
from ragas import evaluate
from ragas.metrics import (
    faithfulness,
    context_recall,
    context_precision,
)
from app_logic import AppLogic
# from testdataII import test_data
# from testdata import test_data
from testdataIII import test_data

# Initialize application logic
app = AppLogic()

llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-pro",
    temperature=0.3,
    max_tokens=None,
    timeout=None,
    max_retries=2,
    google_api_key=os.getenv("GEMINI_API_KEY"),
)


# Prepare the dataset for evaluation
data = {
    "question": [],
    "ground_truth": [],
    "contexts": [],
    "answer": [],  # This will be populated by querying your application
}

# Query your application and populate the dataset
for item in test_data:
    response = app.query(item["question"])
    data["question"].append(item["question"])
    data["ground_truth"].append(item["ground_truth"])
    data["contexts"].append(item["contexts"])
    data["answer"].append(response)

# Convert to Hugging Face Dataset
dataset = Dataset.from_dict(data)

# Define the metrics to evaluate
metrics = [
    faithfulness,
    context_recall,
    context_precision,
]

# Evaluate the dataset
result = evaluate(dataset, metrics, llm=llm)

# Print the evaluation results

print(result)
result.upload()


# # Define and close Weaviate client
# from weaviate import Client
# client = Client(os.getenv("WEAVIATE_URL"))
# client.close()  # for Weaviate

# # Initialize and close Neo4j driver
# from neo4j import GraphDatabase

# driver = GraphDatabase.driver(os.getenv("NEO4J_URI"), auth=(os.getenv("NEO4J_USER"), os.getenv("NEO4J_PASSWORD")))
# driver.close()  # for Neo4j

# Close connections
app.close()