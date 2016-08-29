from api import Api
from cache import Cache
from env import *
from flask_methods import FlaskMethods
from utils import Utils


cache = Cache()
utils = Utils(cache)
api = Api(cache, utils)
flask_methods = FlaskMethods(api)


if __name__ == "__main__":
    flask_methods.app.run(host=SOURCE_HOST)
