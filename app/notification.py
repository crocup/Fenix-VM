from app.storage.database import Storage
notifications_data = Storage(db='notification', collection='notifications')


def notification_message():
    """

    :return:
    """
    return notifications_data.get().sort("_id", -1).limit(10)
