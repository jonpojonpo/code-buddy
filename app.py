from flask import Flask, request, jsonify
import subprocess
import os

app = Flask(__name__)
BEARER_TOKEN = os.environ.get('BEARER_TOKEN')

def verify_token(token):
    return token == BEARER_TOKEN

@app.route('/run-command', methods=['POST'])
def run_command():
    #print(request.headers.get('Authorization'))
    #if not verify_token(request.headers.get('Authorization')):
    #    return jsonify({'error': 'Unauthorized'}), 401

    data = request.json
    command = data.get('command')
    print(command)
    
    # Security check: Validate and sanitize the command here

    try:
        output = subprocess.check_output(command, shell=True, text=True)
        return jsonify({'output': output})
    except subprocess.CalledProcessError as e:
        return jsonify({'error': str(e), 'output': e.output})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
