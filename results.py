from flask import Flask, render_template, request, send_file
import os
from googlesearch import search
import json
import csv

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/result', methods=['POST'])
def result():
    query = request.form['query']
    results = list(search(query, num_results=10))

    # Uložení výsledků do souboru ve formátu JSON
    json_results = json.dumps(results, indent=4)
    with open('results.json', 'w') as json_file:
        json_file.write(json_results)

    # Uložení výsledků do souboru ve formátu CSV
    with open('results.csv', 'w', newline='') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(['URL'])
        writer.writerows([[result] for result in results])

    return render_template('results.html', query=query, results=results)

@app.route('/download_csv')
def download_csv():
    filename = 'results.csv'
    if os.path.isfile(filename):
        return send_file(filename, as_attachment=True)
    else:
        return "CSV file not found."

@app.route('/download_json')
def download_json():
    filename = 'results.json'
    if os.path.isfile(filename):
        return send_file(filename, as_attachment=True)
    else:
        return "JSON file not found."
if __name__ == '__main__':
    app.run(debug=True)
