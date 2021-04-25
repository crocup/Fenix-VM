"""
Оповещение в приложении
Dmitry Livanov, 2021
"""
import requests
from app.service.database import MessageProducer, MongoDriver


def notification_message():
    """
    Вывод последних 10 записей из БД
    :return: *Storage -> Cursor Database
    """
    notifications_data = MessageProducer(MongoDriver(host='localhost', port=27017,
                                                     base="notification", collection="notifications"))
    data = notifications_data.get_message_limit(10)
    return data


def telegram_message(message):
    """
    Отправка сообщения в telegram
    :param message: Сообщение (информация об оповещении)
    :return: None
    """
    try:
        notifications_data = MessageProducer(MongoDriver(host='localhost', port=27017,
                                                         base="setting", collection="notifications"))
        data = notifications_data.get_all_message()
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
    """
    Оправка сообщения на email
    ... доработка
    """
    notifications_data = MessageProducer(MongoDriver(host='localhost', port=27017,
                                                     base="setting", collection="notifications"))
