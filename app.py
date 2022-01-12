import flask
import subprocess
from flask import request

app = flask.Flask(__name__)
app.config['DEBUG'] = True
p = False

def basicCookieAuth(request):
    if request.cookies.get('cookieAuth') == 'cookieAuth':
        return True
    return False

@app.route('/', methods=['GET'])
def home():
    return "<h1>API home placeholder</h1>"

@app.route('/passthrough/api/v1/executeCommand', methods=['GET'])
def api_executeCommand():
    if(not basicCookieAuth(request)):
        return '0'
    global p
    if 'cmd' in request.args:
    	cmd = request.args['cmd']
    else:
    	return "error no command found"

    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr = subprocess.STDOUT)

    response = flask.jsonify({"command":cmd})
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response

@app.route('/passthrough/api/v1/getCommandOutput', methods=['GET'])
def api_getCommandOutput():
    if(not basicCookieAuth(request)):
        return '0'
    global p
    if p:
        response = flask.jsonify({"result": p.stdout.readline().decode()})
    else:
        response = flask.jsonify({"result":''})

    response.headers.add("Access-Control-Allow-Origin", "*")
    return response
    
@app.route('/passthrough/api/v1/health', methods=['GET'])
def api_health():
    p = subprocess.Popen("echo Hello World", shell=True, stdout=subprocess.PIPE)
    out, err = p.communicate()
    return "command output:" + out.decode()
