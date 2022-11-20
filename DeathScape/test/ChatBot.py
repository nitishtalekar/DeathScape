#install packages
# pip install -r chatbot_requirements.txt

# import required packages
from chatterbot import ChatBot
from chatterbot.conversation import Statement
from chatterbot.trainers import ChatterBotCorpusTrainer

# create ChatBot
chat_bot = ChatBot("ChatBot")

# create ChatBot trainer
trainer = ChatterBotCorpusTrainer(chat_bot)

# Train ChatBot with English language corpus
# you can train with different language
# or with your custom .yam file
trainer.train("chatterbot.corpus.english")

# Greeting from chat bot
print("Hi, I am ChatBot")

# keep communicating with ChatBot
while True:
    # take user input/query
    query = input(">>>")
    # response from ChatBot
    # put query on Statement format to avoid runtime alert messages
    # Statement(text=query, search_text=query)
    print(chat_bot.get_response(Statement(text=query, search_text=query)))