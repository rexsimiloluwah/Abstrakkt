import gensim
import nltk
from nltk import word_tokenize, sent_tokenize
import re
from nltk.corpus import stopwords
from gensim.summarization import summarize
import PyPDF2
import requests
from requests import Session
from bs4 import BeautifulSoup

stopwords = stopwords.words("english")

# Using Request session so it does not open a new session on each call 
s = Session()
headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) '\
            'AppleWebKit/537.36 (KHTML, like Gecko) '\
            'Chrome/75.0.3770.80 Safari/537.36'
            }
s.headers.update(headers)

class AbstrakktHelpers:
    def __init__(self, raw_text = None, url = None, upload_path = None):
        self.raw_text = raw_text
        self.url = url 
        self.upload_path = upload_path 

    def read_from_pdf(self):
        pdf_content = PyPDF2.PdfFileReader(open(self.upload_path,'rb'))
        content = []
        for i in range(0, pdf_content.numPages):
            pageObj = pdf_content.getPage(i)
            pdf_text = pageObj.extractText()
            if(len(pdf_text) > 20):
                content.append(pdf_text)
        return content

    def fetch_from_url(self):
        page = requests.get(self.url).content
        soup = BeautifulSoup(page)
        fetched_text = ' '.join(map(lambda p:p.text, soup.findAll('p')))
        return fetched_text

    @staticmethod
    def remove_newline(raw_text : str) -> str:
        sentences = []
        for i in raw_text.split():
            if i == "\n":
                continue
            else: sentences.append(i.replace("[^a-zA-Z]", " "))
        return " ".join(sentences)

    @staticmethod 
    def format_text(raw_text : str) -> str:
        print(raw_text)
        formatted_text = re.sub(r'\[[0-9]*\]', ' ', raw_text)
        formatted_text = re.sub(r'\s+', ' ', raw_text)
        return formatted_text


    def gensim_summarize(self, raw_text : str, n : int = 7) -> str:
        formatted_text = self.format_text(raw_text)
        word_frequencies = {}
        for word in nltk.word_tokenize(re.sub('[^a-zA-Z]',' ',formatted_text)):
            if word not in stopwords:
                if word not in word_frequencies.keys():
                    word_frequencies[word] = 1
                else:
                    word_frequencies[word] += 1
        keywords = [word for word in list(dict(sorted(word_frequencies.items(), key= lambda x:x[1], reverse=True)).keys()) if word.lower() not in stopwords and len(word) >= 3][:n]
        summarized = ' '.join(summarize(formatted_text).splitlines())
        return summarized


    def extract_keywords(self, raw_text : str, n : int = 7, show_definition : bool = True):
        formatted_text = self.format_text(raw_text)
        word_frequencies = {}
        for word in nltk.word_tokenize(re.sub('[^a-zA-Z]',' ',formatted_text)):
            if word not in stopwords:
                if word not in word_frequencies.keys():
                    word_frequencies[word] = 1
                else:
                    word_frequencies[word] += 1
        keywords = list(set([word.strip().lower() for word in list(dict(sorted(word_frequencies.items(), key= lambda x:x[1], reverse=True)).keys()) if word.strip().lower() not in stopwords and len(word.strip()) >= 3][:n]))
        if not show_definition:
            return keywords 
        response = [None for i in range(len(keywords))]
        for index,word in enumerate(keywords):
            try:
                response[index] = {}
                response[index]["word"] = word
                response[index]["definition"] = list(s.get(f'https://api.dictionaryapi.dev/api/v1/entries/en/{word}').json()[0]['meaning'].values())[0][0]["definition"]
            except Exception as e:
                print(e)
                response[index]["definition"] = "No Definition"
        return response
        
if __name__ == "__main__":
    helpers = AbstrakktHelpers(mode = "url", url = "https://codeometry.in/home-automation-using-nodemcu-and-google-assistant/", upload_path = "./uploads/akintade.pdf")
    raw_text = helpers.fetch_from_url()
    print(helpers.extract_keywords(raw_text))
    print(helpers.gensim_summarize(raw_text))
    # print(helpers.fetch_from_url())
    raw_text = "This is what I have been trying to say and it pisses me off that we cannot just maintain ourselves in this country, what kind of dance is this that is killing the entire nation and making us seem maybe like bad people"
