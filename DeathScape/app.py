from flask import Flask, redirect, request, render_template
from story import Story


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

        # return redirect("/deathscape?player={}".format(player))
        return redirect("/deathscape/button_room?player={}".format(player))
    else:
        return render_template("index.html")


@app.route("/deathscape", methods=["GET", "POST"])
def deathscape():
    global story
    player = request.args.get("player")

    if player == None:
        return redirect("/")
    else:
        if request.method == "GET":
            story = Story(player)
        elif "choice" in request.form:
            story.set_choices(request.form["choice"])

        return render_template("deathscape.html", data=story.current)


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


# ChatBot responses
# @app.route("/chat")
# def get_bot_response():
#     userText = request.args.get("msg")
#     return str(chatbot.get_response(userText))


if __name__ == "__main__":
    app.run(port=5000, debug=True)

    # Serve the app with gevent
    # http_server = WSGIServer(("0.0.0.0",5000),app)
    # http_server.serve_forever()
