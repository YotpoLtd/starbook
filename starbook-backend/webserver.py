from flask import Flask, request, jsonify
from elasticsearch import Elasticsearch
from oauth2client import client, crypt
import os
from redis import StrictRedis
import json
from hash_with_lru import HashWithLru

app = Flask(__name__)
es = Elasticsearch([{"host": os.environ['ELASTIC_HOST'], "port": os.environ['ELASTIC_PORT']}])
redis = StrictRedis(host=os.environ['REDIS_HOST'], port=os.environ['REDIS_PORT'], db=os.environ['REDIS_DB_NUM'])
queries_cache = HashWithLru('queries', int(os.environ['QUERIES_CACHE_SIZE']), redis)

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
REDIS_EXPIRY = int(os.environ['REDIS_EXPIRY'])

REDIS_RESPONSE_TREE_KEY = 'response:tree'
USAGE_COUNTER = 'usage_counter'


def clear_cache():
    redis.hset(USAGE_COUNTER, REDIS_RESPONSE_TREE_KEY, 0)
    queries_cache.clear()


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
    clear_cache()
    return jsonify({'created': res['created']})


def update_person_with_json(person):
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
    clear_cache()
    return jsonify({'status': 'ok'})


def update_person():
    person = request.json
    return update_person_with_json(person)


def query():
    query = request.json
    query_string = query['query']
    cached = queries_cache.get(query_string)
    if cached is not None:
        return jsonify(json.loads(cached.decode()))
    res = es.search(PERSONS_INDEX, PERSONS_TYPE, {
        'size': 1000,
        'query': {
            'simple_query_string': {
                'query': query_string
            }
        }
    })
    queries_cache.set(query_string, json.dumps(res).encode())
    return jsonify(res)


def tree():
    redis.hincrby(USAGE_COUNTER, REDIS_RESPONSE_TREE_KEY)
    tree_usage = int(redis.hget(USAGE_COUNTER, REDIS_RESPONSE_TREE_KEY).decode())
    if tree_usage > 3:
        cached = redis.get(REDIS_RESPONSE_TREE_KEY)
        return jsonify(json.loads(cached.decode()))
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

    res = persons[p]
    redis.set(REDIS_RESPONSE_TREE_KEY, json.dumps(res).encode(), ex=REDIS_EXPIRY)
    return jsonify(res)


@app.route(APPLICATION_ROOT, methods=['GET', 'POST'])
def all_routes():
    if request.method == 'OPTIONS':
        return ''

    action = (request.args and request.args.pop('action', None)) or (request.json and request.json.pop('action', None))
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

    outdated = False
    google_id_redis_key = 'google_id:{}'.format(idinfo['sub'])
    cached_google_info = redis.get(google_id_redis_key)
    if cached_google_info:
        google_info = json.loads(cached_google_info.decode())
        if google_info['image'] != idinfo['picture'] or google_info[PERSON_UNIQUE_KEY] != idinfo['email']:
            outdated = True
    else:
        outdated = True

    if outdated:
        update_person_with_json(
            {PERSON_UNIQUE_KEY: idinfo['email'], 'image': idinfo['picture'], 'google_id': idinfo['sub']})
        redis.set(google_id_redis_key,
                  json.dumps({'image': idinfo['picture'], PERSON_UNIQUE_KEY: idinfo['email']}).encode(),
                  ex=REDIS_EXPIRY)


if __name__ == "__main__":
    app.run(host=SOURCE_HOST)
