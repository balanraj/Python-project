from flask import Flask, render_template, request, jsonify
import paramiko

app = Flask(__name__)

# SSH function to connect and execute a Python script
def ssh_execute(hostname, username, password, remote_script_path):
    try:
        # Create an SSH client
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname, username=username, password=password)

        # Execute the Python script on the remote server
        stdin, stdout, stderr = ssh.exec_command(f"python3 {remote_script_path}")

        # Get the command's output and errors
        output = stdout.read().decode()
        error = stderr.read().decode()

        # Close the connection
        ssh.close()

        if error:
            return {"success": False, "error": error}
        return {"success": True, "output": output}
    except Exception as e:
        return {"success": False, "error": str(e)}

# Route to display the form
@app.route('/')
def index():
    return render_template('index.html')

# Route to handle SSH requests
@app.route('/ssh', methods=['POST'])
def ssh():
    data = request.form
    hostname = data['hostname']
    username = data['username']
    password = data['password']
    remote_script_path = data['script_path']

    # Call the SSH function
    result = ssh_execute(hostname, username, password, remote_script_path)
    return jsonify(result)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port='8080', debug=True)
