from flask import Flask
import exp
app = Flask(__name__)

@app.route("/")
def gen4teams():
    return str(exp.entry()).strip("[]")


def hello_world():
    return "hello, world!!!"
