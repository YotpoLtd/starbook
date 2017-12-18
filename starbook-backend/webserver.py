from api import Api
from env import *
from flask_methods import FlaskMethods
from utils import Utils

utils = Utils()
api = Api(utils)
flask_methods = FlaskMethods(api)


if __name__ == "__main__":
    flask_methods.app.run(host=SOURCE_HOST)
