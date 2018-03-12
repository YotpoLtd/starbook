import os

PERSON_REQUIRED_KEYS = os.getenv('PERSON_REQUIRED_KEYS', 'name,email,boss,title').split(',')
PERSONS_INDEX = os.getenv('PERSONS_INDEX', 'persons')
PERSONS_TYPE = os.getenv('PERSONS_TYPE', 'person')
PERSON_UNIQUE_KEY = os.getenv('PERSON_UNIQUE_KEY', 'email')
SOURCE_HOST = os.getenv('SOURCE_HOST', '0.0.0.0')
CLIENT_IDS = os.environ['CLIENT_IDS'].split(',')  # some-client-id.apps.googleusercontent.com,some-client-id2.apps.googleusercontent.com
CLIENT_ID = os.environ['CLIENT_ID']  # some-client-id.apps.googleusercontent.com
APPS_DOMAIN_NAME = os.environ['APPS_DOMAIN_NAME']  # my-domain.com
DEBUG = os.getenv('DEBUG', 'false').lower() == 'true'
ORIGIN = os.getenv('ORIGIN', 'http://localhost:8080')
APPLICATION_ROOT = os.environ['APPLICATION_ROOT'] or ''
ADMINS = (os.environ['ADMINS'] or '').split(',')  # me@my-domain.com,them@my-domain.com
LOGSTASH_HOST = os.getenv('LOGSTASH_HOST', None)
LOGSTASH_PORT = int(os.getenv('LOGSTASH_PORT', 0))
HIVE_API_ENDPOINT = os.environ['HIVE_API_ENDPOINT']  # http://api-endpoint.com
SEND_COOKIES = os.getenv('SEND_COOKIES', True)
FACEBOOK_APP_ID = os.environ['FACEBOOK_APP_ID']  # your-fb-app-id
ELASTIC_HOST = os.getenv('ELASTIC_HOST', 'elasticsearch')
ELASTIC_PORT = os.getenv('ELASTIC_PORT', '9200')
