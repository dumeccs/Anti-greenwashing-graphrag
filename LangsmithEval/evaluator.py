# evaluator.py
from typing_extensions import Annotated, TypedDict
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
import os

# Load environment variables
from dotenv import load_dotenv
load_dotenv()


# Grade output schema for Correctness
class CorrectnessGrade(TypedDict):
    explanation: Annotated[str, ..., "Explain your reasoning for the score"]
    correct: Annotated[bool, ..., "True if the answer is correct, False otherwise."]

# Grade output schema for Relevance
class RelevanceGrade(TypedDict):
    explanation: Annotated[str, ..., "Explain your reasoning for the score"]
    relevant: Annotated[bool, ..., "Provide the score on whether the answer addresses the question"]


# Grade output schema for Groundedness
class GroundednessGrade(TypedDict):
    explanation: Annotated[str, ..., "Explain your reasoning for the score"]
    grounded: Annotated[bool, ..., "True if the answer is grounded in the provided context, False otherwise."]


# Grade output schema
class RetrievalRelevanceGrade(TypedDict):
    explanation: Annotated[str, ..., "Explain your reasoning for the score"]
    relevant: Annotated[bool, ..., "True if the retrieved documents are relevant to the question, False otherwise"]

# Grade prompt for Correctness
correctness_instructions = """You are a teacher grading a quiz. 

You will be given a QUESTION, the GROUND TRUTH (correct) ANSWER, and the STUDENT ANSWER. 

Here is the grade criteria to follow:
(1) Grade the student answers based ONLY on their factual accuracy relative to the ground truth answer. 
(2) Ensure that the student answer does not contain any conflicting statements.
(3) It is OK if the student answer contains more information than the ground truth answer, as long as it is factually accurate relative to the  ground truth answer.

Correctness:
A correctness value of True means that the student's answer meets all of the criteria.
A correctness value of False means that the student's answer does not meet all of the criteria.

Explain your reasoning in a step-by-step manner to ensure your reasoning and conclusion are correct. 

At the end of your response, explicitly state:
- "correctness value is True" if the answer is correct.
- "correctness value is False" if the answer is incorrect.

Avoid simply stating the correct answer at the outset."""

# Grade prompt for Relevance
relevance_instructions = """You are a teacher grading a quiz. 

You will be given a QUESTION and a STUDENT ANSWER. 

Here is the grade criteria to follow:
(1) Ensure the STUDENT ANSWER is concise and relevant to the QUESTION.
(2) Ensure the STUDENT ANSWER helps to answer the QUESTION.
(3) It is OK if the student answer contains more information, as long as it is factually accurate relative to the  ground truth answer.

Relevance:
A relevance value of True means that the student's answer meets all of the criteria.
A relevance value of False means that the student's answer does not meet all of the criteria.

Explain your reasoning in a step-by-step manner to ensure your reasoning and conclusion are correct. 

At the end of your response, explicitly state:
- "relevance value is True" if the answer is relevant.
- "relevance value is False" if the answer is irrelevant.

Avoid simply stating the correct answer at the outset."""


grounded_instructions = """You are a teacher grading a quiz. 

You will be given FACTS and a STUDENT ANSWER. 

Here is the grade criteria to follow:
(1) Ensure the STUDENT ANSWER is grounded in the FACTS. 
(2) Ensure the STUDENT ANSWER does not contain "hallucinated" information outside the scope of the FACTS.

Grounded:
A grounded value of True means that the student's answer meets all of the criteria.
A grounded value of False means that the student's answer does not meet all of the criteria.

Explain your reasoning in a step-by-step manner to ensure your reasoning and conclusion are correct. 

At the end of your response, explicitly state:
- "grounded value is True" if the answer is grounded.
- "grounded value is False" if the answer is ungrounded.

Avoid simply stating the correct answer at the outset."""

# Initialize Gemini model
grader_llm = ChatGoogleGenerativeAI(model="gemini-1.5-pro",
    temperature=0.3,
    max_tokens=None,
    timeout=None,
    max_retries=2,
    google_api_key=os.getenv("GEMINI_API_KEY"))



def correctness(inputs: dict, outputs: dict, reference_outputs: dict) -> dict:
    """An evaluator for RAG answer accuracy."""
    answers = f"""      QUESTION: {inputs['question']}
GROUND TRUTH ANSWER: {reference_outputs['answer']}
STUDENT ANSWER: {outputs['answer']}"""

    # Create a prompt template for Correctness
    prompt = ChatPromptTemplate.from_messages([
        ("system", correctness_instructions),
        ("user", answers),
    ])

    # Chain the prompt, model, and output parser
    chain = prompt | grader_llm | StrOutputParser()

    # Run evaluator
    response = chain.invoke({})
    
    # Debug: Print the raw response
    print("Raw Gemini Response:", response)
    
    # Parse the response
    try:
        # Extract the explanation and correctness from the response
        explanation = response  # Use the entire response as the explanation
        correct = "correctness value is True" in response  # Check if the response indicates correctness
        
        # Return the result in the format LangSmith expects
        return {
            "key": "correctness",
            "score": 1.0 if correct else 0.0,  # Binary score (1.0 for correct, 0.0 for incorrect)
            "comment": explanation,  # Use the entire response as the comment
        }
    except Exception as e:
        print(f"Error parsing Gemini response: {e}")
        return {
            "key": "correctness",
            "score": 0.0,  # Default to incorrect if parsing fails
            "comment": "Error parsing response",
        }


# def relevance(inputs: dict, outputs: dict) -> bool:
#     """An evaluator for RAG answer relevance"""
#     answer = f"""      QUESTION: {inputs['question']}
# STUDENT ANSWER: {outputs['answer']}"""

