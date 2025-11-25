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

    # Divide documentos em partes menores (500 caracteres cada com 50 caracteres de sobreposição).
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    # A sobreposição garante que o contexto não seja perdido nos limites entre os blocos — cada bloco inclui os últimos 50 caracteres do bloco anterior.
    texts = text_splitter.split_documents(documents)

    print(f"{len(texts)} documentos carregados")

    print("---2 - Criando embeddings com Hugging Face ---")

    # Usa o Hugging Face para gerar embeddings (o modelo é baixado na primeira execução).
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    # Armazena os vetores no 
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
