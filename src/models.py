
from typing import TypedDict, List, Literal, Union, List
from pydantic import BaseModel
from langchain_core.messages import BaseMessage


Room = Literal["office", "bedroom"]
Topic = Literal["home/lights/office", "home/lights/bedroom"]
Status = Literal["on", "off"]

class Rooms(BaseModel):
    rooms: Union[Room, List[Room]]
    topics: Union[Topic, List[Topic]]
    status: Union[Status, List[Status]]


class State(TypedDict):
    messages: List[BaseMessage]
    intent: str | None
    rooms: Rooms

    policy_ok: bool
    policy_feedback: str | None
    policy_retry_count: int