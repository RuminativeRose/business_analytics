#!/usr/bin/env python3
'''
A basic business analytics software demonstrating the use of AI in programming techniques.
'''

from openai import OpenAI
# import anthropic # Not yet implemented

from pydantic import BaseModel, Field
from typing import List

# embeddings are not yet implemented, but Pinecone will be used
from pinecone import Pinecone 

from langsmith import Client, traceable, tracing_context
from langsmith.wrappers import wrap_openai

import sys, os
import logging

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())

# LLM Client Setup
openai.api_key = os.environ.get("OPENAI_API_KEY")
client = wrap_openai(openai.Client())

# # Pinecone and Vector Embeddings setup
INDEX_NAME = "business-analytics"
EMBEDDING_MODEL = "text-embedding-3-small"
pc = Pinecone(api_key=os.environ.get("PINECONE_API_KEY"))

# LangSmith client setup
langsmith_api_key = os.environ.get("LANGCHAIN_API_KEY")
langsmith_project = "business-analytics"
langsmith_client = Client(api_key=langsmith_api_key)

# Other Constants/Setup
CHAT_MODEL = "gpt-4o-mini-2024-07-18"

TO_SEARCH=["X", "Kalshi", "Bluesky", "Polymarket", "Instagram","Google"]

class Query(BaseModel):
    """Output specification/model for chained/HITL LLM usage."""
    financial_entities: List[str] = Field(description="One or more stocks or financial entities of interest")
    forecast_queries: List[str] = Field(description="Question(s) about the future of those stocks/financial entities")


#TODO: Static method decorator before or after tracing decorator?
class Embeddings:

    @staticmethod
    @traceable(name="load_documents")
    def load_documents():
        """Load all text documents from the letters directory."""
        documents = []
        script_dir = os.path.dirname(os.path.abspath(__file__))
        path = os.path.join(script_dir, "letters/*.txt")
        files = glob.glob(path)
        
        for file_path in files:
            with open(file_path, 'r',encoding="utf-8") as file:
                content = file.read()
                documents.append({"content": content, "metadata": {"source": file_path}})
        
        print(f"Found {len(documents)} letters")
        return documents

    @staticmethod
    @traceable(name="chunk_documents")
    def chunk_documents(documents, chunk_size=1000, chunk_overlap=200):
        """Split documents into smaller chunks for better processing."""
        chunks = []
        
        for doc in documents:
            content = doc["content"]
            metadata = doc["metadata"]
            
            # Simple text splitting - you can implement more sophisticated chunking if needed
            for i in range(0, len(content), chunk_size - chunk_overlap):
                if i > 0:
                    start = i - chunk_overlap
                else:
                    start = 0
                    
                chunk_content = content[start:start + chunk_size]
                if chunk_content:
                    chunks.append({"content": chunk_content, "metadata": metadata})
        
        return chunks

    @staticmethod
    @traceable(name="get_embeddings")
    def get_embeddings(texts: List[str]):
        """Generate embeddings for a list of texts using OpenAI."""
        response = openai.embeddings.create(
            input=texts,
            model=EMBEDDING_MODEL
        )
        return [embedding.embedding for embedding in response.data]

    @staticmethod
    @traceable(name="embed_documents")
    def embed_documents(chunks, namespace):
        """Embed documents and store them in Pinecone."""
        # Get Pinecone index
        index = pc.Index(INDEX_NAME)
        
        # Prepare batches (Pinecone usually works well with batches of ~100)
        batch_size = 100
        for i in range(0, len(chunks), batch_size):
            chunk_batch = chunks[i:i+batch_size]
            
            # Get text from each chunk
            texts = [chunk["content"] for chunk in chunk_batch]
            
            # Get embeddings
            embeddings = get_embeddings(texts)
            
            # Prepare data for Pinecone
            vectors = []
            for j, embedding in enumerate(embeddings):
                vectors.append({
                    "id": f"chunk_{i+j}",
                    "values": embedding[:1024],
                    "metadata": chunk_batch[j]["metadata"]
                })
            
            # Upsert to Pinecone
            index.upsert(vectors=vectors, namespace=namespace)

    @staticmethod
    @traceable(name="search_documents")
    def search_documents(query, namespace, top_k=5):
        """Search the vector store with the user query."""
        # Get query embedding
        query_embedding = get_embeddings([query])[0]
        
        # Search Pinecone
        index = pc.Index(INDEX_NAME)
        results = index.query(
            vector=query_embedding[:1024],
            top_k=top_k,
            namespace=namespace,
            include_metadata=True,
            include_values=False
        )
        
        # Get matched documents
        docs_with_scores = []
        for match in results["matches"]:
            # Load the document content based on the source file
            with open(match["metadata"]["source"], 'r',encoding="utf-8") as f:
                content = f.read()
            docs_with_scores.append((content, match["score"]))
        
        return docs_with_scores

    # Example: https://docs.smith.langchain.com/observability/how_to_guides/log_traces_to_project
    @staticmethod
    @traceable(name="ask_openai_rag",
            project_name=langsmith_project,
            run_type="llm")
    def ask_openai_rag(query, documents):
        """Ask OpenAI a question with context from the documents."""
        # Join all documents into a single context string
        context = "\n\n".join([doc for doc, _ in documents])
        
        # Create messages for OpenAI
        messages = [
            {"role": "system", "content": "Provide an answer to the user's query about the status of a stock."
                                  "Relevant documents will be provided."
                                  "Use those documents, social media, and prediction markets to best answer the question."},
            {"role": "system", "content": f"Documents: {context}"},
            {"role": "user", "content": query}
        ]
        
        response = client.chat.completions.create(
            model=CHAT_MODEL,
            messages=messages
        )
        
        return response.choices[0].message.content


