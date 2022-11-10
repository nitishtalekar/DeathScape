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
story = ""


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
    player = request.args.get("player")

    if player == None:
        return redirect("/")
    else:
        story = Story(player)

        return render_template("deathscape.html", data=story.current)


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
