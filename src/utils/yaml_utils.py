
import yaml
from pathlib import Path
import importlib
from typing import List, Callable

CONFIG_PATH = Path(__file__).resolve().parent.parent.parent / "config" / "lights.yaml"

def load_config(config_path: Path = CONFIG_PATH):
    with config_path.open() as f:
        return yaml.safe_load(f)

def get_tools_from_config(room_name: str="office", 
                        device_type: str="lights", 
                        control_interface: str="hue_api") -> List[Callable]:
    """
    This function reads the configuration file to determine which tools should be
    loaded for the given room, device type, and control interface. It dynamically
    imports the necessary modules and returns a list of callable functions that can
    be used to control the lights.

    Args:
        room_name (str): The name of the room for which to load tools. Defaults to "office".
        device_type (str): The type of device to control. Defaults to "lights".
        control_interface (str): The control interface to use. Defaults to "hue_api".

    Returns:
        List[Callable]: A list of callable functions that can be used to control lights
        in the specified room using the specified control interface.

    Example:
        >>> tools = get_tools_from_config("living_room", "lights", "hue_api")
        >>> tools[0]()  # Execute the first tool function
    """
    config = load_config()

    for light in config['rooms'][room_name][device_type]:
        if light['control_interface'] == control_interface:
            functions = light['functions']

    tools = [function for function in functions]

    module_name = "utils." + control_interface + "_utils"
    device_utils = importlib.import_module(module_name)
    tool_functions = []
    for tool in tools:
        func = getattr(device_utils, tool)
        tool_functions.append(func)
    return tool_functions