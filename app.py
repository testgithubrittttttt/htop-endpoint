from flask import Flask, render_template_string
import subprocess
import os
import datetime
import pytz
import socket

app = Flask(__name__)

@app.route('/')
def index():
    return "Flask app is running. Go to /htop to see the endpoint."

@app.route('/htop')
def htop():
    try:
        # Your full name - REPLACE THIS WITH YOUR ACTUAL NAME
        name = "Dhruv sharma"
        
        # Get system username with fallback
        try:
            username = os.getlogin()
        except:
            try:
                import getpass
                username = getpass.getuser()
            except:
                username = os.environ.get('USER', 'unknown')
        
        # Get server time in IST
        ist = pytz.timezone('Asia/Kolkata')
        server_time = datetime.datetime.now(ist).strftime('%Y-%m-%d %H:%M:%S.%f%Z')
        
        # Get top output with safer execution
        try:
            top_process = subprocess.run(['top', '-b', '-n', '1'], capture_output=True, text=True, timeout=10)
            top_output = top_process.stdout
            if not top_output:
                top_output = "No output from top command"
        except subprocess.TimeoutExpired:
            top_output = "Top command timed out"
        except Exception as e:
            top_output = f"Error running top command: {str(e)}"
        
        html_template = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>HTOP Endpoint</title>
            <style>
                body {
                    font-family: monospace;
                    background-color: #333;
                    color: #fff;
                    padding: 20px;
                }
                pre {
                    white-space: pre-wrap;
                }
            </style>
        </head>
        <body>
            <p>Name: {{ name }}</p>
            <p>User: {{ username }}</p>
            <p>Server Time (IST): {{ server_time }}</p>
            <p>TOP output:</p>
            <pre>{{ top_output }}</pre>
        </body>
        </html>
        """
        
        return render_template_string(html_template, 
                                    name=name, 
                                    username=username, 
                                    server_time=server_time, 
                                    top_output=top_output)
    
    except Exception as e:
        return f"""
        <html>
        <body>
            <h1>Error Occurred</h1>
            <p>An error occurred while processing this request: {str(e)}</p>
        </body>
        </html>
        """, 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)