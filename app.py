from flask import Flask, send_file, render_template, request, jsonify
import gensim
import sumy
import nltk
from nltk import word_tokenize, sent_tokenize
import re
from nltk.corpus import stopwords
from gensim.summarization import summarize
import PyPDF2
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

def readPdf(file_upload):
    pdf_content = PyPDF2.PdfFileReader(open(file_upload,'rb'))
    content = []
    for i in range(0, pdf_content.numPages):
        pageObj = pdf_content.getPage(i)
        pdf_text = pageObj.extractText()
        content.append(pdf_text)
    return content

def fetch_from_url(url):
    page = requests.get(url).content
    soup = BeautifulSoup(page)
    fetched_text = ' '.join(map(lambda p:p.text, soup.findAll('p')))
    return fetched_text

def gensim_summarize(rawtext):
    formatted_text = re.sub(r'\[[0-9]*\]', ' ', rawtext)
    formatted_text = re.sub(r'\s+', ' ', formatted_text)
    
    word_frequencies = {}
    for word in nltk.word_tokenize(re.sub('[^a-zA-Z]',' ',formatted_text)):
        if word not in nltk.corpus.stopwords.words('english'):
            if word not in word_frequencies.keys():
                word_frequencies[word] = 1
            else:
                word_frequencies[word] += 1
    #keywords extraction

    keywords = [word for word in list(dict(sorted(word_frequencies.items(), key= lambda x:x[1], reverse=True)).keys()) if word.lower() not in nltk.corpus.stopwords.words('english') and len(word) >= 3][:7]
    summarized = ' '.join(summarize(formatted_text).splitlines())
    
    return(len(rawtext), len(summarized), summarized, keywords)

def get_keywords(rawtext):
    formatted_text = re.sub(r'\[[0-9]*\]', ' ', rawtext)
    formatted_text = re.sub(r'\s+', ' ', formatted_text)
    
    word_frequencies = {}
    for word in nltk.word_tokenize(re.sub('[^a-zA-Z]',' ',formatted_text)):
        if word not in nltk.corpus.stopwords.words('english'):
            if word not in word_frequencies.keys():
                word_frequencies[word] = 1
            else:
                word_frequencies[word] += 1
    #keywords extraction

    keywords = [word for word in list(dict(sorted(word_frequencies.items(), key= lambda x:x[1], reverse=True)).keys()) if word.lower() not in nltk.corpus.stopwords.words('english') and len(word) >= 3][:7]
    return keywords


@app.route("/")
def homepage():
    return render_template('index.html')

@app.route("/summarize", methods=['GET','POST'])
def summarize_text():
    if request.method == "POST":
        mode = request.form['documentMode']
        rawText = request.form['raw-text']
        urlLink = request.form['urllink']
        file = request.files['file']
        
        text = ''
        if mode == 'raw-text':
            try:

                text = rawText
                raw_text_length, summarized_text_length, summarized_text, keywords = gensim_summarize(text)
                keydef = {}
                for i in keywords:
                    try:
                        keydef[i] = list(requests.get('https://api.dictionaryapi.dev/api/v1/entries/en/{}'.format(i)).json()[0]['meaning'].values())[0][0]['definition']
                    except:
                        keydef[i] = 'No Definition'
                reading_time = summarized_text_length/200
                prev_reading_time = raw_text_length/200

                return render_template('index.html',prev_reading_time = prev_reading_time, reading_time =reading_time, summarized_text = summarized_text, keydef=keydef)
            except:
                return render_template('index.html',  text = "Unable to Summarize ! Please input a Valid document or Check your data Connection")
        
        elif mode == "url-link":
            try:
                text = fetch_from_url(urlLink)
                raw_text_length, summarized_text_length, summarized_text, keywords = gensim_summarize(text)
                keydef = {}
                for i in keywords:
                    try:
                        keydef[i] = list(requests.get('https://api.dictionaryapi.dev/api/v1/entries/en/{}'.format(i)).json()[0]['meaning'].values())[0][0]['definition']
                    except:
                        keydef[i] = 'No Definition'
                reading_time = summarized_text_length/200
                prev_reading_time = raw_text_length/200
                return render_template('index.html', prev_reading_time=prev_reading_time, reading_time=reading_time, summarized_text = summarized_text, keydef = keydef)
            except:
                return render_template('index.html', text="Unable to Summarize ! Please input a Valid document or Check your data Connection")

        
        elif mode == "pdf":
            try:
                filename = file.filename
                file.save(filename)
                text = readPdf(filename)
                raw_text_length = [] ; summarized_text_length =[] ; summarized_text = []; dummy_kw = []
                for pagefile in text:
                    rtl,stl,st,k = gensim_summarize(pagefile)
                    raw_text_length.append(rtl)
                    summarized_text_length.append(stl)
                    summarized_text.append(st)
                keywords = get_keywords(''.join(text))
                keydef = {}
                for i in keywords:
                    try:
                        keydef[i] = list(requests.get('https://api.dictionaryapi.dev/api/v1/entries/en/{}'.format(i)).json()[0]['meaning'].values())[0][0]['definition']
                    except:
                        keydef[i] = 'No Definition'
                reading_time = sum(summarized_text_length)/200
                prev_reading_time = sum(raw_text_length)/200


                return render_template('index.html', prev_reading_time=prev_reading_time, mode = mode, reading_time= reading_time,summarized_text_length= summarized_text_length, summarized_text = [re.sub("\n","",i) for i in summarized_text], keydef =keydef)
            except:
                return render_template('index.html', text="Unable to Summarize ! Please input a Valid Document or check your data Connection")
        else:

            return render_template('index.html')
    return "OK"

@app.route("/downloadpdf", methods=['POST','GET'])
def downloadpdf():
    return render_template("summarize.html")
        


if __name__ == "__main__":
    app.run(debug=True, port=5000)


