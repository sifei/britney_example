import awsgi
import boto3
import os

from flask_cors import CORS
from flask import Flask, jsonify, request
from uuid import uuid4

client = boto3.client("dynamodb")
TABLE = os.environ.get("STORAGE_BRITNEYSONGSTORAGE_NAME")

app = Flask(__name__)
CORS(app)

# Constant variable with path prefix
BASE_ROUTE = "/song"

@app.route(BASE_ROUTE, methods=['POST'])
def create_song():
    request_json = request.get_json()
    client.put_item(TableName=TABLE, Item={
        'id': { 'S': str(uuid4()) },
        'name': {'S': request_json.get("name")},
        'year': {'S': request_json.get("year")},
        'link': {'S': request_json.get("link")},
    })
    return jsonify(message="item created") 

@app.route(BASE_ROUTE + '/<song_id>', methods=['GET'])
def get_song(song_id):
    item = client.get_item(TableName=TABLE, Key={
        'id': {
            'S': song_id
        }
    })
    return jsonify(data=item)

@app.route(BASE_ROUTE + '/<song_id>', methods=['PUT'])
def update_song(song_id):
    client.update_item(
        TableName=TABLE,
        Key={'id': {'S': song_id}},
        UpdateExpression='SET #name = :name, #year = :year, #link = :link',
        ExpressionAttributeNames={
            '#name': 'name',
            '#year': 'year',
            '#link': 'link'
        },
        ExpressionAttributeValues={
            ':name': {'S': request.json['name']},
            ':year': {'S': request.json['year']},
            ':link': {'S': request.json['link']},
        }
    )
    return jsonify(message="item updated")

@app.route(BASE_ROUTE + '/<song_id>', methods=['DELETE'])
def delete_song(song_id):
    client.delete_item(
        TableName=TABLE,
        Key={'id': {'S': song_id}}
    )
    return jsonify(message="song deleted")

def handler(event, context):
    return awsgi.response(app, event, context)

@app.route(BASE_ROUTE, methods=['GET'])
def list_songs():
    return jsonify(data=client.scan(TableName=TABLE))


