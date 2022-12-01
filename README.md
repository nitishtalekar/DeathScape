# DeathScape

DeathScape is a interactive narrative that is built upon the idea of uncertainty. It starts with the player stuck in an escape room with 5 other NPC. The NPC are autonomous and can be interacted with freely (within limits). The goal of the game is to survive a series of rooms, each room is lethal and can cause either the player or an NPC to die. The player need to make smart decisions while also interacting with the NPC. 

## TECH STACK

- Python 3.7
- Flask
- Chatterbot
- Jinja
- JSON

## HOW TO INSTALL

- Clone the git repository
    
    ```xml
    git clone https://github.com/nitishtalekar/DeathScape.git
    ```
    
- Navigate to DeathScape directory
    
    ```xml
    cd DeathScape
    ```
    
- Install requirements
    
    ```xml
    pip install -r requirements.txt
    ```
    
- Run Flask application
    
    ```xml
    python app.py
    ```
    
- Open URL to start playing
    
    ```xml
    http://localhost:5000
    ```
    

## HOW TO PLAY

### BEGIN

Initially you will find yourself in a room with 5 other characters. You can freely talk to them and see what the have to say. You can select the Puzzle button to try and solve the puzzle to escape the room. Be careful of what you do and say. It matters! Once you solve a room, you can move on to the next. Keep in mind that every room could be your last! Each room will have a puzzle to solve.

### CONVERSATIONS

Talk to any of our characters **Sarah Krista, Natalia Jonathan, Arjun Manoj, Taimo Yong** and **Ester Yura.** All these conversations are non-predetermined. You can go crazy in your conversations. Talk to each one of them as much as you can, during each room.

### GOAL

Clear the rooms one by one. Try and survive. Each room is lethal. The game is **Won** when you survive the file room and escape to safety!

## ABOUT GAME ELEMENTS

### LOGIC STRUCTURE

The logic of the game is linear. The choices are all in a similar format and are processed at the backend via a dataset of choices and consequences. 

********DATASETS********

The Data for all the choices and its consequent narrative is stored in a structured JSON format in the data directory

This data contains:

- clues
- choices
- room description
- deaths
- actions

### RANDOMIZATION

There are elements which are Randomized in DeathScape which make every turn a unique experience

******************NPC NAME ORDER******************

Every time you play the game, the people in the room will change the actions they are doing and the positions they are in randomly since we shuffle the order of NPCs at initialization

**NPC PERSONALITY TRAITS**

Every time you play the game, each NPC will randomly be assigned one of the 8 personalities that we have defined. These personalities are based on 3 characteristics being positive (0) or negative (1).

| Personality Number | Friendliness | Anger | Quietness |
| --- | --- | --- | --- |
| Personality 1 | 0 | 0 | 0 |
| Personality 2 | 0 | 0 | 1 |
| Personality  3 | 0 | 1 | 0 |
| Personality 4 | 0 | 1 | 1 |
| Personality 5 | 1 | 0 | 0 |
| Personality 6 | 1 | 0 | 1 |
| Personality 7 | 1 | 1 | 0 |
| Personality 8 | 1 | 1 | 1 |

### NPC CHATBOTS

The NPC chatbots are trained dynamically when a user wants to talk to an NPC. These bots are trained based on

- Their initial personality

- The current room

These bots were trained on a custom corpus that was manually generated for each personality type and each room.

************CORPUS************

Each personality has a common set of knowledge from the common corpus.

Each personality has a unique room based corpus 

Each personality has a unique emotion based corpus
