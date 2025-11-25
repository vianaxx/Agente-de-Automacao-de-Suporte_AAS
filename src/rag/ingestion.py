import os
from langchain_community.document_loaders import DirectoryLoader
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter

DATA_PATH = "data/docs"
CHROMA_PATH = "data/vector_db"

"""
Script em Python é um pipeline de Ingestão de Dados para a 
criação de um Retrieval-Augmented Generation (RAG) System 
usando bibliotecas do ecossistema LangChain.
"""

def ingest_data():
    print("---1 - Carregando documentos ---")

    loader = DirectoryLoader(DATA_PATH, glob="**/*.md")
    documents = loader.load()

    # Breaks documents into smaller chunks (500 characters each with 50 character overlap)
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    #The overlap ensures context isn't lost at chunk boundaries—each chunk includes the last 50 characters of the previous chunk.
    texts = text_splitter.split_documents(documents)

    print(f"{len(texts)} documentos carregados")

    print("---2 - Criando embeddings com Hugging Face ---")

    # Use Hugging Face for embeddings (downloads model on first run)
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    # Store vectors in Chroma
    vector_store = Chroma.from_documents(
        texts,
        embeddings,
        persist_directory=CHROMA_PATH
    )
    print(f"Vetores armazenados em {CHROMA_PATH}")
    return vector_store

if __name__ == "__main__":
    # Garante que o diretório do DB exista
    os.makedirs(CHROMA_PATH, exist_ok=True)
    ingest_data()