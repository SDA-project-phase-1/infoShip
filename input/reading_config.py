import json
import path as p


def read_config_file(pathOfFile): #takes path as param and returns config structure
    with open(pathOfFile, 'r', encoding='utf-8') as config_file:
        data = json.load(config_file)
    return data



