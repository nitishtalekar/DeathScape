function addText(text) {
  var story = document.getElementById("story");
  if (!story.querySelector("div button").includes(text)) {
    story.innerHTML += "<p>" + text + "</p>";
  }
}

function handle(choice) {
  console.log(choice)
}

function toggle() {
  var choices = document.getElementById("choices");
  choices.classList.toggle("d-none");

  var characters = document.getElementById("characters");
  characters.classList.toggle("d-none");
}