import configparser
from flask import Flask
from flask_restx import Api
import os

config = configparser.ConfigParser(inline_comment_prefixes=('#', ))

config.read('config.ini')

os.environ["MONGO_URI"] = config['CONFIG']['MONGO_URI']
os.environ["API_KEY"] = config['CONFIG']['API_KEY']

from database.db import initialize_db
from routes.routes import initialize_routes

app = Flask(__name__)
api = Api(
    app,
    title="Group Manager API",
    version="1.0",
    description="Group Manager API - Easy to use:)"
)

app.config['MONGODB_SETTINGS'] = {'host': config["CONFIG"]["MONGO_URI"]}

initialize_db(app)
initialize_routes(api)

if __name__ == "__main__":
    app.run(debug=True, port=80)