import requests
from app.service.database.database import Storage


def notification_message():
    """

    :return:
    """
    notifications_data = Storage(db='notification', collection='notifications')
    return notifications_data.find_data_all().sort("_id", -1).limit(10)


def telegram_message(message):
    """

    :param message:
    :return:
    """
    try:
        notifications_data = Storage(db='setting', collection='notification')
        data = notifications_data.find_data_all()
        for item in data:
            bot = item['telegram_bot_api']
            chat_id = item['telegram_chat_id']
            requests.get('https://api.telegram.org/bot{}/sendMessage'.format(bot), params=dict(
                chat_id=chat_id,
                text=message
            ))
    except Exception as e:
        print(e)


def email_message():
    notifications_data = Storage(db='setting', collection='notification')
