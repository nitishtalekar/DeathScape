var data = {
    "player": {},
    "level": 1,
    "room": {},
    "characters": {},
    "story": [],
    "choices": [],
    "show_characters": false
}

var pressed_buttons = ""

function preprocess(player, level, room, characters, story, choices, show_characters) {
    data = {
        "player": player,
        "level": level,
        "room": room,
        "characters": characters,
        "story": story,
        "choices": choices,
        "show_characters": show_characters
    }

    console.log("PLAYER: " + data["player"]);
    console.log("LEVEL: " + data["level"]);
    console.log("ROOM: " + data["room"]);
    console.log("CHARACTERS: " + data["characters"]);
    console.log("STORY: " + data["story"]);
    console.log("CHOICES: " + data["choices"]);
    console.log("SHOW_CHARACTERS: " + data["show_characters"]);
}