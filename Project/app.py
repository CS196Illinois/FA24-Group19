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
    
    # Convert the DataFrame to a list of dictionaries (JSON-serializable)
    data = df.to_dict(orient='records')
    
    # Return the data as JSON

    return jsonify(data)  # Send the array to the frontend

if __name__ == '__main__':
    app.run(debug=True)