#     # Create a prompt template for Relevance
#     prompt = ChatPromptTemplate.from_messages([
#         ("system", relevance_instructions),
#         ("user", answer),
#     ])

#     # Chain the prompt, model, and output parser
#     chain = prompt | grader_llm | StrOutputParser()

#     # Run evaluator
#     response = chain.invoke({})
    
#     # Parse the response (assuming it returns a JSON-like string)
#     try:
#         # Extract the explanation and relevance from the response
#         explanation = response.split("explanation: ")[1].split("\n")[0]
#         relevant = "True" in response.split("relevant: ")[1].split("\n")[0]
#         return {"explanation": explanation, "relevant": relevant}
#     except Exception as e:
#         print(f"Error parsing Gemini response: {e}")
#         return {"explanation": "Error parsing response", "relevant": False}
    
#--------------------------------------------------------------
def relevance(inputs: dict, outputs: dict) -> dict:
    """An evaluator for RAG answer relevance."""
    answer = f"""      QUESTION: {inputs['question']}
STUDENT ANSWER: {outputs['answer']}"""

    # Create a prompt template for Relevance
    prompt = ChatPromptTemplate.from_messages([
        ("system", relevance_instructions),
        ("user", answer),
    ])

    # Chain the prompt, model, and output parser
    chain = prompt | grader_llm | StrOutputParser()

    # Run evaluator
    response = chain.invoke({})
    
    # Debug: Print the raw response
    print("Raw Gemini Response (Relevance):", response)
    
    # Parse the response
    try:
        # Extract the explanation and relevance from the response
        explanation = response  # Use the entire response as the explanation
        relevant = "relevance value is True" in response  # Check if the response indicates relevance
        
        # Return the result in the format LangSmith expects
        return {
            "key": "relevance",
            "score": 1.0 if relevant else 0.0,  # Binary score (1.0 for relevant, 0.0 for irrelevant)
            "comment": explanation,  # Use the entire response as the comment
        }
    except Exception as e:
        print(f"Error parsing Gemini response: {e}")
        return {
            "key": "relevance",
            "score": 0.0,  # Default to irrelevant if parsing fails
            "comment": "Error parsing response",
        }


    

# def groundedness(inputs: dict, outputs: dict) -> dict:
#     """An evaluator for RAG answer groundedness."""
#     # Extract documents and student answer
#     doc_string = "".join(doc.page_content for doc in outputs["documents"])
#     answer = f"""      FACTS: {doc_string}
# STUDENT ANSWER: {outputs['answer']}"""

#     # Create a prompt template for Groundedness
#     prompt = ChatPromptTemplate.from_messages([
#         ("system", grounded_instructions),
#         ("user", answer),
#     ])

#     # Chain the prompt, model, and output parser
#     chain = prompt | grader_llm | StrOutputParser()

#     # Run evaluator
#     response = chain.invoke({})
    
#     # Debug: Print the raw response
#     print("Raw Gemini Response (Groundedness):", response)
    
#     # Parse the response
#     try:
#         # Extract the explanation and groundedness from the response
#         explanation = response  # Use the entire response as the explanation
#         grounded = "grounded value is True" in response  # Check if the response indicates groundedness
        
#         # Return the result in the format LangSmith expects
#         return {
#             "key": "groundedness",
#             "score": 1.0 if grounded else 0.0,  # Binary score (1.0 for grounded, 0.0 for ungrounded)
#             "comment": explanation,  # Use the entire response as the comment
#         }
#     except Exception as e:
#         print(f"Error parsing Gemini response: {e}")
#         return {
#             "key": "groundedness",
#             "score": 0.0,  # Default to ungrounded if parsing fails
#             "comment": "Error parsing response",
#         }

def groundedness(inputs: dict, outputs: dict) -> dict:
    """An evaluator for RAG answer groundedness."""
    # Extract documents and student answer
    if "documents" not in outputs:
        return {
            "key": "groundedness",
            "score": 0.0,  # Default to ungrounded if documents are missing
            "comment": "No documents provided in the outputs.",
        }
    
    # Construct the document string
    try:
        doc_string = "".join(doc for doc in outputs["documents"])  # Assuming documents are plain text
    except Exception as e:
        print(f"Error constructing document string: {e}")
        return {
            "key": "groundedness",
            "score": 0.0,  # Default to ungrounded if documents are invalid
            "comment": "Error constructing document string.",
        }

    answer = f"""      FACTS: {doc_string}
STUDENT ANSWER: {outputs['answer']}"""

    # Create a prompt template for Groundedness
    prompt = ChatPromptTemplate.from_messages([
        ("system", grounded_instructions),
        ("user", answer),
    ])

    # Chain the prompt, model, and output parser
    chain = prompt | grader_llm | StrOutputParser()

    # Run evaluator
    response = chain.invoke({})
    
    # Debug: Print the raw response
    print("Raw Gemini Response (Groundedness):", response)
    
    # Parse the response
    try:
        # Extract the explanation and groundedness from the response
        explanation = response  # Use the entire response as the explanation
        grounded = "grounded value is True" in response  # Check if the response indicates groundedness
        
        # Return the result in the format LangSmith expects
        return {
            "key": "groundedness",
            "score": 1.0 if grounded else 0.0,  # Binary score (1.0 for grounded, 0.0 for ungrounded)
            "comment": explanation,  # Use the entire response as the comment
        }
    except Exception as e:
        print(f"Error parsing Gemini response: {e}")
        return {
            "key": "groundedness",
            "score": 0.0,  # Default to ungrounded if parsing fails
            "comment": "Error parsing response",
        }
    


   