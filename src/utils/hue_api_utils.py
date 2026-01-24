
from phue import Bridge
from typing import List


bridge = Bridge("192.168.178.21")

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

def get_hue_room_states(bridge: Bridge)-> dict:
    '''Gets all the room states from the hue bridge
    Args:
        bridge (Bridge): Bridge object that hue api needs
    Returns:
        hue_room_states (dict): Name of hue rooms and their current brightness
    '''
    hue_room_states = {}
    groups = bridge.get_api()['groups']
    for group_id in groups:
        current_state = {}
        group = bridge.get_group(int(group_id))
        name = group['name']
        current_brightness = group['action']['bri']
        state = group['state']
        current_state[name] = {
            'bri': current_brightness,
            'on': state['any_on']
        }
        hue_room_states[name] = current_state[name]
    return hue_room_states


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

def dim_hue_lights(room_name: str, brightness: int, bridge: Bridge=bridge, transitiontime: int=40):
    '''Dim Philips Hue lights in a room to a specified brightness level.
    Args:
        room_name (str): Name of the room where lights need to be dimmed.
        brightness (int): Brightness level (0-254) to set the lights to.
        bridge (Bridge, optional): Hue Bridge object. Defaults to bridge.
        transitiontime (int, optional): Time in deciseconds for the transition. Defaults to 40 (4 seconds).
    '''
    group_id = bridge.get_group_id_by_name(room_name)
    command =  {'transitiontime' : transitiontime, 'on' : True, 'bri' : brightness}
    bridge.set_group(group_id, command)