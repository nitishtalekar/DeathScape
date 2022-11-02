import json
import random as r

'''
Handles the main flow of the story.
'''

class Story:
    def __init__(self):
        with open("data/character_features.json") as f1:
            self.features = json.load(f1)
        with open("data/characters.json") as f2:
            self.characters = json.load(f2)
        self.players = {}
        self.doomsday = {}
        for character in self.characters:
            self.players[character] = {}
            for feature in self.features:
                self.players[character][feature] = r.choice(['-1','0','1'])
            self.doomsday[character] = self.calcDoomsday(self.players[character])
                
    def calcDoomsday(self,features):
        ddp = 0
        feature_list = "".join([features[i] for i in features])
        for f in ['1','0','-1']:
            for r in ['1','0','-1']:
                for q in ['1','0','-1']:
                    ddp += 10
                    if feature_list == "".join([f,r,q]):
                        return ddp
        return -1 
            
                
    def showPlayers(self):
        print(self.players)
        print(self.doomsday)
        
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
