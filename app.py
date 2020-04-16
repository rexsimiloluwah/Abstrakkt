from flask import Flask, send_file, render_template, request, jsonify
import gensim
# import sumy
import nltk
from nltk import word_tokenize, sent_tokenize
import re
# from nltk.corpus import stopwords
from gensim.summarization import summarize
import PyPDF2
import requests
from bs4 import BeautifulSoup

# nltk.download('stopwords')

app = Flask(__name__)

stopwords = ['i','me','my','myself','we','our','ours','ourselves','you',"you're","you've","you'll","you'd",'your','yours','yourself','yourselves','he','him',
 'his','himself','she',"she's",'her','hers','herself','it',"it's",'its','itself','they','them','their','theirs','themselves','what','which',
 'who','whom','this','that',"that'll",'these','those','am','is','are','was','were','be','been','being','have','has','had','having','do','does','did',
 'doing','a','an','the','and','but','if','or','because','as','until','while','of','at','by','for','with','about','against','between','into',
  'through','during','before','after','above','below','to','from','up','down','in','out','on','off','over','under','again','further','then',
 'once','here','there','when','where','why','how','all','any','both','each','few','more','most','other','some','such','no','nor','not','only',
 'own','same','so','than','too','very','s','t','can','will','just','don',"don't",'should',"should've",'now','d','ll','m','o','re','ve','y',
 'ain','aren',"aren't",'couldn',"couldn't",'didn',"didn't",'doesn',"doesn't",'hadn',"hadn't",'hasn',"hasn't",'haven',"haven't",'isn',"isn't",
 'ma','mightn',"mightn't",'mustn', 'needn',"needn't",'shan',"shan't", 'shouldn', "shouldn't", 'wasn', "wasn't", 'weren', "weren't", 'won',"won't",
 'wouldn',"wouldn't"]

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
        if word not in stopwords:
            if word not in word_frequencies.keys():
                word_frequencies[word] = 1
            else:
                word_frequencies[word] += 1
    #keywords extraction

    keywords = [word for word in list(dict(sorted(word_frequencies.items(), key= lambda x:x[1], reverse=True)).keys()) if word.lower() not in stopwords and len(word) >= 3][:7]
    summarized = ' '.join(summarize(formatted_text).splitlines())
    
    return(len(rawtext), len(summarized), summarized, keywords)

def get_keywords(rawtext):
    formatted_text = re.sub(r'\[[0-9]*\]', ' ', rawtext)
    formatted_text = re.sub(r'\s+', ' ', formatted_text)
    
    word_frequencies = {}
    for word in nltk.word_tokenize(re.sub('[^a-zA-Z]',' ',formatted_text)):
        if word not in stopwords:
            if word not in word_frequencies.keys():
                word_frequencies[word] = 1
            else:
                word_frequencies[word] += 1
    #keywords extraction

    keywords = [word for word in list(dict(sorted(word_frequencies.items(), key= lambda x:x[1], reverse=True)).keys()) if word.lower() not in stopwords and len(word) >= 3][:7]
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


