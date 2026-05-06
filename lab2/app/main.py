import os
from flask import Flask
app = Flask(__name__)

@app.route("/")
def hello():
    name = os.getenv("USER_NAME", "Guest")
    return f"<h1>Hello {name}</h1>"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)