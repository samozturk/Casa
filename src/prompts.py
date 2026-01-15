from langchain_core.messages import BaseMessage, SystemMessage
from langchain_core.output_parsers import PydanticOutputParser
from models import Rooms


# For initial intent classification node: 
INTENT_PROMPT = SystemMessage(
    content=(
        "Classify the user's intent.\n\n"
        "Return exactly ONE of the following strings:\n"
        "- search\n"
        "- read\n"
        "- control\n"
        "- chat\n\n"
        "Return ONLY the label."
    )
)

# For control node: 
room_parser = PydanticOutputParser(pydantic_object=Rooms)
CONTROL_PARAMETER_PROMPT = SystemMessage(
    content = (
        "Based on human message, refer which room's lights needs to be controlled and what needs to be done."
        "You must output JSON that matches this schema:"
        f"{room_parser.get_format_instructions()}"
        "Do not include any text outside the JSON."
    )
)