function toggleDisplay() {
  var characters = document.getElementById("characters");
  characters.classList.toggle("d-none");
  var chat = document.getElementById("chat");
  chat.classList.toggle("d-none");
  var responses = document.getElementById("responses");
  responses.classList.toggle("d-none");
}