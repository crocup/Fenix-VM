from app import db
from app.models import ResultPost
from collections import deque


def last_result():
    """

    :return:
    """
    try:
        item_last = ResultPost.query.all()
        l_result = item_last[-1].uuid
        return l_result
    except IndexError:
        return None


def result_post(uid, name, time):
    res_id = ResultPost(uid, name, time)
    db.session.add(res_id)
    db.session.commit()


def log_file(file_name):
    with open(file_name) as f:
        log_result = list(deque(f, 30))
    return log_result
