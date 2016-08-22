from flask import Flask, request, jsonify
from elasticsearch import Elasticsearch
from oauth2client import client, crypt
import os

app = Flask(__name__)
es = Elasticsearch([{"host": os.environ['ELASTIC_HOST'], "port": os.environ['ELASTIC_PORT']}])

PERSON_REQUIRED_KEYS = os.environ['PERSON_REQUIRED_KEYS'].split(',')
PERSONS_INDEX = os.environ['PERSONS_INDEX']
PERSONS_TYPE = os.environ['PERSONS_TYPE']
PERSON_UNIQUE_KEY = os.environ['PERSON_UNIQUE_KEY']
SOURCE_HOST = os.environ['SOURCE_HOST']
CLIENT_IDS = os.environ['CLIENT_IDS'].split(',')
CLIENT_ID = os.environ['CLIENT_ID']
APPS_DOMAIN_NAME = os.environ['APPS_DOMAIN_NAME']
DEBUG = os.environ['DEBUG'].lower() == 'true'
ORIGIN = os.environ['ORIGIN']
APPLICATION_ROOT = os.environ['APPLICATION_ROOT'] or ''


def add_person():
    person = request.json
    missing_keys = [key for key in PERSON_REQUIRED_KEYS if key not in person]
    if any(missing_keys):
        return jsonify({'error': 'the following keys are missing', 'keys': missing_keys}), 400
    try:
        existing = es.search(PERSONS_INDEX, PERSONS_TYPE, {
            'query': {
                'match': {
                    PERSON_UNIQUE_KEY: {
                        'query': person[PERSON_UNIQUE_KEY],
                        'type': 'phrase'
                    }
                }
            }
        })
        id = [i for i in existing['hits']['hits'] if i['_source'][PERSON_UNIQUE_KEY] ==
              person[PERSON_UNIQUE_KEY]][0]['_id']
    except:
        id = None
    res = es.index(PERSONS_INDEX, PERSONS_TYPE, person, id)
    return jsonify({'created': res['created']})


def update_person():
    person = request.json
    try:
        existing = es.search(PERSONS_INDEX, PERSONS_TYPE, {
            'query': {
                'match': {
                    PERSON_UNIQUE_KEY: {
                        'query': person[PERSON_UNIQUE_KEY],
                        'type': 'phrase'
                    }
                }
            }
        })
        found = [i for i in existing['hits']['hits'] if i['_source'][PERSON_UNIQUE_KEY] == person[PERSON_UNIQUE_KEY]][0]
    except:
        return jsonify({'status': 'Not found'}), 404
    found['_source'].update(person)
    es.index(PERSONS_INDEX, PERSONS_TYPE, found['_source'], found['_id'])
    return jsonify({'status': 'ok'})


def query():
    query = request.json
    res = es.search(PERSONS_INDEX, PERSONS_TYPE, {
        'size': 1000,
        'query': {
            'simple_query_string': {
                'query': query['query']
            }
        }
    })
    return jsonify(res)


def tree():
    res = es.search(PERSONS_INDEX, PERSONS_TYPE, {'size': 1000})
    persons = {}
    for p in res['hits']['hits']:
        persons[p['_source'][PERSON_UNIQUE_KEY]] = p['_source']

    for p in persons.keys():
        current_person = persons[p]
        his_boss = persons.get(current_person['boss'])
        if his_boss and his_boss.get('_children'):
            his_boss['_children'].append(current_person)
        elif his_boss:
            his_boss['_children'] = [current_person]

    p = list(persons.keys())[0]
    while persons.get(persons[p]['boss']):
        p = persons[persons[p]['boss']][PERSON_UNIQUE_KEY]

    return jsonify(persons[p])


@app.route(APPLICATION_ROOT, methods=['GET', 'POST'])
def all_routes():
    if request.method == 'OPTIONS':
        return ''

    action = (request.args and request.args.get('action', None)) or (request.json and request.json.get('action', None))
    if not action:
        return '<html><body><h1>Hi there!</h1></body></html>'

    if action == 'tree':
        return tree()
    elif action == 'query':
        return query()
    elif action == 'update_person':
        return update_person()
    elif action == 'add_person':
        return add_person()
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


@app.before_request
def verify_token():
    if DEBUG or request.method == 'OPTIONS':
        return
    token = request.cookies.get('starbook-token') or (request.json and request.json.get('starbook-token'))
    if request.json:
        request.json.pop('starbook-token', None)
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


if __name__ == "__main__":
    app.run(host=SOURCE_HOST)
