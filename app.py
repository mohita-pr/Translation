import os
from flask import Flask, request, render_template, url_for, redirect, send_file
import requests

app = Flask(__name__)

@app.route("/")
def fileFrontPage():
    return render_template('fileform.html')

@app.route("/handleUpload", methods=['POST'])
def handleFileUpload():
    if 'TanslationFile' in request.files:
        TanslationFile = request.files['TanslationFile']

    url = 'https://babelfish.bing-answerdata.microsoft-falcon.io/api/v1/translate?text='

    TanslationFile.seek(0)
    Lines = TanslationFile.read().decode('utf-8').splitlines() 

    file2 = open('languages.txt', 'r')
    Lang = file2.read().splitlines() 

    file3 = open('translation.tsv', 'w+', encoding="utf-8")
    file4 = open('lang.tsv', 'a+', encoding="utf-8")

    for intent in Lines:

        file3.write(intent)
        response = requests.get(url+intent, verify=False)
        res = response.json()
        translation = res["translation"]
        for l in Lang:
            file3.write("\t" + translation[l])
            file4.write(l + "\t")

        file3.write("\n")
        file4.write("\n")

    return redirect('/downloadfile/'+ TanslationFile.filename)

# # Download API
@app.route("/downloadfile/<filename>", methods = ['GET'])
def download_file(filename):
    
    file_path = "translation.tsv"
    return send_file(file_path, as_attachment=True, download_name='translated.tsv')

if __name__ == '__main__':
    app.run()     