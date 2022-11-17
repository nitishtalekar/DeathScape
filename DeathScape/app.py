from chatterbot import ChatBot
from chatterbot.conversation import Statement
from chatterbot.trainers import ChatterBotCorpusTrainer
from flask import Flask, redirect, request, render_template
from story import Story


app = Flask(__name__)
story = None
chatbot = ChatBot("ChatBot")
trainer = ChatterBotCorpusTrainer(chatbot)
trainer.train("chatterbot.corpus.english")


@app.errorhandler(404)
def page_not_found(e):
    return render_template("page_not_found.html"), 404


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
            if "choice" in request.form:
                story.set_choices(request.form["choice"])

            if "character" in request.form:
                npc = request.form["character"]
                talk = True
                if npc == "end_convo":
                    story.end_convo()
                    talk = False
                elif npc == "msg":
                    query = request.form["msg"]
                    resp = str(story.bot.get_response(
                        Statement(text=query, search_text=query)))
                    user_chat = {"name": player, "text": query}
                    npc_chat = {"name": story.npc, "text": resp}
                    story.msg.append(user_chat)
                    story.msg.append(npc_chat)
                else:
                    story.chat_npc(npc)
        elif request.method == "GET":
            story = Story(player)

        return render_template("deathscape.html", data=story.current, talk=talk, msg=story.msg)


@app.route("/deathscape/button_room", methods=["GET", "POST"])
def button_room():
    global story
    player = request.args.get("player")

    if player == None:
        return redirect("/")
    else:
        story = Story(player)

        data = {
            "current": story.current,
            "room": story.button_room
        }

        return render_template("button_room.html", data=data)


@app.route("/deathscape/lab_room", methods=["GET", "POST"])
def lab_room():
    global story
    player = request.args.get("player")

    if player == None:
        return redirect("/")
    else:
        story = Story(player)

        data = {
            "current": story.current,
            "room": story.lab_room
        }

        return render_template("lab_room.html", data=data)


@app.route("/deathscape/justice_room", methods=["GET", "POST"])
def justice_room():
    global story
    player = request.args.get("player")

    if player == None:
        return redirect("/")
    else:
        story = Story(player)

        data = {
            "current": story.current,
            "room": story.justice_room
        }

        return render_template("justice_room.html", data=data)


@app.route("/deathscape/trap_room", methods=["GET", "POST"])
def trap_room():
    global story
    player = request.args.get("player")

    if player == None:
        return redirect("/")
    else:
        story = Story(player)

        data = {
            "current": story.current,
            "room": story.trap_room
        }

        return render_template("trap_room.html", data=data)


@app.route("/deathscape/dilemma_room", methods=["GET", "POST"])
def dilemma_room():
    global story
    player = request.args.get("player")

    if player == None:
        return redirect("/")
    else:
        story = Story(player)

        data = {
            "current": story.current,
            "room": story.dilemma_room
        }

        return render_template("dilemma_room.html", data=data)


@app.route("/chat", methods=["POST"])
def get_bot_response():
    userText = request.form["msg"]
    resp = str(chatbot.get_response(userText))

    print(userText)
    print(resp)

    return render_template("chat.html", userText=userText, response=resp)


if __name__ == "__main__":
    app.run(port=5000, debug=True)
