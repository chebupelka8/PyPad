import json


def load_settings(path_to_settings_file: str):
    with open(path_to_settings_file, "r") as file:
        settings = json.load(file)
        file.close()
    
    return settings

def load_style(__path_to_file: str) -> str:
    with open(__path_to_file, "r") as file:
        code = file.read()
        file.close()
    
    return code