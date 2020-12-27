from app import db_notification


def notification_message():
    result = db_notification["notifications"].find().sort("_id", -1).limit(10)
    # print(result)
    return result


def delete_notification():
    return db_notification["notifications"].remove()
