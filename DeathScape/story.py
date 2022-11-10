import json
import random


class Story:
    def __init__(self, player):
        self.player = {
            "name": player,
            "doomsday": 0
        }
        self.level = 1
        self.rooms = self.init_rooms()
        self.character_features = self.init_character_features()
        self.characters = self.init_characters()
        self.story = self.init_story()

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
