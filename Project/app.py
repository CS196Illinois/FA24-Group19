from flask import Flask, jsonify, render_template
import pandas as pd

app = Flask(__name__)

# route to find html
@app.route('/')
def index():
    return render_template('index.html')

# parse csv and return it as an array (list of lists)
@app.route('/data')
def get_csv_data():
    # read csv file
    df = pd.read_csv(r'FA24-Group19\Project\output.csv')  # parse csv with pandas
    df = df.head(500)  # get the first 500 rows
    
    # Convert to a list of lists (array-like structure)
    data = df.values.tolist()

    return jsonify(data)  # Send the array to the frontend

if __name__ == '__main__':
    app.run(debug=True)
