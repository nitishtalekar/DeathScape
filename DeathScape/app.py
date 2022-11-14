from flask import Flask, redirect, request, render_template
from story import Story

from chatterbot import ChatBot
from chatterbot.conversation import Statement
from chatterbot.trainers import ChatterBotCorpusTrainer

# ChatBot imports
# from chatterbot import ChatBot
# from chatterbot.trainers import ChatterBotCorpusTrainer

# Define ChatBot
# chatbot = ChatBot("ChatBot")
# trainer = ChatterBotCorpusTrainer(chatbot)
# trainer.train("chatterbot.corpus.english")


app = Flask(__name__)
story = None


@app.errorhandler(404)
def page_not_found(e):
    return render_template('page_not_found.html'), 404


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        player = request.form["player_name"]

        return redirect("/deathscape?player={}".format(player))
    else:
        return render_template("index.html")


@app.route("/deathscape", methods=["GET", "POST"])
def deathscape():
    global story
    player = request.args.get("player")
    talk = False
    if player == None:
        return redirect("/")
    else:
        if request.method == "POST":
            npc = request.form["talk_npc"]
            talk = True
            if npc == "end_convo":
                story.end_convo()
                talk = False
            elif npc == "msg":
                query = request.form["msg"]
                resp = str(story.bot.get_response(Statement(text=query, search_text=query)))
                user_chat = {"name":player,"text":query}
                npc_chat = {"name":story.npc,"text":resp}
                story.msg.append(user_chat)
                story.msg.append(npc_chat)
            else:
                story.chat_npc(npc)
                
        if request.method == "GET":
            story = Story(player)
        elif "choice" in request.form:
            story.set_choices(request.form["choice"])

        return render_template("deathscape.html", data=story.current,talk = talk,msg = story.msg)


# ChatBot responses
@app.route("/chat", methods=["GET", "POST"])
def get_bot_response():
    if request.method == "POST":
        userText = request.form["msg"]
        print(userText)
        resp = str(chatbot.get_response(userText))
        print(resp)
        print("----------")
        return render_template("chat.html",response = resp)
    resp = "HELLO THERE"
    return render_template("chat.html",response = resp)


if __name__ == "__main__":
    app.run(port=5000, debug=True)

    # Serve the app with gevent
    # http_server = WSGIServer(("0.0.0.0",5000),app)
    # http_server.serve_forever()
