import os
from langchain_google_genai import ChatGoogleGenerativeAI
from datasets import Dataset
from ragas import evaluate
from ragas.metrics import (
    faithfulness,
    # answer_relevance,  
    # context_relevance,  
    context_recall,
    context_precision,
)
from app_logic import AppLogic
from testdata import test_data

# Initialize application logic
app = AppLogic()

llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-pro",
    temperature=0,
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
    # answer_relevance,
    # context_relevance,
    context_recall,
    context_precision,
]

# Evaluate the dataset
result = evaluate(dataset, metrics, llm=llm)

# Print the evaluation results
print(result)

# Close connections
app.close()