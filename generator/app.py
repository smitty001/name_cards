from flask import Flask, render_template, request, redirect, url_for, send_file
from placecardsv2 import *

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/', methods=['POST'])
def upload_file():
    uploaded_file = request.files['file']
    if uploaded_file.filename != '':
        uploaded_file.save(uploaded_file.filename)
        generate_pdf(uploaded_file.filename)
    return redirect(url_for('downloadFile'))

@app.route('/download')
def downloadFile ():
    path = "cards.pdf"
    return send_file(path, as_attachment=True)

app.run(host='0.0.0.0')
