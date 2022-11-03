from __future__ import division, print_function
# coding=utf-8
import sys
import os
import glob
import re
import numpy as np
from flow import Story

# Flask utils
from flask import Flask, redirect, url_for, request, render_template
from werkzeug.utils import secure_filename
from gevent.pywsgi import WSGIServer

# ------------------------------------------------
# IMPORT REQUIRED
# ------------------------------------------------


# ------------------------------------------------
# PREPROCESSING FUCTION DEFINE
# ------------------------------------------------

app = Flask(__name__)

print('Check http://127.0.0.1:5000/')

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        player = request.form['player_name']
        return redirect('/deathscape?player='+player)
    return render_template('index.html')

@app.route('/deathscape', methods=['GET'])
def deathscape():
    player_name = request.args.get('player')
    story = Story(player_name)
    story.showPlayers()
    players = story.getPlayerNames()
    lvl = story.getCurrentLevel()
    room_info = story.callLevel(lvl)
    print(room_info['intro'])

    # Main page
    game_data = {"players":players,"room":room_info}
    return render_template('deathscape.html',data = game_data)


@app.route('/predict', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        num = request.form['number']
        
        # ------------------------------------------------
        # PREPROCESS INPUT
        # GET RESULT FROM MODEL
        # ------------------------------------------------

        return render_template('index.html',number=num)
    return None

if __name__ == '__main__':
    # app.run(port=5002, debug=True)

    # Serve the app with gevent
    http_server = WSGIServer(('0.0.0.0',5000),app)
    http_server.serve_forever()
