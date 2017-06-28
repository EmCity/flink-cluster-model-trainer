from flask import Flask, render_template, current_app, request
import subprocess 

application = Flask(__name__, template_folder='../gui/src', static_folder='../gui/src')

@application.route('/')
def index():
    print(application.root_path)
    return render_template('index.html')

# for tests
@application.route('/runflinkjar')
def run_flink_jar():
    
    job_name = 'testJob'
    job_def_json = '~/BigDataScience/sose17-small-data/flink/flink-python-job/src/main/java/org/lmu/JobDef.json'

    cmd1 = 'flink-1.3.0/bin/flink run -c org.lmu.RunCMD BigDataScience/sose17-small-data/flink/flink-python-job/target/flink-python-job-0.1.jar '
    
    cmd2 = 'flink-1.3.0/bin/flink run -c org.lmu.RunCMD2 BigDataScience/sose17-small-data/flink/flink-python-job/target/flink-python-job-0.1.jar '+ job_def_json
    cmd = cmd2


    #out = subprocess.check_output("echo %cd%", shell=True) # win
    out = 'called backend from: ' + subprocess.check_output("pwd", shell=True) # linux
    
    out += '<br><br>'
    out += 'job_def_json: ' + job_def_json
    
    out += '<br><br>'
    out += 'call: '+cmd
    
    out += '<br><br><hr>'
    outres = subprocess.check_output(cmd, shell=True)
    out += outres.replace('\n', '<br>')

    return  out

@application.route('/predict', methods=['GET', 'POST'])
def start_prediction():
    #read the JSON format
    #return the result in JSON format
    return request.data
    #return 'Your prediction is being run'



if __name__ == "__main__":
    application.run(host='0.0.0.0')
