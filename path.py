import os

base_path = os.path.dirname(__file__)

def return_base_directory():
    return base_path

def return_config_directory():
    return os.path.join(return_base_directory(),"config.json")