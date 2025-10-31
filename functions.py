# !pip3 install --upgrade --quiet langchain langchain-community langchain-openai chromadb langchain_experimental
# !pip3 install --upgrade --quiet pypdf pandas streamlit python-dotenv
# !pip3 install tabulate

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_chroma import Chroma
from langchain_core.runnables import RunnablePassthrough
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field

def connect_chat_openai(key):
    llm = ChatOpenAI(model="gpt-4o", api_key=key)
    return llm

def get_embedding_function(apikey):
    embeddings = OpenAIEmbeddings(
        model="text-embedding-3-small",
        openai_api_key=apikey
    )
    return embeddings


def load_vectorstore(doc, embeddingfunction, testdb):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1500,
        chunk_overlap=200,
        length_function=len
    )

    chunks = text_splitter.split_text(doc)

    vectorstore = Chroma.from_texts(
        texts=chunks,
        embedding=embeddingfunction,
        persist_directory=testdb
    )

    return vectorstore


class ExtractInfo(BaseModel):
    title: str = Field(description="Title of the document")
    summary: str = Field(description="Summary of the document")
    year: int = Field(description="Year of the publication of the document")
    document_author: str = Field(description="Names of the auther")


def prompt(vecorstore, llm):
    PROMPT_TEMPLATE = """
    {context}

    Answer the question based on the above context: {question}
    """

    retriever = vecorstore.as_retriever(search_kwargs={"k": 3})

    prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)

    rag_langchain = (
            {
                "context": retriever,
                "question": RunnablePassthrough()
            }
            | prompt_template
            | llm.with_structured_output(ExtractInfo, strict=True)
    )
    structured_response = rag_langchain.invoke("Give me the title, summary, year, author of the document.")
    return structured_response

