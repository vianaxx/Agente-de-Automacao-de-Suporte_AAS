import os
from langchain_community.llms import Ollama
from ollama import Client

LL_CLOUD_MODEL = "gpt-oss:120b-cloud"
HOST_URL = "https://ollama.com"

class OllamaCloudLLM(Ollama):
    """
    Classe para conectar ao OLLAM CLOUD via API KEY
    """
    @property
    def _get_api_client(self):
        #LÊ A CHAVE DE AMBIENTE
        ollama_api_key = os.environ["OLLAMA_API_KEY"]
        if not ollama_api_key:
            raise ValueError("OLLAMA_API_KEY NÃO DEFINIDA NO .ENV")

        return Client(
            host=HOST_URL,
            headers={"Authorization": f"Bearer {ollama_api_key}"}
        )

# Instancia o LLM
llm = OllamaCloudLLM(
    model = LL_CLOUD_MODEL,
    temperature=0.0,
)

