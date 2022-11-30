from chatterbot.conversation import Statement
from flask import Flask, redirect, request, render_template
from story import Story


app = Flask(__name__)
story = None


@app.errorhandler(404)
def page_not_found(e):
    return render_template("page_not_found.html"), 404


@app.route("/")
def index():
    return redirect("/deathscape")


@app.route("/deathscape", methods=["GET", "POST"])
def deathscape():
    if request.method == "POST":
        player = request.form["player_name"]

        return redirect("/deathscape/intro?player={}".format(player))
    else:
        return render_template("index.html")


@app.route("/deathscape/intro", methods=["GET", "POST"])
def intro():
    player = request.args.get("player")

    if player == None:
        return redirect("/deathscape")
    else:
        global story

        if request.method == "GET":
            story = Story(player)

            data = {
                "player": story.current["player"],
                "intro": story.intro
            }

            return render_template("intro.html", data=data)
        elif request.method == "POST":
            return redirect("/deathscape/button_room?player={}".format(player))


@app.route("/deathscape/button_room", methods=["GET", "POST"])
def button_room():
    player = request.args.get("player")

    if player == None:
        return redirect("/deathscape")
    else:
        global story

        dead = False
        solved = False
        talk = False

        if request.method == "POST":
            if "choice" in request.form:
                choice = request.form["choice"]

                # if choice == "Try the puzzle later":
                #     story.go_back(choice)
                # else:
                story.set_choices(choice)

                if "Press the golden button" in choice:
                    dead = True
                elif "golden button" in choice:
                    solved = True
            elif "character" in request.form:
                choice = request.form["character"]
                talk = True

                if choice == "back":
                    story.dont_talk()
                    talk = False
                elif choice == "end_conversation":
                    story.end_conversation()
                    talk = False
                elif choice == "talk":
                    query = request.form["messages"]
                    resp = str(story.current["bot"].get_response(
                        Statement(text=query, search_text=query)))

                    story.add_messages(query, resp)
                else:
                    story.add_character_to_story(choice)
                    story.set_bot(choice)
            elif "next" in request.form:
                # story.next()

                return redirect("/deathscape/lab_room?player={}".format(player))
            elif "restart" in request.form:
                return redirect("/")
        elif request.method == "GET":
            story = Story(player)

        return render_template("button_room.html", data=story.current, talk=talk, messages=story.current["messages"], solved=solved, dead=dead)


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

    # player = request.args.get("player")

    # if player == None:
    #     return redirect("/deathscape")
    # else:
    #     global story

    #     talk = False

    #     if request.method == "POST":
    #         if "choice" in request.form:
    #             choice = request.form["choice"]

    #             # if choice == "Try the puzzle later":
    #             #     story.go_back(choice)
    #             # else:
    #             story.set_choices(choice)
    #         elif "character" in request.form:
    #             choice = request.form["character"]
    #             talk = True

    #             if choice == "back":
    #                 story.dont_talk()
    #                 talk = False
    #             elif choice == "end_conversation":
    #                 story.end_conversation()
    #                 talk = False
    #             elif choice == "talk":
    #                 query = request.form["messages"]
    #                 resp = str(story.current["bot"].get_response(
    #                     Statement(text=query, search_text=query)))

    #                 story.add_messages(query, resp)
    #             else:
    #                 story.add_character_to_story(choice)
    #                 story.set_bot(choice)
    #         elif "next" in request.form:
    #             return redirect("/deathscape/justice_room?player={}".format(player))
    #         elif "restart" in request.form:
    #             return redirect("/")
    #     elif request.method == "GET":
    #         story = story

    #     return render_template("lab_room.html", data=story.current, talk=talk, messages=story.current["messages"])


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


if __name__ == "__main__":
    app.run(port=5000, debug=True)
