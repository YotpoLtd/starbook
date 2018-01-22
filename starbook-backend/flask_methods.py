import json
from oauth2client import client, crypt
from api import Api
from env import *
from flask import request, jsonify, Flask, send_from_directory, render_template
from logger import log


class FlaskMethods:
    def __init__(self, api):
        self.app = Flask(__name__)
        static_file_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'static')
        app = self.app

        @app.route("/")
        def send_index():
            return render_template('index.html',
                                   client_id=CLIENT_ID,
                                   starbook_api=STAR_BOOK_API_ENDPOINT,
                                   send_cookies=int(SEND_COOKIES),
                                   facebook_app_id=FACEBOOK_APP_ID)

        @app.route("/static/<path:path>")
        def send_file(path):
            return send_from_directory(static_file_dir, path)

        @app.route(APPLICATION_ROOT, methods=['GET', 'POST'])
        def all_routes():
            if request.method == 'OPTIONS':
                return ''

            action = (request.json and request.json.pop('action', None)) or (
                request.args and request.args.pop('action', None))
            if not action:
                return '<html><body><h1>Hi there!</h1></body></html>'

            if action == 'tree':
                return api.tree()
            elif action == 'get_all':
                return api.get_all()
            elif action == 'query':
                return api.query()
            elif action == 'update_person':
                return api.update_person()
            elif action == 'add_person':
                return api.add_person()
            elif action == 'get_role':
                return Api.get_role()
            elif action == 'remove_person':
                return api.remove_person()
            else:
                return '<html><body><h1>Unknown action</h1></body></html>', 404

        @app.after_request
        def after_request(response):
            allow_origin = '*' if DEBUG else ORIGIN
            response.headers.add('Access-Control-Allow-Origin', allow_origin)
            response.headers.add('Access-Control-Allow-Credentials', str(not DEBUG).lower())
            response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
            response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
            return response

        @app.errorhandler(500)
        def internal_server_error(error):
            try:
                log({'error': repr(error)})
            except:
                print('failed to log error')
            return 'internal server error', 500

        @app.before_request
        def verify_token():
            if DEBUG or request.method == 'OPTIONS':
                return
            if request.path.startswith(static_file_dir):
                return
            token = request.cookies.get('starbook-token') or (request.json and request.json.get('starbook-token'))
            if not token:
                return jsonify({'error': 'no token'}), 401
            try:
                idinfo = client.verify_id_token(token, CLIENT_ID)
                # If multiple clients access the backend server:
                if idinfo['aud'] not in CLIENT_IDS:
                    return jsonify({'error': 'Unrecognized client'}), 401
                if idinfo['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
                    return jsonify({'error': 'Wrong issuer'}), 401
                if idinfo['hd'] != APPS_DOMAIN_NAME:
                    return jsonify({'error': 'Wrong hosted domain'}), 401
            except crypt.AppIdentityError as e:
                # Invalid token
                return jsonify({'error': 'Invalid token'}), 401

            log({'idinfo': idinfo, 'req': request.json, 'args': request.args})

            api.utils.update_person_with_json(
                {PERSON_UNIQUE_KEY: idinfo['email'], 'image': idinfo['picture'], 'google_id': idinfo['sub']})
