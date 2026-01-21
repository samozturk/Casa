
from phue import Bridge
from typing import List


bridge = Bridge("192.168.178.21")

# TODO: write docstrings
# Functions to gather information from hue bridge for validation
def get_hue_scenes(bridge: Bridge=bridge):
    scenes_dict = {}
    scenes_dict['name'] = []
    scenes_dict['id'] = []
    scenes_dict['lights'] = []
    scenes_dict['group'] = []

    for scene_id, scene_data in bridge.get_scene().items():
        scenes_dict['name'].append(scene_data.get('name'))
        scenes_dict['id'].append(scene_id)
        scenes_dict['lights'].append(scene_data.get('lights'))
        scenes_dict['group'].append(scene_data.get('group'))
    return scenes_dict

def get_hue_rooms(bridge: Bridge)-> List[str]:
    '''Gets all the room names from the hue bridge

    Args:
        bridge (Bridge): Bridge object that hue api needs
    Returns:
        hue_rooms (List[str]): Name of hue rooms
    '''
    hue_rooms = []
    for id, room in bridge.get_group().items():
        hue_rooms.append(room['name'])
    return hue_rooms

# Hue control commands
def set_hue_scene(scene_name: str, room_name: str, bridge: Bridge=bridge):
    '''Activate a philips hue scene from hue bridge via an API

    Args:
        scene_name (str): scene name to run
        room_name (str): room name to activate the scene
        bridge (Bridge, optional): hue bridge object. Defaults to bridge.

    Returns:
        _type_: _description_
    '''
    # Room name validation
    if room_name in get_hue_rooms(bridge=bridge):
        # Scene name validation
        if scene_name in get_hue_scenes(bridge)['name']:
            bridge.run_scene(group_name=room_name, scene_name=scene_name)
            return f"Scene '{scene_name}' activated."
        else:
            return f"Scene '{scene_name}' not found."

def turn_hue_light_on_off(room_name: str, status: str, bridge: Bridge=bridge):
    lights = bridge.get_light_objects('name')
    if room_name in get_hue_rooms(bridge=bridge):
        
