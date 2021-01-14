from app import db_notification


def notification_message():
    """

    :return:
    """
    return db_notification["notifications"].find().sort("_id", -1).limit(10)


def delete_notification():
    """

    :return:
    """
    return db_notification["notifications"].remove()