# Function from chapter 5 hitl assignment
def get_human_confirmation(self, prompt: str) -> bool:
    """Get human confirmation for a suggestion."""
    while True:
        choice = input(f"{prompt} (y/n): ").lower().strip()
        if choice in ['y', 'n']:
            return choice == 'y'
        print("Please enter 'y' or 'n'")



@traceable(name="ask_openai_hitl",
        project_name=langsmith_project,
        run_type="llm")
def ask_openai_hitl(question: str):
    prompt = f"""You are a financial analyst who predicts future performance of stocks, funds, and companies based on trends on social media and prediction markets.
            You'll use {', '.join(TO_SEARCH)} as some of your sources to answer the user's query about a financial entity, its future performance, and whether to invest. 
            First respond by (1) identifying each stock or company or financial device of interest and (2) the specific question(s) the user has."""
    messages = [
        {
            "role": "system",
            "content": prompt,
        },
        {
            "role": "user",
            "content": f"Question: {question}\n",
        },
    ]
    chat_completion = client.chat.responses.parse(
        model="gpt-4o-mini-2024-07-18",
        input=messages,
        text_format=Query
        )
    return chat_completion.output_parsed

@traceable(name="ask_openai",
        project_name=langsmith_project,
        run_type="llm")
def ask_openai(query: Query):
    messages = [
        {
            "role": "system",
            "content": f"""You are a financial analyst who predicts future performance of stocks, funds, and companies based on trends on social media and prediction markets.
            You'll use {', '.join(TO_SEARCH)} as some of your sources to answer the user's query about a financial entity, its future performance, and whether to invest. """,
        },
        {
            "role": "user",
            "content": f"""The one or more companies, stocks, financial entities in question: {', '.join(query.financial_entities)}
            The user's question(s): '{'\', \''.join(query.forecast_queries)}'""",
            
        },
    ]
    chat_completion = client.chat.completions.create(
        model=CHAT_MODEL, messages=messages
    )
    return chat_completion.choices[0].message.content

def main():
    with tracing_context(enabled=True, client=langsmith_client, project_name=langsmith_project):
        while True:
            ### replace
            question = input('Enter your query about a stock, company, or financial entity.')
            logger.info('User inputted question "%s"',question)
            query = ask_openai_hitl(question)
            logger.info('Pydantic model %s generated',repr(query))
            prompt = f"Did you ask '{'\', \''.join(query.forecast_queries)}', about {', '.join(query.financial_entities)}?"
            if not get_human_confirmation(prompt):
                # try one more time
                question = input('Enter your query about a stock, company, or financial entity.')
                query = ask_openai_hitl(question)
                logger.info('User inputted question "%s"',question)
                logger.info('Pydantic model %s generated',repr(query))
            reply = ask_openai(query)
            print(reply+'\n')
            
            ans=input("Press 'q' to quit or any other key to repeat.")
            if ans.casefold() == 'q':
                break
            


if __name__ == "__main__":
    logging.config(filename="main.log",level=logging.INFO)
    sys.exit(main())