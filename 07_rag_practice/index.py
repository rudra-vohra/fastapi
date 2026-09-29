from dotenv import load_dotenv
from pathlib import Path
import time
load_dotenv()
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_qdrant import QdrantVectorStore
from langchain_google_genai import GoogleGenerativeAIEmbeddings

# PDF path
path = Path(__file__).parent / "nodejs.pdf"

loader = PyPDFLoader(file_path=path)
docs = loader.load()

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size = 1000,
    chunk_overlap = 400
)

chunks = text_splitter.split_documents(docs)

embedding = GoogleGenerativeAIEmbeddings(
    model = 'gemini-embedding-2',
)
batch_size = 10
delay = 8

first_batch = chunks[:batch_size]

vector_store = QdrantVectorStore.from_documents(
    documents = first_batch,
    embedding=embedding,
    url = 'http://localhost:6333',
    collection_name = 'chunks'
)

# Add remaining batches
for i in range(batch_size, len(chunks), batch_size):

    batch = chunks[i:i + batch_size]

    vector_store.add_documents(batch)

    processed = min(i + batch_size, len(chunks))

    print(f"Processed {processed}/{len(chunks)} chunks")

    # Throttle API requests
    if processed < len(chunks):
        print(f"Waiting {delay} seconds...")
        time.sleep(delay)

print("Indexing of documents done!")



