from env import *
from flask import request, jsonify
from oauth2client import client


def verify_email_from_request():
    if DEBUG:
        return
    token = request.cookies.get('starbook-token') or (request.json and request.json.pop('starbook-token'))
    google_email = client.verify_id_token(token, CLIENT_ID)['email']
    request_email = request.json.get(PERSON_UNIQUE_KEY, None)
    if request_email is None:
        return
    if request_email != google_email and google_email not in ADMINS:
        return jsonify({'error': 'You are not allowed to do that'}), 403


def verify_admin():
    if DEBUG:
        return
    token = request.cookies.get('starbook-token') or (request.json and request.json.pop('starbook-token'))
    google_email = client.verify_id_token(token, CLIENT_ID)['email']
    if google_email not in ADMINS:
        return jsonify({'error': 'You are not allowed to do that'}), 403


def get_role():
    if DEBUG:
        return jsonify({'admin': True})
    token = request.cookies.get('starbook-token') or (request.json and request.json.pop('starbook-token'))
    google_email = client.verify_id_token(token, CLIENT_ID)['email']
    return jsonify({'admin': google_email in ADMINS})
