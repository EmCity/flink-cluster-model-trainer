from flask import Flask
app = Flask(__name__)

@app.route('/predict')
def start_prediction():
	#read the JSON format
	#return the result in JSON format
    return 'Your prediction is being run'