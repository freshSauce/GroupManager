import configparser
from flask import Flask
from flask_restx import Api

from database.db import initialize_db
from routes.routes import initialize_routes

config = configparser.ConfigParser(inline_comment_prefixes=('#', ))

config.read('config.ini')

app = Flask(__name__)
api = Api(app)

app.config['MONGODB_SETTINGS'] = {'host': config["CONFIG"]["MONGO_URI"]}

initialize_db(app)
initialize_routes(api)

if __name__ == "__main__":
    app.run(debug=True)