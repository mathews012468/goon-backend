from flask import Flask
from flask import request
from flask import send_from_directory
from flask import render_template
import translateAcronym as ta

app = Flask(__name__)

@app.route('/', methods=["GET"])
def entry():
    return render_template("index.html")

@app.route('/hello')
def a():
    return "Hello"

@app.route('/translate', methods=["GET"])
def translate():
    #the only url argument should be acronym
    goonAcronym = request.args.get('acronym', default="")
    goonAcronymDefined = ta.defineGoonAcronym(goonAcronym)

    #restrict to the first ten results
    goonAcronymDefinitionsList = goonAcronymDefined[:10]
    return {"Definitions": [goonWord["goon definition"] for goonWord in goonAcronymDefinitionsList]}
