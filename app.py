from flask import Flask, request, jsonify
import subprocess
import os

app = Flask(__name__)
BEARER_TOKEN = os.environ.get('BEARER_TOKEN')

def verify_token(token):
    parts = token.split()
    if len(parts) == 2 and parts[0] == 'Bearer':
        token = parts[1]
    return token == BEARER_TOKEN

@app.route('/run-command', methods=['POST'])
def run_command():
    if not verify_token(request.headers.get('Authorization')):
        return jsonify({'error': 'Unauthorized'}), 401

    data = request.json
    command = data.get('command')
    
    # Security check: Validate and sanitize the command here

    try:
        output = subprocess.check_output(command, shell=True, text=True)
        return jsonify({'output': output})
    except subprocess.CalledProcessError as e:
        return jsonify({'error': str(e), 'output': e.output})

# New route for applying a unified patch
@app.route('/apply-patch', methods=['POST'])
def apply_patch():
    # Verify the authorization token
    if not verify_token(request.headers.get('Authorization')):
        return jsonify({'error': 'Unauthorized'}), 401

    data = request.json
    file_path = data.get('file_path')
    patch_content = data.get('patch_content')

    # Check if file_path and patch_content are provided
    if not file_path or not patch_content:
        return jsonify({'error': 'Missing file_path or patch_content'}), 400

    # Apply the patch using 'git apply'
    try:
        subprocess.run(['git', 'apply', '--cached', '--whitespace=nowarn', patch_content], check=True)
        return jsonify({'message': 'Patch applied successfully'})
    except subprocess.CalledProcessError as e:
        return jsonify({'error': 'Failed to apply patch: ' + str(e)})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

