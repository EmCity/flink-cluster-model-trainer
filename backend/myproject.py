from flask import Flask, render_template, current_app, request
import subprocess 

app = Flask(__name__, template_folder='../gui/src', static_folder='../gui/src')

@app.route('/')
def index():
	print(app.root_path)
	return render_template('index.html')

# for tests
@app.route('/runflinkjar')
def run_flink_jar():

	#out = subprocess.check_output("echo %cd%", shell=True) # win
	out = subprocess.check_output("pwd", shell=True) # linux

	cmd = 'flink-1.3.0/bin/flink run -c org.lmu.RunCMD2 BigDataScience/sose17-small-data/flink/flink-python-job/target/flink-python-job-0.1.jar -port 6123'
	
	out += subprocess.check_output(cmd, shell=True)

	return  out

@application.route('/predict', methods=['GET', 'POST'])
def start_prediction():
    #read the JSON format
    #return the result in JSON format
    return request.data
    #return 'Your prediction is being run'



if __name__ == "__main__":
    application.run(host='0.0.0.0')
