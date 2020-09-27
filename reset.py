#!/usr/bin/python3
from flask import Flask, render_template
import utils
import constants

app = Flask(__name__, template_folder="/home/wb/reindexer")

@app.route("/reindex")
def reIndex():
    utils.reset()
    return render_template("reset_template.html", poster=constants.broken)

@app.route("/random")
def random_movie():    
    info = utils.get_movie()
    return render_template("template.html", name=info)

if __name__ == "__main__":
   app.run(host="192.168.0.14",port=5000)  
