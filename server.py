import os

from flask import Flask
from apis.home import home_api
from apis.ignite import ignite_api

PORT = 8080

app = Flask(__name__)
app.debug = True
app.register_blueprint(home_api)
app.register_blueprint(ignite_api)
app.secret_key = 'development key'

if __name__ == '__main__':
    app.run(host= '0.0.0.0', port=PORT, use_reloader=False)

