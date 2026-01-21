import yaml
from pathlib import Path
from typing import List

CONFIG_PATH = Path(__file__).resolve().parent.parent / "config" / "lights.yaml"

def load_config():
    with CONFIG_PATH.open() as f:
        return yaml.safe_load(f)
    
def get_rooms(config: dict) -> List[str]:
    return list(config['rooms'].keys())

def main():
    cfg = load_config()
    print(f"Welcome to {cfg['house']}!")
    rooms = get_rooms(cfg)
    print("Available rooms:")
    for room in rooms:
        print(f"  • {room.capitalize()}")

main()