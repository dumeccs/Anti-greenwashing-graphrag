import os
from dotenv import load_dotenv
from langsmith import Client
from evaluator import correctness,  relevance, groundedness
from app_logic import AppLogic

# Load environment variables from .env file
load_dotenv()

# Initialize LangSmith client
client = Client()

# Fetch dataset name from environment variables
DATASET_NAME = os.getenv("DATASET_NAME", "FCA and CMA anti-greenwashing rules")

# Import examples from the separate file
from testdatalangsmith import examples

def get_or_create_dataset(client: Client, dataset_name: str) -> str:
    """
    Get the dataset ID if it exists, or create a new dataset if it doesn't.
    
    Args:
        client (Client): LangSmith client instance.
        dataset_name (str): Name of the dataset.
    
    Returns:
        str: ID of the dataset.
    """
    try:
        # Check if the dataset already exists
        datasets = list(client.list_datasets(dataset_name=dataset_name))  # Convert generator to list
        if datasets:
            print(f"Dataset '{dataset_name}' already exists. Using existing dataset.")
            return datasets[0].id  # Access the first dataset in the list
        
        # Create a new dataset
        dataset = client.create_dataset(dataset_name=dataset_name)
        print(f"Created new dataset: {dataset_name}")
        return dataset.id
    except Exception as e:
        print(f"Error getting or creating dataset: {e}")
        raise

def populate_dataset(client: Client, dataset_id: str, examples: list):
    """
    Populate a dataset with examples.
    
    Args:
        client (Client): LangSmith client instance.
        dataset_id (str): ID of the dataset to populate.
        examples (list): List of examples in the format [(question, answer), ...].
    """
    try:
        # Create examples in the dataset
        client.create_examples(
            inputs=[{"question": q} for q, _ in examples], 
            outputs=[{"answer": a} for _, a in examples], 
            dataset_id=dataset_id,
        )
        print(f"Populated dataset with {len(examples)} examples.")
    except Exception as e:
        print(f"Error populating dataset: {e}")
        raise

def target(inputs: dict) -> dict:
    """
    Target function representing the RAG application.
    Uses AppLogic to generate a response to the question.
    """
    # Initialize the RAG application
    rag_app = AppLogic()
    
    try:
        # Get the question from the inputs
        question = inputs["question"]
        
        # Query the RAG application
        response = rag_app.query(question)
        
        # Return the response in the expected format
        return {"answer": response["answer"],
                "documents": response["documents"]}
    finally:
        # Close the RAG application connections
        rag_app.close()

def main():
    # Get or create the dataset
    dataset_id = get_or_create_dataset(client, DATASET_NAME)
    
    # Populate the dataset with examples
    populate_dataset(client, dataset_id, examples)

     # Run the evaluation
    experiment_results = client.evaluate(
        target,  # Your RAG application
        data=DATASET_NAME,  # Name of the dataset to evaluate on
        evaluators=[correctness,relevance, groundedness],  # List of evaluators
        experiment_prefix="rag-doc-relevanceII",  # Prefix for the experiment name
        metadata={"version": "GraphRAG with Gemini EXP2"},  # Metadata for the experiment
    )

     # Print or log the results
    print("Experiment Results:", experiment_results)

if __name__ == "__main__":
    main()