from elasticsearch import Elasticsearch

from env import *
from flask import jsonify


class Utils:
    def __init__(self):
        self.es = Elasticsearch([{"host": os.environ['ELASTIC_HOST'], "port": os.environ['ELASTIC_PORT']}])

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
