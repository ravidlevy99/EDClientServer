import communication.protocol as protocol
import socket
import communication.jsonsocket as jsocket


class Client(jsocket.Client):
    def __init__(self):
        self.protocol = self.send_syn_request()

    def send_syn_request(self):
        request = protocol.create_syn_request()
        self.send_request(request)
        response = self.get_response()
        return protocol.parse_response(response)

    def stop_communication(self):
        self.send_request(protocol.create_terminate_request())
        if self.get_response() == protocol.TERMINATE:
            self.close()

    def send_request(self, data):
        self.send(data)

    def get_response(self):
        return self.recv()

    def setup_connection(self, host, port):
        while True:
            try:
                self.connect(host, port)
                break
            except Exception as e:
                print(e)


def get_free_port():
    return 55555
    # with socketserver.TCPServer(("localhost", 0), None) as s:
    #     return s.server_address[1]



