from app.service.database.database import Storage
notifications_data = Storage(db='notification', collection='notifications')


def notification_message():
    """

    :return:
    """
    return notifications_data.find_data_all().sort("_id", -1).limit(10)
