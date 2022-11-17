import json
import random
from chatterbot import ChatBot
from chatterbot.conversation import Statement
from chatterbot.trainers import ChatterBotCorpusTrainer


class Story:
    def __init__(self, player):
        self.rooms = self.init_rooms()
        self.characters = self.init_characters()
        self.story = self.init_story()

        self.current = {
            "player": {
                "name": player,
                "doomsday": 0,
                "clue": self.rooms["1"]["clues"]["clue1"]
            },
            "level": 1,
            "room": self.rooms["1"],
            "characters": {character: info for character, info in self.characters.items() if info["alive"]},
            "story": self.story[self.rooms["1"]["name"]],
            "choices": self.rooms["1"]["choices"]
        }

        self.chatbots = {}
        self.bot = ""
        self.initChat()
        self.msg = []

        self.init_choices(self.current["choices"])

        # For demo purposes only
        # self.remaining_characters = [
        #     character for character, info in self.characters.items() if info["alive"]]

        # self.button_room = {
        #     "player": {
        #         "name": player,
        #         "doomsday": 0,
        #         "clue": self.rooms["1"]["clues"]["clue1"]
        #     },
        #     "level": 1,
        #     "room": self.rooms["1"],
        #     "characters": self.remaining_characters,
        #     "story": self.story[self.rooms["1"]["name"]],
        #     "choices": self.rooms["1"]["choices"]
        # }

        # self.remaining_characters.pop()

        # self.lab_room = {
        #     "player": {
        #         "name": player,
        #         "doomsday": 0,
        #         "clue": ""
        #     },
        #     "level": 2,
        #     "room": self.rooms["2"],
        #     "characters": self.remaining_characters,
        #     "story": self.story[self.rooms["2"]["name"]],
        #     "choices": self.rooms["2"]["choices"]
        # }

        # self.remaining_characters.pop()

        # self.justice_room = {
        #     "player": {
        #         "name": player,
        #         "doomsday": 0,
        #         "clue": ""
        #     },
        #     "level": 3,
        #     "room": self.rooms["3"],
        #     "characters": self.remaining_characters,
        #     "story": self.story[self.rooms["3"]["name"]],
        #     "choices": self.rooms["3"]["choices"]
        # }

        # self.remaining_characters.pop()

        # self.trap_room = {
        #     "player": {
        #         "name": player,
        #         "doomsday": 0,
        #         "clue": self.rooms["4"]["clues"]["clue1"]
        #     },
        #     "level": 4,
        #     "room": self.rooms["4"],
        #     "characters": self.remaining_characters,
        #     "story": self.story[self.rooms["4"]["name"]],
        #     "choices": self.rooms["4"]["choices"]
        # }

        # self.remaining_characters.pop()

        # self.dilemma_room = {
        #     "player": {
        #         "name": player,
        #         "doomsday": 0,
        #         "clue": self.rooms["5"]["clues"]["clue1"]
        #     },
        #     "level": 5,
        #     "room": self.rooms["5"],
        #     "characters": self.remaining_characters,
        #     "story": self.story[self.rooms["5"]["name"]],
        #     "choices": self.rooms["5"]["choices"]
        # }

    # For chatting Purposes
    def initChat(self):
        sk = ChatBot("SarahKrista")
        nj = ChatBot("NataliaJonathan")
        am = ChatBot("ArjunManoj")
        ty = ChatBot("TaimoYong")
        ey = ChatBot("EsterYura")

        sk_trainer = ChatterBotCorpusTrainer(sk)
        nj_trainer = ChatterBotCorpusTrainer(nj)
        am_trainer = ChatterBotCorpusTrainer(am)
        ty_trainer = ChatterBotCorpusTrainer(ty)
        ey_trainer = ChatterBotCorpusTrainer(ey)

        self.chatbots["SarahKrista"] = sk
        self.chatbots["NataliaJonathan"] = nj
        self.chatbots["ArjunManoj"] = am
        self.chatbots["TaimoYong"] = ty
        self.chatbots["EsterYura"] = ey

    def chat_npc(self, npc_name):
        self.npc = npc_name
        self.bot = self.chatbots[npc_name]

    def end_convo(self):
        print(self.msg)

        self.msg = []
        self.bot = ""

    def init_rooms(self):
        with open("data/rooms.json") as f:
            room_names = json.load(f)

        rooms = {}

        for room_number, room_name in room_names.items():
            with open("data/{}Room.json".format(room_name)) as f:
                rooms[room_number] = json.load(f)

        return rooms

    def init_characters(self):
        with open("data/characterFeatures.json") as f:
            character_features = json.load(f)

        with open("data/characters.json") as f:
            characters = json.load(f)

        for index, character in zip(range(len(characters)), characters):
            characters[character]["alive"] = True
            characters[character]["clue"] = self.rooms["1"]["clues"]["clue{}".format(
                index + 2)]

            for character_feature in character_features:
                characters[character][character_feature] = random.choice(
                    [-1, 0, 1])

            doomsday = 0
            for friendliness in [1, 0, -1]:
                for anger in [1, 0, -1]:
                    for quietness in [1, 0, -1]:
                        doomsday += 10

                        if characters[character]["friendliness"] == friendliness and characters[character]["anger"] == anger and characters[character]["quietness"] == quietness:
                            characters[character]["doomsday"] = doomsday

        return characters

    def init_story(self):
        story = {}

        for room in self.rooms.values():
            story[room["name"]] = [room["description"]]

        return story

    def set_choices(self, current):
        for choice in self.current["choices"]:
            if choice["name"] == current:
                replaced = self.replace_placeholders(
                    "\n{}".format(choice["text"]))
                if replaced not in self.current["story"]:
                    self.current["story"].append(replaced)

                replaced = []
                next = None

                if "next" in choice:
                    next = choice["next"]
                else:
                    next = self.rooms["1"]["choices"]

                for item in next:
                    replaced.append({
                        "name": self.replace_placeholders(item["name"]),
                        "text": self.replace_placeholders(item["text"])
                    })

                    if "next" in item:
                        replaced[len(replaced) - 1].update({
                            "next": item["next"]
                        })

                self.current["choices"] = replaced

                return

    def replace_placeholders(self, text):
        replaced = text
        num_characters = 1
        max_doomsday = 0
        dead = ""

        replaced = replaced.replace("%CLUE%", self.current["player"]["clue"])

        for character, info in self.current["characters"].items():
            replaced = replaced.replace(
                "%NPC{}%".format(num_characters), character).replace(
                "%CLUE{}%".format(num_characters), info["clue"])
            num_characters += 1

            if info["doomsday"] > max_doomsday:
                dead = character.split(" ")[0]

        replaced = replaced.replace("%DEAD%", dead)

        return replaced

    # For demo purposes only
    # def get_death_order(self):
    #     order = []

    #     # for i in range(len(self.characters)):
    #     #     max_doomsday = 0
    #     #     item = ""

    #     #     for character, info in self.characters.items():
    #     #         if info["doomsday"] > max_doomsday:
    #     #             if character not in order:
    #     #                 item = character

    #     #     order.append(item)

    #     order = sorted(self.characters.items(),
    #                    key=lambda info: info["doomsday"])

    #     return order

    def init_choices(self, choices):
        for choice in choices:
            self.add_parent(choice, None)

    def add_parent(self, node, parent):
        node['parent'] = parent
        if not node.get('next'):
            return
        for child in node['next']:
            self.add_parent(child, node)
