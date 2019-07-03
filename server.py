import os

from flask import Flask
from apis.home import home_api

PORT = 8080

app = Flask(__name__)
app.register_blueprint(home_api)

if __name__ == '__main__':
    app.run(host= '0.0.0.0', port=AUTH_PORT, use_reloader=False)

