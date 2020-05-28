from omicron.models import ResultPost


def all_result():
    """

    :return:
    """
    ar_result = []
    all_task = ResultPost.query.all()
    for task in all_task:
        lists = [task.uid, task.uuid, task.name, task.dateofreg]
        ar_result.append(lists)
    # print(ar_result)
    return ar_result
