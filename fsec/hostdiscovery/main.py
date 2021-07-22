from concurrent import futures
import grpc
import hostdiscovery
import hostdiscovery_pb2
import hostdiscovery_pb2_grpc


class DataHostDiscoveryServicer(hostdiscovery_pb2_grpc.HostDiscoveryServicer):

    def arp_scan(self, request, context):
        response = hostdiscovery_pb2.ResultIp()
        response.ip, response.hostname, response.mac, response.date = hostdiscovery.arp_scan(request.data)
        return response


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=12))
    hostdiscovery_pb2_grpc.add_HostDiscoveryServicer_to_server(DataHostDiscoveryServicer(), server)
    print('Starting server on port 6066.')
    server.add_insecure_port('[::]:6066')
    server.start()
    # работаем час или до прерывания с клавиатуры
    try:
        while True:
            pass
    except KeyboardInterrupt:
        server.stop(0)


if __name__ == '__main__':
    serve()