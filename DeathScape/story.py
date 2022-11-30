import json
import random
from chatterbot import ChatBot
# from chatterbot.conversation import Statement
# from chatterbot.trainers import ChatterBotCorpusTrainer


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
            "choices": self.rooms["1"]["choices"],
            "show_characters": False,
            "chatbots": {},
            "npc": "",
            "bot": "",
            "messages": []
        }

        self.intro = self.init_intro()
        self.init_choices()
        self.init_chat()

        self.remaining_characters = [
            character for character, info in self.characters.items() if info["alive"]]

        self.remaining_characters.pop()

        self.lab_room = {
            "player": {
                "name": player,
                "doomsday": 0,
                "clue": ""
            },
            "level": 2,
            "room": self.rooms["2"],
            "characters": self.remaining_characters,
            "story": self.story[self.rooms["2"]["name"]],
            "choices": self.rooms["2"]["choices"],
            "show_characters": False
        }

        self.remaining_characters.pop()

        self.justice_room = {
            "player": {
                "name": player,
                "doomsday": 0,
                "clue": ""
            },
            "level": 3,
            "room": self.rooms["3"],
            "characters": self.remaining_characters,
            "story": self.story[self.rooms["3"]["name"]],
            "choices": self.rooms["3"]["choices"],
            "show_characters": False
        }

        self.remaining_characters.pop()

        self.trap_room = {
            "player": {
                "name": player,
                "doomsday": 0,
                "clue": self.rooms["4"]["clues"]["clue1"]
            },
            "level": 4,
            "room": self.rooms["4"],
            "characters": self.remaining_characters,
            "story": self.story[self.rooms["4"]["name"]],
            "choices": self.rooms["4"]["choices"],
            "show_characters": False
        }

        self.remaining_characters.pop()

        self.dilemma_room = {
            "player": {
                "name": player,
                "doomsday": 0,
                "clue": self.rooms["5"]["clues"]["clue1"]
            },
            "level": 5,
            "room": self.rooms["5"],
            "characters": self.remaining_characters,
            "story": self.story[self.rooms["5"]["name"]],
            "choices": self.rooms["5"]["choices"],
            "show_characters": False
        }

    def init_intro(self):
        with open("data/intro.json") as f:
            intro = json.load(f)

        return self.replace_placeholders(intro["description"])

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
            characters[character]["index"] = index + 1
            characters[character]["alive"] = True
            characters[character]["clue"] = self.rooms["1"]["clues"]["clue{}".format(
                characters[character]["index"] + 1)]

            for character_feature in character_features:
                characters[character][character_feature] = random.choice(
                    [-1, 1])

            doomsday = 0
            for friendliness in [1, -1]:
                for anger in [1, -1]:
                    for quietness in [1, -1]:
                        doomsday += 10

                        if characters[character]["friendliness"] == friendliness and characters[character]["anger"] == anger and characters[character]["quietness"] == quietness:
                            characters[character]["doomsday"] = doomsday

        return characters

    def init_story(self):
        story = {}

        for room in self.rooms.values():
            story[room["name"]] = [room["description"]]

        return story

    def init_choices(self):
        for choice in self.current["choices"]:
            self.add_parent(choice, None)

        # for choice in self.current["choices"]:
        #     self.set_parent(choice)

    def init_chat(self):
        sk = ChatBot("Sarah Krista")
        nj = ChatBot("Natalia Jonathan")
        am = ChatBot("Arjun Manoj")
        ty = ChatBot("Taimo Yong")
        ey = ChatBot("Ester Yura")

        # sk_trainer = ChatterBotCorpusTrainer(sk)
        # nj_trainer = ChatterBotCorpusTrainer(nj)
        # am_trainer = ChatterBotCorpusTrainer(am)
        # ty_trainer = ChatterBotCorpusTrainer(ty)
        # ey_trainer = ChatterBotCorpusTrainer(ey)

        # sk_trainer.train("chatterbot.corpus.english.greetings")
        # nj_trainer.train("chatterbot.corpus.english.emotion")
        # am_trainer.train("chatterbot.corpus.english.food")
        # ty_trainer.train("chatterbot.corpus.english")
        # ey_trainer.train("chatterbot.corpus.english")

        self.current["chatbots"]["Sarah Krista"] = sk
        self.current["chatbots"]["Natalia Jonathan"] = nj
        self.current["chatbots"]["Arjun Manoj"] = am
        self.current["chatbots"]["Taimo Yong"] = ty
        self.current["chatbots"]["Ester Yura"] = ey

    def add_parent(self, node, parent):
        node["parent"] = parent

        if "next" not in node:
            return

        for child in node["next"]:
            self.add_parent(child, node["name"])

    def set_parent(self, node):
        for choice in self.current["choices"]:
            if choice["name"] == node["parent"]:
                node["parent"] = choice["parent"]

                break

        if "next" not in node:
            return

        for child in node["next"]:
            self.set_parent(child)

    def replace_placeholders(self, text):
        replaced = text
        max_doomsday = 0
        dead = ""

        for character, info in self.current["characters"].items():
            replaced = replaced.replace(
                "%NPC{}%".format(info["index"]), character).replace(
                "%CLUE{}%".format(info["index"]), info["clue"])

            if info["doomsday"] > max_doomsday:
                max_doomsday = info["doomsday"]
                dead = character.split(" ")[0]

        replaced = replaced.replace("%DEAD%", dead)

        return replaced

    def set_choices(self, current):
        if current == "Talk to someone":
            self.current["show_characters"] = True
        for choice in self.current["choices"]:
            if choice["name"] == current:
                self.add_to_story(current)

                replaced = []
                next = None

                if "next" not in choice:
                    if "Try the puzzle later" == current or "Talk to someone" == current:
                        next = self.rooms["{}".format(
                            self.current["level"])]["choices"]
                    else:
                        next = self.rooms["{}".format(
                            self.current["level"])]["choices"][0]["next"]
                else:
                    if "red" in self.current["story"][len(self.current["story"]) - 4] and "blue" in self.current["story"][len(self.current["story"]) - 3] and "yellow" in self.current["story"][len(self.current["story"]) - 2] and "green" in self.current["story"][len(self.current["story"]) - 1]:
                        self.current["story"].append(
                            "A hidden compartment on the table pops open to reveal a golden button.")
                        next = choice["next"]
                    else:
                        next = self.rooms["{}".format(
                            self.current["level"])]["choices"][0]["next"]

                for item in next:
                    replaced.append({
                        "name": self.replace_placeholders(item["name"]),
                        "text": self.replace_placeholders(item["text"]),
                        "parent": item["parent"]
                    })

                    if "next" in item:
                        replaced[len(replaced) - 1].update({
                            "next": item["next"]
                        })

                self.current["choices"] = replaced

                return

    def add_to_story(self, current):
        for choice in self.current["choices"]:
            if choice["name"] == current:
                replaced = self.replace_placeholders(
                    "\n{}".format(choice["text"]))

                if (replaced not in self.current["story"][len(self.current["story"]) - 1] or "pressed the" in replaced.lower()) and (replaced not in self.current["story"] or "You decide to talk to someone" in replaced or "You decide to try the puzzle" in replaced or "pressed the" in replaced.lower()):
                    self.current["story"].append(replaced)

                    if "Try the puzzle" == current and self.current["player"]["clue"] not in self.current["story"]:
                        if self.current["player"]["clue"] != "":
                            self.current["story"].append(
                                self.current["player"]["clue"])
                        elif "It seems like you have to find a way to dislocate the lock to successfully escape the room." not in self.current["story"]:
                            self.current["story"].append(
                                "It seems like you have to find a way to dislocate the lock to successfully escape the room.")
                    elif "golden button" in current:
                        if "Do not" in current:
                            self.current["story"].append(self.replace_placeholders(
                                self.current["room"]["deaths"]["npc"]))

                            max_doomsday = 0
                            dead = ""
                            for character, info in self.current["characters"].items():
                                if info["doomsday"] > max_doomsday:
                                    max_doomsday = info["doomsday"]
                                    dead = character

                            self.current["characters"][dead]["alive"] = False
                        else:
                            self.current["story"].append(self.replace_placeholders(
                                self.current["room"]["deaths"]["player"]))

                return

    def add_character_to_story(self, character_to_add):
        for character in self.current["characters"]:
            if character == character_to_add:
                replaced = "You approach {}. {}".format(character, self.replace_placeholders(
                    self.current["room"]["actions"]["npc{}".format(self.current["characters"][character]["index"])]))

                if replaced not in self.current["story"][len(self.current["story"]) - 1] and replaced not in self.current["story"][len(self.current["story"]) - 2]:
                    self.current["story"].append(replaced)

                if self.current["characters"][character]["description"] not in self.current["story"]:
                    self.current["story"].append(
                        self.current["characters"][character]["description"])

                return

    def go_back(self, current):
        self.add_to_story(current)

        for choice in self.current["choices"]:
            if choice["name"] == current:
                self.set_choices(choice["parent"])

                return

    def set_bot(self, npc_name):
        self.current["npc"] = npc_name
        self.current["bot"] = self.current["chatbots"][npc_name]

    def add_messages(self, player_message, character_message):
        player = {"name": "You", "text": player_message}
        character = {"name": self.current["npc"], "text": character_message}

        if len(self.current["messages"]) == 0 or (self.current["messages"][len(self.current["messages"]) - 2] != player and self.current["messages"][len(self.current["messages"]) - 1] != character):
            self.current["messages"].append(player)
            self.current["messages"].append(character)

    def dont_talk(self):
        self.current["show_characters"] = False

        if "You decide not to talk to anyone." not in self.current["story"][len(self.current["story"]) - 1]:
            self.current["story"].append("You decide not to talk to anyone.")

    def end_conversation(self):
        self.current["show_characters"] = False

        for message in self.current["messages"]:
            self.current["story"].append(self.replace_placeholders("\n{}: {}".format(
                message["name"] if message["name"] != self.current["player"]["name"] else "You", message["text"])))

        if self.current["npc"] != "":
            for character in self.current["characters"]:
                if character == self.current["npc"]:
                    replaced = self.replace_placeholders(
                        self.current["characters"][character]["clue"])

                    if replaced not in self.current["story"]:
                        self.current["story"].append(replaced)

                    if "You walk away." not in self.current["story"][len(self.current["story"]) - 1]:
                        self.current["story"].append(
                            "You walk away.")

                    break

        self.current["npc"] = ""
        self.current["messages"] = []
        self.current["bot"] = ""

    def next(self):
        self.current = {
            "player": {
                "name": self.current["player"]["name"],
                "doomsday": self.current["player"]["doomsday"],
                "clue": ""
            },
            "level": self.current["level"] + 1,
            "room": self.rooms["{}".format(self.current["level"] + 1)],
            "characters": {character: info for character, info in self.characters.items() if info["alive"]},
            "story": self.story[self.rooms["{}".format(self.current["level"] + 1)]["name"]],
            "choices": self.rooms["{}".format(self.current["level"] + 1)]["choices"],
            "show_characters": False,
            "chatbots": {},
            "npc": "",
            "bot": "",
            "messages": []
        }

        self.init_choices()
