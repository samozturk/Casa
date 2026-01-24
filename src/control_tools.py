# Control Tools
from typing import get_args

from langchain.tools import tool
from langchain_core.messages import HumanMessage

from models import Rooms, State, Room, Topic, Status
from prompts import room_parser, llm, CONTROL_PARAMETER_PROMPT
from utils.utils import publish_mqtt_message


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
    #TODO: Also check if the lenght of the lists are the same
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
    topics = state['rooms'].topics

    if topics is isinstance(topics, list):
        for topic, room, status in zip(state['rooms'].topics, state['rooms'].rooms, state['rooms'].status):
            response = publish_mqtt_message(
                topic=topic,
                message=f'{{"room": "{room}", "status": "{status}"}}'
            )
            print(f'Published to {topic}: {response}')
    else:
        response = publish_mqtt_message(
            topic=topics,
            message=f'{{"room": "{state["rooms"].rooms}", "status": "{state["rooms"].status}"}}'
        )
        print(f'Published to {topics}: {response}')
    # TODO: add response to state
    return state