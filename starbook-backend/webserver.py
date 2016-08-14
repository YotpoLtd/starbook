from flask import Flask, request, jsonify
from elasticsearch import Elasticsearch
import os

app = Flask(__name__)
es = Elasticsearch([{"host": os.environ['ELASTIC_HOST'], "port": os.environ['ELASTIC_PORT']}])

PERSON_REQUIRED_KEYS = os.environ['PERSON_REQUIRED_KEYS'].split(',')
PERSONS_INDEX = os.environ['PERSONS_INDEX']
PERSONS_TYPE = os.environ['PERSONS_TYPE']
PERSON_UNIQUE_KEY = os.environ['PERSON_UNIQUE_KEY']
SOURCE_HOST = os.environ['SOURCE_HOST']


@app.route('/add_person', methods=['POST'])
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


@app.route('/update_person', methods=['POST'])
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


@app.route('/query', methods=['POST'])
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


@app.route('/tree', methods=['GET'])
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


@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
    return response


if __name__ == "__main__":
    app.run(host=SOURCE_HOST)
