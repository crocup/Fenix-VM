"""
Сервис для работы с базой данных mongo
Автор: Dmitry Livanov, 2020
"""
import json

import flask
from flask import jsonify, request, abort
import database
from bson import json_util

app = flask.Flask(__name__)


@app.route('/api/v1/database_old/mongo/upsert', methods=['POST'])
def database_upsert():
    if not request.json:
        abort(400)
    data = request.json
    upsert_data = database.Storage(db=data["base"], collection=data["collection"])
    upsert_data.upsert(name=data["data"]["name"], data=data["data"]["set"])
    upsert_data.close_connection()
    return jsonify({"data": "OK"})


@app.route('/api/v1/database_old/mongo/insert', methods=['POST'])
def database_insert():
    if not request.json:
        abort(400)
    data = request.json
    insert_data = database.Storage(db=data["base"], collection=data["collection"])
    insert_data.insert(data=data["data"])
    insert_data.close_connection()
    return jsonify({"data": "OK"})


@app.route('/api/v1/database_old/mongo/get_one', methods=['POST'])
def database_get_one():
    if not request.json:
        abort(400)
    data = request.json
    insert_data = database.Storage(db=data["base"], collection=data["collection"])
    result = insert_data.find_one(data=data["data"])
    insert_data.close_connection()
    return jsonify({"data": result})


@app.route('/api/v1/database_old/mongo/get_all', methods=['POST'])
def database_get_all():
    if not request.json:
        abort(400)
    data = request.json
    get_data = database.Storage(db=data["base"], collection=data["collection"])
    result = get_data.find_data_all()
    json_docs = []
    for doc in result:
        json_doc = json.dumps(doc, default=json_util.default)
        json_docs.append(json_doc)
    count = len(json_docs)
    get_data.close_connection()
    return jsonify({"data": json_docs, "count": count})


if __name__ == '__main__':
    app.run(port=9002)
