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
from prompts import room_parser, INTENT_PROMPT, CONTROL_PARAMETER_PROMPT
from utils import publish_mqtt_message

llm = ChatOllama(
    model="llama70b",
    temperature=0,
)

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


# Control Tools
def control_parameter_node(state: State):
    '''Sends commands for turning on or off lights.
    Based on `topics` field in `rooms` parameter, it will decide which mqtt topic
    it will send the message. `status` field in `rooms` class is needed for `on` 
    or `off` command.

    Args:
        state (State): the state has been being managed by Langgraph.
        rooms (Rooms): Rooms class to be parsed in the function to send 
        necessary messages to proper mqtt topic.

    Returns:
        state (State): the state has been being managed by Langgraph.
    '''
    response = llm.invoke(
        [CONTROL_PARAMETER_PROMPT] + state["messages"]
    )
    # TODO: add try-except block
    rooms = response.content.strip().lower()
    rooms: Rooms = room_parser.parse(response.content)
    return {
        "rooms": rooms,
        "messages": state["messages"] + [response]
    }

def control_policy_check(state: State):
    errors = []

    rooms = state['rooms'].rooms
    topics = state['rooms'].topics
    statuses = state['rooms'].status

    # Check if rooms fit the schema
    if isinstance(rooms, list):
        for room in rooms:
            if room not in get_args(Room):
                print(f'----NOK-----, {room}')
                errors.append(f"Invalid room: {rooms}")
    else:
        if rooms not in get_args(Room):
                print(f'----NOK-----, {topics}')
                errors.append(f"Invalid topic: {topics}")

    # Check if topics fit the schema
    if isinstance(rooms, list):
        for topic in topics:
            if topic not in get_args(Topic):
                print(f'----NOK-----, {topic}')
                errors.append(f"Invalid topic: {topics}")
    else:
        if topics not in get_args(Topic):
                print(f'----NOK-----, {topics}')
                errors.append(f"Invalid topic: {topics}")

    # Check if statuses fit the schema
    if isinstance(statuses, list):
        for status in statuses:
            if status not in get_args(Status):
                print(f'----NOK-----, {status}')
                errors.append(f"Invalid status: {statuses}")
    if errors:
        return {
            "policy_ok": False,
            "policy_feedback": "; ".join(errors),
            "policy_retry_count": state.get("policy_retry_count", 0) + 1,
        }

    return {
        "policy_ok": True,
        "policy_feedback": None,
    }

def control_node(state: State):

    # TODO: send message to proper topic
    print("→ CONTROL")
    response = publish_mqtt_message(
        topic=state['rooms'].topics,
        message=state['rooms'].status
    )
    # return state


# Read Tools
# 1. Convert the natural language to db query
# 2. Run the query and get the result
# 3. Embed the result to a prompt

# Write Tools
# 1. Convert the natural language to db query
# 2. Run the query and get the result
# 3. Embed the result to a prompt