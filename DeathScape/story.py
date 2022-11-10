import json
import random


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

        # For demo purposes only
        # self.death_order = self.get_death_order()
        self.remaining_characters = [character for character, info in self.characters.items() if info["alive"]]

        # print("DEATH ORDER:\n-----------------------------------------------------------------------------\n{}".format(self.death_order))
        print("REMAINING CHARACTERS:\n-----------------------------------------------------------------------------\n{}".format(self.remaining_characters))

        self.button_room = {
            "player": {
                "name": player,
                "doomsday": 0,
                "clue": self.rooms["1"]["clues"]["clue1"]
            },
            "level": 1,
            "room": self.rooms["1"],
            "characters": self.remaining_characters,
            "story": self.story[self.rooms["1"]["name"]],
            "choices": self.rooms["1"]["choices"]
        }

        # del self.remaining_characters[self.death_order[0]]
        self.remaining_characters.pop()

        self.lab_room = {
            "player": {
                "name": player,
                "doomsday": 0,
                "clue": ""
            },
            "level": 1,
            "room": self.rooms["2"],
            "characters": self.remaining_characters,
            "story": self.story[self.rooms["2"]["name"]],
            "choices": self.rooms["2"]["choices"]
        }
        
        print("REMAINING CHARACTERS:\n-----------------------------------------------------------------------------\n{}".format(self.remaining_characters))

        self.remaining_characters.pop()

        self.lab_room = {
            "player": {
                "name": player,
                "doomsday": 0,
                "clue": ""
            },
            "level": 1,
            "room": self.rooms["2"],
            "characters": self.remaining_characters,
            "story": self.story[self.rooms["2"]["name"]],
            "choices": self.rooms["2"]["choices"]
        }
        
        print("REMAINING CHARACTERS:\n-----------------------------------------------------------------------------\n{}".format(self.remaining_characters))


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

        # player_has_clue = len(self.rooms["clues"]) > len(
        #     {character: info for character, info in self.characters.items() if info["alive"]})

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

        for character, info in self.current["characters"].items():
            replaced = replaced.replace(
                "%NPC{}%".format(num_characters), character)
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

    #     order = sorted(self.characters.items(), key=lambda info:info["doomsday"])

    #     return order
