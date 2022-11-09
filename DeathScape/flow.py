import json
import random as r

'''
Handles the main flow of the story.
'''

class Story:
    def __init__(self,name):
        self.main_character = name
        self.players,self.doomsday = self.initPlayers()
        self.players[name] = {'friendship':'0',
                            'rage' : '0',
                            'quiteness' : '0'}
        self.doomsday[name] = self.calcDoomsday(self.players[name])
        self.curr_lvl = 1
        self.lvl_func = {
            1 : self.buttonRoom,
            2 : self.labRoom,
            3 : self.justiceRoom,
            4 : self.trapRoom,
            5 : self.dilemmaRoom
        }
        self.displayText = []
    
    def initPlayers(self):
        with open("data/character_features.json") as f1:
            features = json.load(f1)
        with open("data/characters.json") as f2:
            characters = json.load(f2)
        players = {}
        doomsday = {}
        for character in characters:
            players[character] = {}
            for feature in features:
                players[character][feature] = r.choice(['-1','0','1'])
            doomsday[character] = self.calcDoomsday(players[character])
        return players,doomsday
                    
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
            
    def callLevel(self,lvl):
        return self.lvl_func[lvl]()
            
    ''' ----- Get Functions ----- '''
    def getPlot(self,id):
        return self.room["options"][id]
        
    def fetchOptions(self,options):
        return [[i,self.room["options"][i]["opt_text"]] for i in options ]
    
    def getPlayerNames(self):
        return list(self.players.keys())
        
    def getCurrentLevel(self):
        return self.curr_lvl
        
    def getRoomName(self):
        return self.room["name"]
        
    def getActiveNPC(self):
        return [name for name in list(self.players.keys()) if name != self.main_character]
        
                
    def showPlayers(self):
        print(self.players)
        print(self.doomsday)
    ''' ----- Set Functions ----- '''
    def setCurrentRoom(self):
        lvl = self.getCurrentLevel()
        self.callLevel(lvl)
        
    def setCurrentLevel(self):
        self.curr_lvl += 1
        
    def setDisplayText(self,newText):
        self.displayText.append(newText)
        
    ''' ----- Level Functions ----- '''
                
    def buttonRoom(self):
        with open("data/buttonRoom.json") as f:
            self.room = json.load(f)
        
    def labRoom(self):
        with open("data/labRoom.json") as f:
            self.room = json.load(f)
        
    def justiceRoom(self):
        with open("data/justiceRoom.json") as f:
            self.room = json.load(f)
        
    def trapRoom(self):
        with open("data/trapRoom.json") as f:
            self.room = json.load(f)
        
    def dilemmaRoom(self):
        with open("data/dilemmaRoom.json") as f:
            self.room = json.load(f)

    def setup(self):
        print("TODO")

    def start(self):
        print("TODO")

    def start(self):
        print("TODO")
