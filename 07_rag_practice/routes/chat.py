from fastapi import APIRouter
from dotenv import load_dotenv
import os
load_dotenv()
from openai import OpenAI
from langchain_qdrant import QdrantVectorStore
from langchain_google_genai import GoogleGenerativeAIEmbeddings


router = APIRouter(
    prefix="/chat",
    tags=["Query"],
)

client = OpenAI(
    api_key= os.getenv("GEMINI_API_KEY"),
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

# Google Gemini embedding model
embeddings = GoogleGenerativeAIEmbeddings(
    model="gemini-embedding-2"
)

vector_store = QdrantVectorStore.from_existing_collection(
    embedding=embeddings,
    url="http://localhost:6333",
    collection_name="chunks"
)

@router.post("/query")
def get_answer(query: str):
    """
    Get an answer to a query using the RAG approach.
    """
    # Retrieve relevant documents from the vector store
    search_results = vector_store.similarity_search(query)

    context = " ".join(
        [
            f"[Page {result.metadata.get('page', 'unknown')}] {result.page_content}"
            for result in search_results
        ]
    )

    SYSTEM_PROMPT = f"""You are a helpful assistant. Use the following pieces of retrieved context to answer the question. If context is not sufficient, say "I don't know.
     Also include page number of the context at the end of your answer if applicable. Mention it in the answer in the following format: (Page number: X). If there are multiple pages, mention all of them in the answer in the following format: (Page numbers: X, Y, Z).

    Context: {context}
    """

    response = client.chat.completions.create(
        model="gemini-3.5-flash-lite",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": query},
        ],
    )

    return {
        "query": query,
        "answer": response.choices[0].message.content
    }




