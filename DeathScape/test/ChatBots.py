#install packages
# pip install -r chatbot_requirements.txt

# import required packages
from chatterbot import ChatBot
from chatterbot.conversation import Statement
from chatterbot.trainers import ChatterBotCorpusTrainer

# create ChatBot
sk = ChatBot("Sarah Krista")
nj = ChatBot("Natalia Jonathan")
am = ChatBot("Arjun Manoj")
ty = ChatBot("Taimo Yong")
ey = ChatBot("Ester Yura")

# create ChatBot trainer
sk_trainer = ChatterBotCorpusTrainer(sk)
nj_trainer = ChatterBotCorpusTrainer(nj)
am_trainer = ChatterBotCorpusTrainer(am)
ty_trainer = ChatterBotCorpusTrainer(ty)
ey_trainer = ChatterBotCorpusTrainer(ey)

# Train ChatBot with English language corpus
# you can train with different language
# or with your custom .yam file
# trainer.train("chatterbot.corpus.english")

# sk_trainer.train("chatterbot.corpus.english.greetings")
# nj_trainer.train("chatterbot.corpus.english.emotion")
# am_trainer.train("chatterbot.corpus.english.food")
# ty_trainer.train("chatterbot.corpus.english")
# ey_trainer.train("chatterbot.corpus.english")

while True:
    npc = int(input("Enter:\n 1: Sarah Krista\n 2: Natalia Jonathan\n 3: Arjun Manoj\n 4: Taimo Yong\n 5: Ester Yura\n"))
    
    if npc == 0:
        break
    
    name_list = {1: "Sarah Krista", 2: "Natalia Jonathan", 3: "Arjun Manoj", 4: "Taimo Yong", 5: "Ester Yura"}
    chat_list = {1: sk,2:nj,3:am,4:ty,5:ey}

    bot = chat_list[npc]
    name = name_list[npc]
    # Greeting from chat bot
    print("Hello I am " + name)

    # keep communicating with ChatBot
    while True:
        # take user input/query
        query = input("You: ")
        if query == "Q":
            break
        # response from ChatBot
        # put query on Statement format to avoid runtime alert messages
        # Statement(text=query, search_text=query)
        print(name + ":" + str(bot.get_response(Statement(text=query, search_text=query))))