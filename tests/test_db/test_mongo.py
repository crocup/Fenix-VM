from app.core.config import DATABASE_IP, DATABASE_PORT
from app.models.database import Message
from app.services.database import MessageProducer, MongoDriver

test_db = MessageProducer(MongoDriver(host=DATABASE_IP, port=DATABASE_PORT,
                                      base="Test", collection="test"))

message = {"test": "test"}
new_value = {"test": "test1"}


def test_insert_and_get_data():
    in_data = test_db.insert_message(message)
    data = test_db.get_message(message)
    for dt in data:
        data = dt
    assert data["test"] == "test"
    assert in_data == Message(success=True)


def test_get_all_message():
    data = test_db.get_all_message()
    data_list = list()
    for i in data:
        del i["_id"]
        data_list.append(i)
    assert data_list == [{'test': 'test'}]


def test_update_data():
    up_data = test_db.update_message(message, new_value)
    data = test_db.get_message(new_value)
    for dt in data:
        data = dt
    assert data["test"] == "test1"
    assert up_data == Message(success=True)


def test_delete_data():
    data = test_db.delete_message(new_value)
    assert data == Message(success=True)


def test_delete_no_data():
    data = test_db.delete_message(message)
    assert data == Message(success=True)
