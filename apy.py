import flask
import subprocess
from flask import request

app = flask.Flask(__name__)
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80)

@app.route('/', methods=['GET'])
def home():
    return "<h1>API home placeholder</h1>"

@app.route('/passthrough/api/v1/executeCommand', methods=['GET'])
def api_cmd():
    if 'cmd' in request.args:
    	cmd = request.args['cmd']
    else:
    	return "error"

    out = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, text=True)
    return "<div> command output: " + out.stdout + "</div>"
    
@app.route('/passthrough/api/v1/health', methods=['GET'])
def api_health():
    out = subprocess.Popen("echo Hello World", shell=True, stdout=subprocess.PIPE)
    subprocess_return = out.stdout.read()
    return "command output:" + str(subprocess_return)

app.run()
