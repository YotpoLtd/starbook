from elasticsearch import Elasticsearch

from env import *
from flask import jsonify


class Utils:
    def __init__(self, cache):
        self.es = Elasticsearch([{"host": os.environ['ELASTIC_HOST'], "port": os.environ['ELASTIC_PORT']}])
        self.cache = cache

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
        except RuntimeError:
            return jsonify({'status': 'Not found'}), 404
        found['_source'].update(person)
        self.es.index(PERSONS_INDEX, PERSONS_TYPE, found['_source'], found['_id'])
        self.cache.clear_cache()
        return jsonify({'status': 'ok'})
