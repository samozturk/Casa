from typing import TypedDict, List, Literal, Optional
from langchain_core.messages import BaseMessage, SystemMessage
from pydantic import BaseModel
from langchain_core.output_parsers import PydanticOutputParser
from typing import TypedDict, List, Any, get_args

from langchain_ollama import ChatOllama
from langchain.tools import tool
from langchain_core.messages import HumanMessage

from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode
from langgraph.prebuilt import tools_condition
import os

from models import Rooms, State, Room, Topic, Status
from prompts import room_parser, llm, INTENT_PROMPT, CONTROL_PARAMETER_PROMPT, READ_FILE_SELECTION_PROMPT
from utils.utils import publish_mqtt_message

# llm = ChatOllama(
#     model="llama70b",
#     temperature=0,
# )

def classify_intent(state: State):
    response = llm.invoke(
        [INTENT_PROMPT] + state["messages"]
    )

    intent = response.content.strip().lower()

    return {
        "intent": intent,
        "messages": state["messages"] + [response],
    }


def route_by_intent(state: State) -> str:
    intent = state.get("intent")

    if intent == "read":
        return "read_node"
    if intent == "control":
        return "control_parameter_node"

    return "chat_node"


def read_node(state: State):
    print("→ READ")
    return state

def chat_node(state: State):
    print("→ CHAT")
    return state





# Read Tools
# 1. Convert the natural language to db query
# 2. Run the query and get the result
# 3. Embed the result to a prompt
OBSIDIAN_VAULT_PATH = "/Users/sam/Documents/Obsidian Vault/Casa"
def select_note_to_read(state: State):
    files = os.listdir(OBSIDIAN_VAULT_PATH)
    response = llm.invoke(
        [READ_FILE_SELECTION_PROMPT,
        SystemMessage(content=f"Here is the list of files: {files}. Select the most relevant file to read.")] + state["messages"]
    )
    filename = response.content.strip()
    return {
        "filename": filename,
        "messages": state["messages"] + [response]
    }

def read_note(state: State, filename: str) -> str:
    file_path = os.path.join(OBSIDIAN_VAULT_PATH, filename)
    try:
        with open(file_path, 'r') as file:
            content = file.read()
        return content
    except FileNotFoundError:
        return "File not found."

# Write Tools
# 1. Convert the natural language to db query
# 2. Run the query and get the result
# 3. Embed the result to a prompt