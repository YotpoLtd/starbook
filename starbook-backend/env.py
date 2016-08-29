import os

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
ADMINS = (os.environ['ADMINS'] or '').split(',')
QUERIES_CACHE_SIZE = int(os.environ['QUERIES_CACHE_SIZE'])

REDIS_RESPONSE_TREE_KEY = 'response:tree'
USAGE_COUNTER = 'usage_counter'
