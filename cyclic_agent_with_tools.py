from langgraph.graph import StateGraph, MessagesState, START, END
from langchain_core.messages import HumanMessage, SystemMessage
from utilities.load_model import load_model


llm = load_model()


def llm_node(state: MessagesState) -> MessagesState:
    real_ai_response = llm.invoke(state["messages"])
    system_message = SystemMessage(content="You are a helpful assistant.")
    human_message = state.get("messages")[-1]
    state.get("messages").insert(0, system_message)
    return {"messages": [system_message, human_message, real_ai_response]}


graph = StateGraph(MessagesState)

graph.add_node("llm", llm_node)
graph.add_edge(START, "llm")
graph.add_edge("llm", END)
agent = graph.compile()

result = agent.invoke({"messages": [HumanMessage(content="How are you?")]})

print(result["messages"][-1].content[0].get("text"))
