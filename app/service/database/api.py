"""
Сервис для работы с базой данных mongo
Автор: Dmitry Livanov, 2020
"""
import flask
from flask import jsonify, request, abort
import database

app = flask.Flask(__name__)


@app.route('/api/v1/database/mongo/upsert', methods=['POST'])
def database_upsert():
    if not request.json:
        abort(400)
    data = request.json
    upsert_data = database.Storage(db=data["base"], collection=data["collection"])
    upsert_data.upsert(name=data["data"]["name"], data=data["data"]["set"])
    upsert_data.close_connection()
    return jsonify({"data": "OK"})


@app.route('/api/v1/database/mongo/insert', methods=['POST'])
def database_insert():
    if not request.json:
        abort(400)
    data = request.json
    insert_data = database.Storage(db=data["base"], collection=data["collection"])
    insert_data.insert(data=data["data"])
    insert_data.close_connection()
    return jsonify({"data": "OK"})


@app.route('/api/v1/database/mongo/get_one', methods=['POST'])
def database_get_one():
    if not request.json:
        abort(400)
    data = request.json
    insert_data = database.Storage(db=data["base"], collection=data["collection"])
    result = insert_data.find_one(data=data["data"])
    insert_data.close_connection()
    return jsonify({"data": result})


if __name__ == '__main__':
    app.run(port=9002)
