from flask import request as rq
from flask import jsonify
from google.cloud import storage
import uuid
import json

client = storage.Client()
BUCKET_NAME = "nuoblog-wish"

def response(data=None, status_code=200, headers=None):
    # Set CORS headers for the main request
    if headers is None:
        headers = {
            'Access-Control-Allow-Origin': '*'
        }
    return (jsonify({
        "data": data
    }), status_code, headers)

def create_content_in_bucket(data):
    blob = client.bucket(BUCKET_NAME).blob("%s.json" % uuid.uuid1())
    blob.upload_from_string(
        json.dumps(data), 
        content_type="application/json", 
        predefined_acl="publicRead"
    )
    return blob.public_url

def add_content(request):
    # import pdb;pdb.set_trace()
    # Set CORS headers for the preflight request
    if request.method == 'OPTIONS':
        # Allows GET requests from any origin with the Content-Type
        # header and caches preflight response for an 3600s
        headers = {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'GET',
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Max-Age': '3600'
        }

        return response('', 204, headers)

    elif request.method == 'POST':
        data = json.loads(request.get_data())
        blob_url = create_content_in_bucket(data)
        return response({
            'url': blob_url
        })
    return response(None, 403)

def main():
    return add_content(rq)