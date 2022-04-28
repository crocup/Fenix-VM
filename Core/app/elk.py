from elasticsearch import Elasticsearch


def send_elk(doc):
    es = Elasticsearch('https://login:password@localhost:9200', verify_certs=False)
    resp = es.index(index="test-discovery", document=doc)
    print(resp['result'])
