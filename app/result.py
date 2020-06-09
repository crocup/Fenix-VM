from app.models import ResultPost


def last_result():
    """

    :return:
    """
    item_last = ResultPost.query.all()
    return item_last[-1].uuid
