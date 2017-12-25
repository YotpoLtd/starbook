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
ADMINS = (os.environ['ADMINS'] or '').split(',')
LOGSTASH_HOST = os.getenv('LOGSTASH_HOST', None)
LOGSTASH_PORT = int(os.getenv('LOGSTASH_PORT', 0))
USAGE_COUNTER = 'usage_counter'
