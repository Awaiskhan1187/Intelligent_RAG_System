from rag import RAG
from prompt import DECISION_PROMPT,CLARIFY_PROMPT,RAG_PROMPT,DIRECT_PROMPT
from typing import TypedDict
from langgraph.graph import StateGraph, END
from langchain_core.messages import AIMessage

rag = RAG()
rag.init_model()

class State(TypedDict):
    messages: list
    query: str
    route: str
    context: str

def query_analyzer(state: State):
    query = state["query"]
    route = rag.decide("query")
    return {**state, "route": route}

def clarify_node(state: State):
    print("clarify node: \n")
    response = rag.clarify(state["query"])
    return {**state, "messages": state["messages"] + [AIMessage(content=response)] }

def  retriever_node(state: State):
    print("retriever node: \n")
    docs = rag.retrieve_answer(state["query"])
    context = "\n".join([d.page_content for d in docs])
    return {**state, "context": context}


def decision_node(state: State):
    print("decision node: \n")
    if state["route"] == "clarify":
        return clarify_node(state)
    elif state["route"] == "retriever":
        answer =  retriever_node(state)
    else:
        answer  = rag.direct_answer(state["query"])
    
    return {**state,
            "messages": state["messages"] + [AIMessage(content = answer)]
            }

def build_graph():
    graph = StateGraph(State)

    graph.add_node("query_analyzer", query_analyzer)
    graph.add_node("decision", decision_node)
    
    graph.set_entry_point("query_analyzer")
    graph.add_edge("query_analyzer", "decision")
    graph.add_edge("decision", END)

    return graph.compile()


