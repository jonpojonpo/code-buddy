from flask import Flask, request, jsonify
import tempfile
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

    # Write the patch content to a temporary file and apply it
    try:
        with tempfile.NamedTemporaryFile(mode='w+', delete=False) as tmp_file:
            tmp_file.write(patch_content)
            tmp_file_path = tmp_file.name

        subprocess.run(['git', 'apply', '--whitespace=nowarn', tmp_file_path], check=True)

        return jsonify({'message': 'Patch applied successfully'})
    except subprocess.CalledProcessError as e:
        return jsonify({'error': 'Failed to apply patch: ' + str(e)})
    finally:
        # Clean up the temporary file
        try:
            os.remove(tmp_file_path)
        except OSError:
            pass  # Handle error if file doesn't exist

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

