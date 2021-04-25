from app.service.database import MessageProducer, MongoDriver


def table_KB():
    """

    """
    message_KB = MessageProducer(MongoDriver(host='localhost', port=27017,
                                             base="vulndb", collection="cve"))
    return message_KB.get_message_limit(50)


def get_cve_info(cve):
    """

    """
    try:
        cve_upper = str(cve).upper().replace(' ', '')
        cve_KB = MessageProducer(MongoDriver(host='localhost', port=27017,
                                             base="vulndb", collection="cve"))
        data = cve_KB.get_message({"cve": cve_upper})
    except Exception as e:
        data = []
    return data
