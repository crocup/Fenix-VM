import grpc
import hostdiscovery_pb2
import hostdiscovery_pb2_grpc


# открываем канал и создаем клиент
channel = grpc.insecure_channel('localhost:6066')
stub = hostdiscovery_pb2_grpc.HostDiscoveryStub(channel)

# текст
text = '192.168.1.0/24'

# запрос за arp_scan
to_md5 = hostdiscovery_pb2.Text(data=text)
response = stub.arp_scan(to_md5)
print(response)
