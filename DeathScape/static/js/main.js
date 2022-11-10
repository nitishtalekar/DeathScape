var player = {};
var level = 1;
var room = {};
var characters = {};
var story = [];
var choices = [];

function preprocess(player, level, room, characters, story, choices) {
  player = player;
  level = level;
  room = room;
  characters = characters;
  story = story;
  choices = choices;

  console.log("PLAYER: " + player);
  console.log("LEVEL: " + level);
  console.log("ROOM: " + room);
  console.log("CHARACTERS: " + characters);
  console.log("STORY: " + story);
  console.log("CHOICES: " + choices);
}

function handle(choice) {

}