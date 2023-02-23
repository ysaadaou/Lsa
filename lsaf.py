from io import BytesIO
from PyPDF2 import PdfReader
from flask import Flask, request, render_template,make_response, jsonify
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer
import requests
from bs4 import BeautifulSoup
import re
import xml.etree.ElementTree as ET
import nltk
import numpy as np



def extract_transcript_text(xml_string):
    # Parse the XML string
    root = ET.fromstring(xml_string)
    
    # Extract the text from each <text> element and join them together
    text_list = [text_element.text for text_element in root.findall("./text")]
    i = 0
    full_text = ""
    for sent in text_list:
        if i == 0:
            full_text = sent
        elif i % 9 == 0:
            full_text = full_text +'. '+ sent
        elif i % 3 == 0:
            full_text = full_text +', '+ sent
        else:
            full_text = full_text +  ' ' + sent

        i = i + 1

    #full_text = " ".join(text_list)
    full_text = full_text.replace("&#39;", "'")
    return full_text
def get_youtube_transcript(youtube_url):
    # extract the timed text URL from the YouTube video page
    pattern = r'playerCaptionsTracklistRenderer.*?(youtube.com\/api\/timedtext.*?)\"'
    response = requests.get(youtube_url)
    match = re.search(pattern, response.text)

    if match:
        decoded_url = match.group(1).replace("\\u0026", "&")
        response = requests.get("https://"+decoded_url)
        xml_text = response.text
        full_text = extract_transcript_text(xml_text)
        return full_text
        

app = Flask(__name__)

def summarize(text, lang):
        
        parser = PlaintextParser.from_string(text, Tokenizer(lang))
        summarizer = LsaSummarizer()
        summary = ""
        for sentence in summarizer(parser.document, 4):
            summary += str(sentence)

        return summary
def get_text_from_url(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    p_tags = soup.find_all('p')
    text =''
    for p in p_tags:
        text += p.text
    return text

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == "POST":
        lang = request.form['language']
        # Get text from URL
        if request.form.get('url'):
            url = request.form['url']
            text = get_text_from_url(url)

        # Get text from file
        elif request.files.get('file'):
            file = request.files['file']
            if file.content_type == 'text/plain':
                text = file.read().decode('utf-8')
            elif file.content_type == 'application/pdf':
                pdf_bytes = file.read()
                with BytesIO(pdf_bytes) as pdf_stream:
                    pdf_reader = PdfReader(pdf_stream)
                    text = ''
                    for page in pdf_reader.pages:
                        text += page.extract_text()
        # Get text from textarea
        elif request.form.get('text'):
            text = request.form['text']
        #Get text from youtube video
        elif request.form.get('youtubeUrl'):
            youtube_url=request.form['youtubeUrl']
            text = str(get_youtube_transcript(youtube_url))
        else:
            text =""

        # Summarize text
        summary = summarize(text, lang)
        return render_template('indexe.html', summary=summary ,text=text)
    return render_template('indexe.html')

@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['file']
    file_content = file.read().decode('utf-8')
    return render_template('file.html', file_content=file_content)

@app.route("/process_file", methods=["POST"])
def process_file():
    file = request.files["file"]
    if file.content_type == 'text/plain':
        text = file.read().decode('utf-8')
    elif file.content_type == 'application/pdf':
        pdf_bytes = file.read()
        with BytesIO(pdf_bytes) as pdf_stream:
            pdf_reader = PdfReader(pdf_stream)
            text = ''
            for page in pdf_reader.pages:
                text += page.extract_text()
    processed_text = summarize(text, "english")
    # Process the text using your Python code

    response_data = {
            "original_text": text,
            "processed_text": processed_text
        }
    return jsonify(response_data)
#    response = make_response(text)
#    response.headers["Content-Type"] = "text/plain"
#    return response
if __name__ == '__main__':
    app.run(debug=True)
