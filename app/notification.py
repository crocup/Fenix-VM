from app.service.database.database import Storage


def notification_message():
    """

    :return:
    """
    notifications_data = Storage(db='notification', collection='notifications')
    return notifications_data.find_data_all().sort("_id", -1).limit(10)


def telegram_message():
    notifications_data = Storage(db='setting', collection='notification')


def email_message():
    notifications_data = Storage(db='setting', collection='notification')

