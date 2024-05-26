# app.py
from flask import Flask
import os 
app = Flask(__name__)

@app.route('/')
def hello_world():
    # return current user that runs the app
    return f'Hello, World'
    

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)