"""
LLM
"""
from google import genai
from .prompts import context_providing_prompt, cypher_generating_prompt
import os
import json
from google.oauth2 import service_account


ONTOLOGY = """
@prefix : <http://neo4j.com/voc/greenwashing#> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix xml: <http://www.w3.org/XML/1998/namespace> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix schema: <https://schema.org/> .
@base <http://neo4j.com/voc/greenwashing#> .

<http://neo4j.com/voc/greenwashing#> 
    rdf:type owl:Ontology ;
    owl:imports <https://schema.org/version/latest/schemaorg-current-https.ttl> ;
    owl:versionInfo "1.0" ;
    rdfs:label "Greenwashing Ontology" ;
    rdfs:comment "An ontology for describing and analyzing greenwashing claims in financial products and services." .

#################################################################
#    Classes
#################################################################

###  http://neo4j.com/voc/greenwashing#Rule
:Rule 
    rdf:type owl:Class ;
    rdfs:comment "A regulatory rule or guideline related to greenwashing or sustainability." ;
    rdfs:subClassOf schema:Legislation .

###  http://neo4j.com/voc/greenwashing#Firm
:Firm 
    rdf:type owl:Class ;
    rdfs:comment "A company or organization that offers financial products or services." ;
    rdfs:subClassOf schema:Organization .

###  http://neo4j.com/voc/greenwashing#Product
:Product 
    rdf:type owl:Class ;
    rdfs:comment "A financial product or service offered by a firm." ;
    rdfs:subClassOf schema:FinancialProduct .

###  http://neo4j.com/voc/greenwashing#Claim
:Claim 
    rdf:type owl:Class ;
    rdfs:comment "A sustainability-related claim made by a firm about a product or service." ;
    rdfs:subClassOf schema:CreativeWork ;
    rdfs:subClassOf [
        rdf:type owl:Restriction ;
        owl:onProperty :supportedBy ;
        owl:minCardinality "1"^^xsd:nonNegativeInteger
    ] .

###  http://neo4j.com/voc/greenwashing#Evidence
:Evidence 
    rdf:type owl:Class ;
    rdfs:comment "Evidence or data that supports a sustainability-related claim." ;
    rdfs:subClassOf schema:Dataset .

###  http://neo4j.com/voc/greenwashing#Stakeholder
:Stakeholder 
    rdf:type owl:Class ;
    rdfs:comment "A person or entity that interacts with a firm or product (e.g., consumers, regulators)." ;
    rdfs:subClassOf schema:Person .

###  http://neo4j.com/voc/greenwashing#SustainabilityCharacteristic
:SustainabilityCharacteristic 
    rdf:type owl:Class ;
    rdfs:comment "A characteristic of a product or service related to sustainability (e.g., environmental, social)." ;
    rdfs:subClassOf schema:Property .

#################################################################
#    Object Properties
#################################################################

###  http://neo4j.com/voc/greenwashing#appliesTo
:appliesTo 
    rdf:type owl:ObjectProperty ;
    rdfs:comment "Connects a Rule to the Firm it applies to." ;
    rdfs:domain :Rule ;
    rdfs:range :Firm ;
    owl:inverseOf :subjectTo .

###  http://neo4j.com/voc/greenwashing#makes
:makes 
    rdf:type owl:ObjectProperty ;
    rdfs:comment "Connects a Firm to a Claim it makes about a Product." ;
    rdfs:domain :Firm ;
    rdfs:range :Claim ;
    owl:inverseOf :madeBy .

###  http://neo4j.com/voc/greenwashing#supportedBy
:supportedBy 
    rdf:type owl:ObjectProperty ;
    rdfs:comment "Connects a Claim to the Evidence that supports it." ;
    rdfs:domain :Claim ;
    rdfs:range :Evidence ;
    owl:inverseOf :supports .

###  http://neo4j.com/voc/greenwashing#has
:has 
    rdf:type owl:ObjectProperty ;
    rdfs:comment "Connects a Product to its sustainability characteristics or features." ;
    rdfs:domain :Product ;
    rdfs:range :SustainabilityCharacteristic .

###  http://neo4j.com/voc/greenwashing#interactsWith
:interactsWith 
    rdf:type owl:ObjectProperty ;
    rdfs:comment "Connects a Stakeholder to a Product or Firm they interact with." ;
    rdfs:domain :Stakeholder ;
    rdfs:range [ 
        rdf:type owl:Class ;
        owl:unionOf ( :Product :Firm )
    ] .

#################################################################
#    Data Properties
#################################################################

###  http://neo4j.com/voc/greenwashing#description
:description 
    rdf:type owl:DatatypeProperty ;
    rdfs:comment "A textual description of a Claim, Rule, or Product." ;
    rdfs:range xsd:string ;
    rdfs:domain [
        rdf:type owl:Class ;
        owl:unionOf ( :Claim :Rule :Product )
    ] .

###  http://neo4j.com/voc/greenwashing#name
:name 
    rdf:type owl:DatatypeProperty ;
    rdfs:comment "The name of a Firm, Product, or Rule." ;
    rdfs:range xsd:string ;
    rdfs:domain [
        rdf:type owl:Class ;
        owl:unionOf ( :Firm :Product :Rule )
    ] .

###  http://neo4j.com/voc/greenwashing#claimStatus
:claimStatus
    rdf:type owl:DatatypeProperty ;
    rdfs:domain :Claim ;
    rdfs:range [
        rdf:type rdfs:Datatype ;
        owl:oneOf ( "Verified" "Pending" "Disputed" "Withdrawn" )
    ] .

###  http://neo4j.com/voc/greenwashing#claimDate
:claimDate
    rdf:type owl:DatatypeProperty ;
    rdfs:domain :Claim ;
    rdfs:range xsd:dateTime .

###  http://neo4j.com/voc/greenwashing#evidenceDate
:dateCollected
    rdf:type owl:DatatypeProperty ;
    rdfs:domain :Evidence ;
    rdfs:range xsd:dateTime .

###  http://neo4j.com/voc/greenwashing#validityPeriod
:validityPeriod
    rdf:type owl:DatatypeProperty ;
    rdfs:domain :Evidence ;
    rdfs:range xsd:duration .

###  http://neo4j.com/voc/greenwashing#characteristicType
:characteristicType
    rdf:type owl:DatatypeProperty ;
    rdfs:domain :SustainabilityCharacteristic ;
    rdfs:range [
        rdf:type rdfs:Datatype ;
        owl:oneOf ( "Environmental" "Social" "Governance" )
    ] .

###  http://neo4j.com/voc/greenwashing#jurisdiction
:jurisdiction
    rdf:type owl:DatatypeProperty ;
    rdfs:domain :Rule ;
    rdfs:range xsd:string .

###  http://neo4j.com/voc/greenwashing#effectiveDate
:effectiveDate
    rdf:type owl:DatatypeProperty ;
    rdfs:domain :Rule ;
    rdfs:range xsd:date .

###  http://neo4j.com/voc/greenwashing#productCategory
:productCategory
    rdf:type owl:DatatypeProperty ;
    rdfs:domain :Product ;
    rdfs:range xsd:string .

###  http://neo4j.com/voc/greenwashing#sustainabilityRating
:sustainabilityRating
    rdf:type owl:DatatypeProperty ;
    rdfs:domain :Product ;
    rdfs:range xsd:integer ;
    rdfs:comment "Sustainability rating on a scale (e.g., 1-5)" .

###  http://neo4j.com/voc/greenwashing#stakeholderType
:stakeholderType
    rdf:type owl:DatatypeProperty ;
    rdfs:domain :Stakeholder ;
    rdfs:range [
        rdf:type rdfs:Datatype ;
        owl:oneOf ( "Regulator" "Consumer" "Investor" "NGO" )
    ] .
"""

