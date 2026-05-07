<h1 align = center>INTELLIGENT RAG AGENT<h1>

<h2>tools:</h2>
<p>from typing import TypedDict<br/>
from langchain_core.messages import SystemMessage,HumanMessage,AIMessage<br/>
from langgraph.graph import StateGraph, END<br/>
from langchain.agent import create_agent<br/>
from langchain.chat_model import init_chat_model<br/>
from langchain_openai import OpenAIEmbeddings<br/>
from langchain_community.document_loaders import  PyPDFLoader<br/>
from langchain_community.vectorstores import FAISS<br/>
from langchain_core.tools import create_retriever_tool<br/>
from langchain_text_splitters import RecursiveCharacterTextSplitter<br/>
</p>
<br/>
<br/>
User Query<br/>
   ↓<br/>
Analyzer Node<br/>
   ↓<br/>
Decision Node<br/>
   ↓
 ├── Clarify User<br/>
 ├── Retrieve from FAISS<br/>
 └── Direct Answer<br/>

 <h1>Discription</h1>
 User query -> user input prompt at this stage, this is starting of this agent<br>
 Analyzer Node -> this analyze the query either the query is correct or not.<br>
 Decision Node -> This node take a decision to perform a task like should retrieve from vector database , direct answer or ask for clarification 

