var data = {
    "player": {},
    "level": 1,
    "room": {},
    "characters": {},
    "story": [],
    "choices": [],
    "show_characters": false,
    "chatbots": {},
    "npc": "",
    "bot": null,
    "messages": []
}

function preprocess(player, level, room, characters, story, choices, show_characters, chatbots, npc, bot, messages) {
    window.scrollTo(0, document.body.scrollHeight);

    var scrollbox = document.getElementsByClassName("scrollbox")[0];
    if (scrollbox) {
        scrollbox.scrollTop = scrollbox.scrollHeight;
    }

    data = {
        "player": player,
        "level": level,
        "room": room,
        "characters": characters,
        "story": story,
        "choices": choices,
        "show_characters": show_characters,
        "chatbots": chatbots,
        "npc": npc,
        "bot": bot,
        "messages": messages
    }

    console.log("PLAYER: " + data["player"]);
    console.log("LEVEL: " + data["level"]);
    console.log("ROOM: " + data["room"]);
    console.log("CHARACTERS: " + data["characters"]);
    console.log("STORY: " + data["story"]);
    console.log("CHOICES: " + data["choices"]);
    console.log("SHOW_CHARACTERS: " + data["show_characters"]);
    console.log("CHATBOTS: " + data["chatbots"]);
    console.log("NPC: " + data["npc"]);
    console.log("BOT: " + data["bot"]);
    console.log("MESSAGES: " + data["messages"]);
}