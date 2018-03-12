from elasticsearch import Elasticsearch, client

from env import *
from flask import jsonify


class Utils:
    def __init__(self):
        self.es = Elasticsearch([{"host": ELASTIC_HOST, "port": ELASTIC_PORT}])

    def create_index(self):
        indices_client = client.IndicesClient(self.es)
        if not indices_client.exists(PERSONS_INDEX):
            print('Creating new index')
            indices_client.create(PERSONS_INDEX)
            self.create_first_admin_user()

    def create_first_admin_user(self):
        admin = ADMINS[0]
        print('Adding {} to index'.format(admin))
        person = {key: 'Admin' for key in PERSON_REQUIRED_KEYS}
        person[PERSON_UNIQUE_KEY] = admin
        self.es.index(PERSONS_INDEX, PERSONS_TYPE, person)

    def update_person_with_json(self, person):
        try:
            existing = self.es.search(PERSONS_INDEX, PERSONS_TYPE, {
                'query': {
                    'match': {
                        PERSON_UNIQUE_KEY: {
                            'query': person[PERSON_UNIQUE_KEY],
                            'type': 'phrase'
                        }
                    }
                }
            })
            found = \
                [i for i in existing['hits']['hits'] if i['_source'][PERSON_UNIQUE_KEY] == person[PERSON_UNIQUE_KEY]][0]
        except:
            return jsonify({'status': 'Not found'}), 404
        found['_source'].update(person)
        self.es.index(PERSONS_INDEX, PERSONS_TYPE, found['_source'], found['_id'])
        return jsonify({'status': 'ok'})
