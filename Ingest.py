from langchain_openai import OpenAIEmbeddings
from langchain_community.document_loaders import  PyPDFLoader
from langchain_community.vectorstores import FAISS
from langchain_core.tools import create_retriever_tool
from langchain_text_splitters import RecursiveCharacterTextSplitter

from dotenv import load_dotenv
import os

class ingest:
    def __init__(self):
        self.__vectorstore = None
        self.__retriever_tool = None
        self.__embeddings = None
        self.__API_KEY = None
        self.__text_loader = None
        self.__document = None
        self.__spliter = RecursiveCharacterTextSplitter(chunk_size = 500, chunk_overlap = 50)
    
    def __set_APIKEY(self):
        try:
            load_dotenv("/home/dev/c++/data science lab/data science lab/langchain/.env")
            self.__API_KEY = os.getenv("openai_key")
        except Exception as e:
            print(f"Error setting API key: {e}")

    def __load_text(self,path: str,filename: str):
        try:
            self.__text_loader = PyPDFLoader(f"{path}/{filename}")
            self.__document = self.__text_loader.load()
        except Exception as e:
            print(f"Error loading text: {e}")

    def __split_text(self):
        try:
            if self.__document is None:
                raise ValueError("Text loader not set. call text loader function first.")
            self.__document = self.__spliter.split_documents(self.__document)
        except Exception as e:
            print(f"Split text failed: {e}")

    def __set_embeddings(self):
        try:
            if self.__API_KEY is None:
                raise ValueError("API key not set. Please set the API key before initializing embeddings.")
            self.__embeddings = OpenAIEmbeddings(model = "text-embedding-3-large", openai_api_key = self.__API_KEY)
        except Exception as e:
            print(f"Error setting embeddings: {e}")

    def __create_vectorstore(self):
        try:
            if self.__document is None:
                raise ValueError("Text loader not set. call text loader function first.")
            elif self.__embeddings is None:
                raise ValueError("Embeddings not set. call set_embeddings function first.")
            self.__vectorstore = FAISS.from_documents(self.__document,embedding = self.__embeddings)

            self.__retriever = self.__vectorstore.as_retriever(search_kwargs = {"k": 2})
            self.__retriever_tool = create_retriever_tool(self.__retriever, name = "kb_search", description = "use this tool to search the knowledge base")
            return self.__retriever_tool
        except Exception as e:
            print(f"Error: {e}")

    def run(self):
        try:
            self.__set_APIKEY()
            self.__load_text("/home/dev/c++/data science lab/data science lab/RAG/", "AIhealthcare.pdf")
            self.__split_text()
            self.__set_embeddings()
            retriever_tool = self.__create_vectorstore()
            return retriever_tool
        except Exception as e:
            print(f"Ingest Pipeline failed: {e}")
