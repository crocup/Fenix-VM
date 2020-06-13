from app.models import ResultPost


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
