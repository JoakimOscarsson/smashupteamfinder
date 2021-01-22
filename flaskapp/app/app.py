from flask import Flask, render_template
import exp
app = Flask(__name__)

"""
@app.route("/")
def gen4teams():
    return str(exp.entry()).strip("[]")
"""

@app.route("/")
@app.route("/index")
def index():
    teams = exp.entry()
    return render_template("index.html", menu_title="World!", body_title="", teams=teams)
