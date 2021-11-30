from flask import Flask, Response, request, render_template, redirect, url_for
import torch
import pickle
import joblib
import os
import difflib


app=Flask(__name__)

# model = pickle.load(open('model.pkl','rb'))

Allowed_Extensions = set(['txt'])

def check_file(file):
    return '.' in file and file.rsplit('.', 1)[1].lower() in Allowed_Extensions

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    error = None
    filename = None
    if request.method == 'POST':
        if 'file' not in request.files:
            error = 'No file selected'
            return render_template('index.html', error=error)

        file = request.files['file']
        filename = file.filename

        if filename == '':
            error = 'No file selected'
            return render_template('index.html', error=error)

        if check_file(filename) == False:
            error = 'File extension not allowed'
            return render_template('index.html', error=error)

        file.save(os.path.join("corrupt_version.txt"))
    return render_template('index.html', filename = filename)

@app.route('/result', methods=['GET', 'POST'])
def predict():
    
    # model.correct_from_file(src="corrupt_version.txt")

    # corrupt_file = 'file'
    corrupt_file = 'corrupt_version.txt'
    corrected_file = 'clean_version.txt'
    corrupt_file_lines = open(corrupt_file).readlines()
    corrected_file_lines = open(corrected_file).readlines()
    diff = difflib.HtmlDiff().make_file(corrupt_file_lines,
                                        corrected_file_lines,corrupt_file,
                                    corrected_file)
    diff_report = open('diff_report.html','w')
    diff_report.write(diff)
    diff_report.close()
    os.replace("diff_report.html", "templates/diff_report.html")
    return render_template('diff_report.html', diff_report = diff_report)


if __name__ == '__main__':
    app.run(debug=True)




