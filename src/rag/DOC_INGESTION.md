Esse script em Python é um **pipeline de Ingestão de Dados (criação do banco de dados)** para a criação de um **Retrieval-Augmented Generation (RAG) System** usando bibliotecas do ecossistema LangChain.

-----

## Visão Geral do Mecanismo

O principal objetivo do script é pegar documentos de texto (arquivos Markdown) e transformá-los em uma representação numérica (*vetores* ou *embeddings*) para que possam ser facilmente pesquisados e recuperados por um Large Language Model (LLM) posteriormente.

Ele segue três etapas principais:

1.  **Carregar:** Ler os documentos brutos.
2.  **Dividir/Chunking:** Quebrar os documentos em pedaços menores.
3.  **Embed/Armazenar:** Converter os pedaços em vetores e salvá-los em um banco de dados vetorial.

-----

## Explicação Detalhada do Código

### 1\. Configurações Iniciais e Imports

```python
import os
from langchain_community.document_loaders import DirectoryLoader
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter

DATA_PATH = "data/docs"
CHROMA_PATH = "data/vector_db"

"""
Script para carregar os dados do data/docs/ no Vector DB. Execute este arquivo uma vez.
"""
```

* **Imports:** Importa as classes necessárias das bibliotecas LangChain (agora divididas em `langchain_community`, `langchain_huggingface`, `langchain_chroma`, etc.).
    * `os`: Para operações de sistema (criação de diretório).
    * `DirectoryLoader`: Classe para carregar documentos de um diretório.
    * `HuggingFaceEmbeddings`: Classe para gerar os vetores (embeddings) usando modelos do Hugging Face.
    * `Chroma`: O banco de dados vetorial escolhido para armazenar os vetores.
    * `RecursiveCharacterTextSplitter`: Uma estratégia para dividir o texto.
* **Constantes (`DATA_PATH`, `CHROMA_PATH`):** Definem onde os documentos de entrada estão e onde o banco de dados vetorial será salvo, respectivamente.

### 2\. Função Principal de Ingestão (`ingest_data`)

#### A. Carregamento dos Documentos (Loading)

```python
def ingest_data():
    print("---1 - Carregando documentos ---")

    loader = DirectoryLoader(DATA_PATH, glob="**/*.md")
    documents = loader.load()
```

* **`DirectoryLoader`:** Inicializa um carregador que busca arquivos no `DATA_PATH` (i.e., `data/docs`).
* **`glob="**/*.md"`:** Isso é um padrão de *wildcard* que instrui o carregador a buscar **todos** os arquivos com a extensão `.md` (Markdown) dentro do `DATA_PATH` e em quaisquer subdiretórios (`**/*`).
* **`loader.load()`:** Executa o carregamento, retornando uma lista de objetos `Document` do LangChain. Cada objeto contém o texto de um arquivo e seus metadados (como o caminho do arquivo original).

#### B. Divisão do Texto em Pedaços (Chunking)

```python
    # Divide documentos em partes menores (500 caracteres cada com 50 caracteres de sobreposição)
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    # A sobreposição garante que o contexto não seja perdido nos limites entre os blocos — cada bloco inclui os últimos 50 caracteres do bloco anterior.
    texts = text_splitter.split_documents(documents)

    print(f"{len(texts)} documentos carregados")
```

* **Mecanismo:** Modelos de embedding e LLMs têm limites de entrada (tokens/caracteres). Além disso, documentos grandes dificultam a pesquisa precisa. Por isso, os documentos são divididos em "chunks".
* **`RecursiveCharacterTextSplitter`:** Tenta dividir o texto usando uma lista de separadores (`\n\n`, `\n`, `     `, etc.) em ordem decrescente de granularidade. Isso ajuda a manter a integridade semântica, tentando não quebrar frases ou parágrafos no meio.
* **`chunk_size=500`:** O tamanho máximo de cada pedaço de texto é de **500 caracteres**.
* **`chunk_overlap=50`:** **Sobrelapagem** de 50 caracteres. Isso significa que os últimos 50 caracteres de um chunk são também os primeiros 50 caracteres do chunk seguinte.
    * **Por trás do script:** A sobrelapagem é crucial para garantir que o **contexto** não seja perdido na fronteira entre os pedaços. Se uma ideia importante for dividida no limite de dois chunks, o overlap ajuda a garantir que o LLM receba informações contextuais completas ao buscar um dos pedaços.

#### C. Criação e Armazenamento dos Vetores (Embedding and Storing)

```python
    print("---2 - Criando embeddings com Hugging Face ---")

    # Usa o Hugging Face para gerar embeddings (o modelo é baixado na primeira execução).
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    # Armazena os vetores no Chroma
    vector_store = Chroma.from_documents(
        texts,
        embeddings,
        persist_directory=CHROMA_PATH
    )
    print(f"Vetores armazenados em {CHROMA_PATH}")
    return vector_store
```

* **`HuggingFaceEmbeddings`:** Inicializa o modelo que fará a conversão de texto para vetor.
* **`model_name="sentence-transformers/all-MiniLM-L6-v2"`:** Este é um modelo de *Sentence Transformer* muito popular e eficiente.
    * **Por trás do script:** O modelo pega cada pedaço de texto (chunk) e o transforma em uma lista longa de números (*vetor*) em um espaço dimensional (por exemplo, 384 dimensões para este modelo). Esse vetor captura o **significado semântico** do texto. Textos com significados semelhantes terão vetores que estão próximos uns dos outros nesse espaço.
* **`Chroma.from_documents(...)`:** Esta é a etapa final e mais importante:
    * Pega a lista de **chunks de texto** (`texts`).
    * Usa o **modelo de embedding** (`embeddings`) para converter cada chunk em seu vetor correspondente.
    * Armazena o **vetor** e o **texto original** (e seus metadados) no banco de dados **Chroma** no caminho especificado (`CHROMA_PATH`).
* **`persist_directory=CHROMA_PATH`:** Garante que o banco de dados seja salvo no disco, permitindo que seja carregado novamente em outro script (o script de recuperação/geração) sem a necessidade de reprocessar os documentos.

### 3\. Bloco de Execução Principal

```python
if __name__ == "__main__":
    # Garante que o diretório do DB exista
    os.makedirs(CHROMA_PATH, exist_ok=True)
    ingest_data()
```

* **`if __name__ == "__main__":`:** Garante que o código dentro deste bloco só seja executado quando o script for rodado diretamente (e não quando for importado como um módulo).
* **`os.makedirs(CHROMA_PATH, exist_ok=True)`:** Cria o diretório de destino (`data/vector_db`) se ele ainda não existir.
* **`ingest_data()`:** Chama a função que executa todo o pipeline de carregamento, divisão e armazenamento.

-----

## Resumo do Fluxo de Recuperação (RAG)

Quando você for usar esse DB em um script de resposta:

1.  O usuário faz uma **pergunta** (ex: "Qual o processo X?").
2.  A **pergunta** também é transformada em um **vetor** usando o **MESMO** modelo de embedding.
3.  O banco de dados Chroma (`CHROMA_PATH`) é consultado, buscando os **vetores** de documentos que são **mais próximos** do vetor da pergunta (usando cálculo de **similaridade de cosseno**).
4.  O script recupera os **chunks de texto** correspondentes aos vetores mais próximos.
5.  Esses chunks de texto relevantes são injetados como **contexto** na *prompt* enviada ao LLM (ex: "Baseado no contexto abaixo, responda à pergunta: [Contexto: chunk 1, chunk 2, etc.] [Pergunta: Qual o processo X?]").
6.  O LLM gera uma resposta precisa, baseada na informação original dos seus documentos.