class LLM:
    """
    LLM
    """
    def __init__(self):
         # Read service account JSON from Railway environment variable
        service_account_info = json.loads(os.environ["GOOGLE_APPLICATION_CREDENTIALS"])

         # Create a temporary file to store credentials
        tmp_path = "/tmp/gcp-service-account.json"
        with open(tmp_path, "w") as temp_file:
            json.dump(service_account_info, temp_file)

        # Set GOOGLE_APPLICATION_CREDENTIALS to the temporary file path
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = tmp_path

        self.credentials = service_account.Credentials.from_service_account_info(service_account_info)

        self.model = genai.Client(
            vertexai=True,
            location="us-central1",
            project="gen-lang-client-0902554404"
    )

    def respond(self, question: str, vector_context: str, graph_context: str):
        """
        Answering a question with the provided context
        """
        prompt = context_providing_prompt.invoke({
            "question": question, 
            "vector_context": vector_context,
            "graph_context": graph_context,
        })
        return self.model.models.generate_content_stream(model="gemini-1.5-pro-002", contents=prompt.to_string())


    def generate_cypher(self, query: str):
        """
        Generating cypher queryies relevant to the user's query
        """
        prompt = cypher_generating_prompt.invoke({
            "ontology": ONTOLOGY,
            "query": query
        })

        response = self.model.models.generate_content(
            model="gemini-2.0-pro-exp-02-05",
            contents=prompt.to_string()
        )

        response = response.text.strip("```cypher").strip()
        return response
