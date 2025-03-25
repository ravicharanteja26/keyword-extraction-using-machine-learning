from flask import Flask, request, jsonify, render_template
import os
from keyword_extractor import extract_keywords
import PyPDF2
import docx

app = Flask(__name__)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'txt', 'pdf', 'doc', 'docx',}

def extract_text_from_file(file_stream, filename):
    ext = filename.rsplit('.', 1)[1].lower()
    if ext == 'txt':
        return file_stream.read().decode('utf-8', errors='ignore')
    elif ext == 'pdf':
        reader = PyPDF2.PdfReader(file_stream)
        text = ""
        for page in reader.pages:
            text += page.extract_text() + "\n"
        return text
    elif ext in ['doc', 'docx']:
        doc = docx.Document(file_stream)
        text = "\n".join([para.text for para in doc.paragraphs])
        return text
    else:
        return ""

@app.route('/extract', methods=['POST'])
def extract():
    if 'file' not in request.files:
        return jsonify(error="No file provided"), 400
    file = request.files['file']
    if file.filename == "":
        return jsonify(error="No selected file"), 400
    if file and allowed_file(file.filename):
        try:
            file.stream.seek(0)
            text = extract_text_from_file(file.stream, file.filename)
            if not text:
                return jsonify(error="Unable to extract text from file"), 400
            keywords = extract_keywords(text)
            return jsonify(keywords=keywords)
        except Exception as e:
            return jsonify(error=str(e)), 500
    else:
        return jsonify(error="File type not allowed"), 400

@app.route('/')
def home():
    return render_template("index.html")

if __name__ == '__main__':
    app.run(debug=True)
