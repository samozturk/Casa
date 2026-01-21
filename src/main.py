from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage


from langgraph.graph import StateGraph, START, END
from langgraph.prebuilt import ToolNode
from langgraph.prebuilt import tools_condition

from models import Rooms, State
from tools import classify_intent, route_by_intent, read_node, chat_node, select_note_to_read
from control_tools import control_parameter_node, control_policy_check, control_node

# TODO: create a config.ini


config = {
    "bedroom": "home/lights/bedroom",
    "office": "home/lights/office"
}


graph = StateGraph(State)

graph.add_edge(START, "intent")
graph.add_node("intent", classify_intent)
graph.add_node("read_node", read_node)
graph.add_node("chat_node", chat_node)
# Control Nodes
graph.add_node("control_parameter_node", control_parameter_node)
graph.add_node("control_policy_check", control_policy_check)
graph.add_node("control_node", control_node)
# Read Nodes
graph.add_node("decide_files_to_read", select_note_to_read)


graph.add_conditional_edges(
    "intent",
    route_by_intent,
    {
        "read_node": "read_node",
        "control_parameter_node": "control_parameter_node",
        "chat_node": "chat_node",
    },
)
# TODO: add this to the graph
graph.add_conditional_edges(
    "control_policy_check",
    lambda state: "ok" if state["policy_ok"] else "retry",
    {
        "ok": "control_node",
        "retry": "control_parameter_node",
    },
)
# Read Edges
graph.add_edge("read_node", "decide_files_to_read")
graph.add_edge("decide_files_to_read", END)

graph.add_edge("chat_node", END)
# Control Edges
graph.add_edge("control_parameter_node", "control_policy_check")
graph.add_edge("control_policy_check", "control_node")
graph.add_edge("control_node", END)



app = graph.compile()



# result = app.invoke({
#     "messages": [HumanMessage(content="Turn off the bedroom lights")],
#     "intent": None,
# })

# print(result)
# print(result['rooms'])