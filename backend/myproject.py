from flask import Flask
from flask import request
application = Flask(__name__)

@application.route('/predict', methods=['GET', 'POST'])
def start_prediction():
    #read the JSON format
    #return the result in JSON format
    return request.data
    #return 'Your prediction is being run'

if __name__ == "__main__":
    application.run(host='0.0.0.0')
