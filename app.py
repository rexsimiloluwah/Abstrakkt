import json
import validators
import os
import pathlib
import shortuuid
from flask import Flask, send_file, render_template, request, jsonify, make_response
from werkzeug.utils import secure_filename
from helpers import AbstrakktHelpers 
app = Flask(__name__)


app.config['WORDS_PER_MINUTE'] = 210
app.config["MAX_CONTENT_LENGTH"] = 10 * 1024 * 1024
app.config["ALLOWED_EXTENSIONS"] = ["pdf"]
app.config["UPLOADS_DIR"] = "./uploads"

if not os.path.isdir(app.config["UPLOADS_DIR"]):
    os.mkdir(app.config["UPLOADS_DIR"])

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config["ALLOWED_EXTENSIONS"]

@app.errorhandler(413)
def too_large(e):
    return make_response(
        jsonify({"error":"Max file upload size size is 10MB"}), 413)

@app.route("/")
def homepage():
    return render_template('index.html')

@app.route("/summarize", methods=['GET','POST'])
def summarize_text():
    if request.method == "POST":
        print(request.get_json())
        mode = request.args.get("mode")
        n_keywords = request.args.get("n_keywords")
        raw_text = None
        url = None 
        raw_text = None

        if not mode in ["url", "raw_text"]:
            return make_response(
                jsonify({"error" : "Mode must be one of ['url', 'raw_text']"}), 400
            )
        
        if request.get_json():
            if mode == "url" and "url" not in request.get_json():
                return make_response(
                    jsonify({"error" : "url is required."}), 400
                )
            elif mode == "url" and "url" in request.get_json():
                url = request.get_json()["url"]
            
            if mode == "raw_text" and "raw_text" not in request.get_json():
                return make_response(
                    jsonify({"error" : "raw_text is required."}), 400
                )
            elif mode == "raw_text" and "raw_text" in request.get_json():
                raw_text = request.get_json()["raw_text"]
            
            if mode == "url" and not validators.url(url):
                return make_response(
                    jsonify({"error" : "url is invalid."}), 400
                )
        else:
            return make_response(
                jsonify({"error" : "url or raw_text is required."}),
                400
            )
        
        helpers = AbstrakktHelpers(url = url, raw_text = raw_text)
        if mode == "url":
            try:
                raw_text = helpers.fetch_from_url()
            except Exception as e:
                return make_response(
                    jsonify({"error" : e}), 400
                )
        
        response = {}
        try:
            summarized_text = helpers.gensim_summarize(raw_text)
            response["summarized_text"] = summarized_text
            if(len(summarized_text) == 0):
                return make_response(
                jsonify({"error" : "An unknown error occurred, could not summarize."}), 500
            )
            
            # Compute reading time in minutes (to 2 d.p)
            response["original_reading_time"] = round(len(raw_text)/app.config["WORDS_PER_MINUTE"], 2)
            response["reading_time"] = round(len(summarized_text)/app.config["WORDS_PER_MINUTE"], 2)
            n_keywords = n_keywords or 7
            response["keywords"] = helpers.extract_keywords(raw_text, n = int(n_keywords))

            return make_response(
                jsonify({"message" : "Summarization successful !", **response}), 200
            )
        except Exception as e:
            return make_response(
                jsonify({"error" : str(e)}), 500
            )
            
@app.route("/summarize/upload", methods = ["POST"])
def summarize_from_file():
    n_keywords = request.args.get("n_keywords")
    print(request.files)
    if not request.files.get("file"):
        return make_response(
            jsonify({"error" : "File upload is required."}), 400
        )

    file = request.files.get("file")
    extension = "".join([".", file.filename.split(".")[-1]])
    print(extension)
    if not allowed_file(extension):
        return make_response(jsonify({"error" : "Only .pdf files are allowed."}), 400)
    
    filename = secure_filename(file.filename)
    id = shortuuid.uuid()
    upload_path = os.path.join(app.config["UPLOADS_DIR"], f"{id}-{filename}")
    file.save(os.path.join(app.config["UPLOADS_DIR"], f"{id}-{filename}"))
    helpers = AbstrakktHelpers(upload_path = upload_path)
    content = helpers.read_from_pdf()
    summarized_content = []
    for page in content:
        try:
            summarized_content.append(helpers.gensim_summarize(page))
        except Exception as e:
            summarized_content.append(helpers.format_text(page))
    summarized_content = list(filter(lambda x : len(x) > 0, summarized_content))
    if(len(summarized_content) == 0):
        return make_response(
            jsonify({"error" : "An unknown error occurred, could not summarize."}), 500
        )
    response = {}
    response["summarized_pages"]= list(map(lambda x : {"page" : summarized_content.index(x), "summarized_text" : x}, summarized_content))
    response["original_reading_time"] = round(len(" ".join(content))/app.config["WORDS_PER_MINUTE"], 2)
    response["reading_time"] = round(len(" ".join(summarized_content))/app.config["WORDS_PER_MINUTE"], 2)
    n_keywords = n_keywords or 7
    response["keywords"] = helpers.extract_keywords(" ".join(summarized_content))

    return make_response(
        jsonify({"message" : "Summarization successful !", **response}), 200
    )


@app.route("/downloadpdf", methods=['POST','GET'])
def downloadpdf():
    return render_template("summarize.html")
        


if __name__ == "__main__":
    app.run(debug=True, port=5000)


