from Ingest import ingest
from langchain.agents import create_agent
from langchain.chat_models import init_chat_model
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from prompt import DECISION_PROMPT,CLARIFY_PROMPT,RAG_PROMPT,DIRECT_PROMPT
from dotenv import load_dotenv
import os


class RAG:
    def __init__(self):
        self.__ingest_pipeline = ingest()
        self.__retriever_tool = self.__ingest_pipeline.run()
        self.__agent = None
        self.__model = None
        self.__API_KEY = None
    
    def init_model(self):
        load_dotenv("/home/dev/c++/data science lab/data science lab/langchain/.env")
        self.__API_KEY = os.getenv("openai_key")
        self.__model = init_chat_model(
            model = "gpt-3.5-turbo",
            model_provider = "openai",
            openai_api_key = self.__API_KEY
        )
    def __init_agent(self):
        try:
            if self.__model is None:
                raise ValueError("Model not initialized,call init_model function first.")
            self.__agent = create_agent(
                model = self.__model,
                tools = [self.__retriever_tool],
                system_message = SystemMessage(content="You are a helpful assistant. If the user asks any question related to healthcare, answer based on the knowledge base. Use kb_search when needed.")
            )
        except Exception as e:
            print(f"agent initialization failed: {e}")

    def invoke(self, query: str) -> str:
        if self.__agent is None:
            raise ValueError("Agent not initialized, call init_agent function first.")
        return self.__agent.invoke({
            "messages": HumanMessage(content = query)
        })
    
    def decide(self, query):
        prompt = DECISION_PROMPT.format(query=query)
        return self.__model.invoke(prompt).content.strip()

    def clarify(self, query):
        prompt = CLARIFY_PROMPT.format(query=query)
        return self.__model.invoke(prompt).content

    def retrieve_answer(self, query):
        docs = self.retriever.invoke(query)
        context = "\n".join([d.page_content for d in docs])

        prompt = RAG_PROMPT.format(context=context, query=query)
        return self.__model.invoke(prompt).content

  
    def direct_answer(self, query):
        return self.__model.invoke(query).content
