import json

'''
Handles the main flow of the story.
'''

class Story:
    def __init__(self):
        self.character_features = {}
        self.characters = {}

    def read_json(self):
        print("Here")
        with open("data/character_features.json") as f1:
            with open("data/characters.json") as f2:
                self.character_features = json.load(f1)
                self.characters = json.load(f2)
                

    def setup(self):
        print("TODO")

    def start(self):
        print("TODO")

    def start(self):
        print("TODO")
