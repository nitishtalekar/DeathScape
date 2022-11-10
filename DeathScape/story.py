import json
import random


class Story:
    def __init__(self, player):
        self.rooms = self.init_rooms()
        self.character_features = self.init_character_features()
        self.characters = self.init_characters()
        self.story = self.init_story()

        self.current = {
            "player": {
                "name": player,
                "doomsday": 0
            },
            "level": 1,
            "room": self.rooms["1"],
            "characters": {character: info for character, info in self.characters.items() if info["alive"]},
            "story": self.story[self.rooms["1"]["name"]],
            "choices": self.rooms["1"]["choices"]
        }

    def init_rooms(self):
        with open("data/rooms.json") as f:
            room_names = json.load(f)

        rooms = {}

        for room_number, room_name in room_names.items():
            with open("data/{}Room.json".format(room_name)) as f:
                rooms[room_number] = json.load(f)

        return rooms

    def init_character_features(self):
        with open("data/characterFeatures.json") as f:
            character_features = json.load(f)

        return character_features

    def init_characters(self):
        with open("data/characters.json") as f:
            characters = json.load(f)

        for character in characters:
            characters[character]["alive"] = True

            for character_feature in self.character_features:
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
