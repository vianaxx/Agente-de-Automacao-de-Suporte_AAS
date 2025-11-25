from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_core.vectorstores import VectorStoreRetriever

CHROMA_PATH = "data/vector_db"

def get_retriever() -> VectorStoreRetriever:
    """Carrega o Vector DB e retorna um retriever"""
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"  # Use full path
    )

    vectorstore = Chroma(
        persist_directory=CHROMA_PATH,
        embedding_function=embeddings,
    )

    return vectorstore.as_retriever(search_kwargs={"k": 2})