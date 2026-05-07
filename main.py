from graph import build_graph
from langchain_core.messages import HumanMessage

def main():

    while True:
        query = input("PROMPT :")

        if query.lower() == "exit" or query.lower() == "quit":
            break
        app = build_graph()
        
        result = app.invoke({
            "messages": [HumanMessage(content = query)],
            "query": query,
            "route": "",
            "context": "",
        })
        
        history = result["messages"]
        print(f"RESPONSE : {history[-1].content} \n")

if __name__ == "__main__":
    main()