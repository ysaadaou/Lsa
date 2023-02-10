from flask import Flask, request, render_template
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

def get_text_from_url(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    text = soup.get_text()
    return text

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Get text from URL
        if request.form.get('url'):
            url = request.form['url']
            text = get_text_from_url(url)

        # Get text from file
        elif request.files.get('file'):
            file = request.files['file']
            text = file.read().decode('utf-8')

        # Get text from textarea
        elif request.form.get('text'):
            text = request.form['text']

        # Summarize text
        parser = PlaintextParser.from_string(text, Tokenizer("arabic"))
        summarizer = LsaSummarizer()
        summary = ""
        for sentence in summarizer(parser.document, 3):
            summary += str(sentence)
        return render_template('index.html', summary=summary)
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
