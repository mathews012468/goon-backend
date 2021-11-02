from flask import Flask
from flask import request
import translateAcronym as ta

app = Flask(__name__)

@app.route('/', methods=["GET"])
def translate():
    #the only url argument should be acronym
    goonAcronym = request.args.get('acronym', default="")
    goonAcronymDefined = ta.defineGoonAcronym(goonAcronym)

    #restrict to the first ten results
    goonAcronymDefinitionsList = goonAcronymDefined[:10]
    return {"Definitions": [goonWord["goon definition"] for goonWord in goonAcronymDefinitionsList]}

