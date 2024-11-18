from flask import Flask, jsonify, render_template
import pandas as pd
import csv_interpreter

app = Flask(__name__)

# route to find html
@app.route('/')
def index():
    return render_template('index.html')

# parse csv and return it as an array (list of lists)
@app.route('/data')
def get_csv_data():
    return jsonify(csv_interpreter.job_skills_dict)  # Send the dictionary to the frontend

if __name__ == '__main__':
    app.run(debug=True)