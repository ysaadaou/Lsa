from flask import Flask, render_template, request
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer

from bs4 import BeautifulSoup
import requests
app = Flask(__name__)

#text only

'''
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        text = request.form["text"]
        parser = PlaintextParser.from_string(text, Tokenizer("english"))
        summarizer = LsaSummarizer()
        summary = summarizer(parser.document, 3)
        return render_template("index.html", summary=summary)
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
    '''

#text and file
'''
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        if "file" in request.files:
            file = request.files["file"]
            text = file.read().decode("utf-8")
        else:
            text = request.form["text"]
        parser = PlaintextParser.from_string(text, Tokenizer("english"))
        summarizer = LsaSummarizer()
        summary = summarizer(parser.document, 3)
        
        return render_template("index.html", summary=summary)
    return render_template("index.html")
'''


#file + text + URL


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        if "url" in request.form:
            # Scrape the content of the blog post using BeautifulSoup
            response = requests.get(request.form["url"])
            soup = BeautifulSoup(response.text, "html.parser")
            text = soup.get_text()
        elif "file" in request.files:
            file = request.files["file"]
            text = file.read().decode("utf-8")
        else:
            text = request.form["text"]
        parser = PlaintextParser.from_string(text, Tokenizer("english"))
        summarizer = LsaSummarizer()
        summary = summarizer(parser.document, 3)
        
        return render_template("index.html", summary=summary)
    return render_template("index.html")
