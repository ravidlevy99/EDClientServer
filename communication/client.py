import communication.protocol as protocol
import socket


class Client:
    def __init__(self, port):
        self.soc = setup_connection('localhost', port)
        self.protocol = self.send_syn_request()

    def send_syn_request(self):
        request = protocol.create_syn_request()
        self.send_request(request)
        response = self.get_response()
        return protocol.parse_response(response)

    def stop_communication(self):
        self.send_request(protocol.create_terminate_request())
        if self.get_response() == protocol.TERMINATE:
            self.soc.close()


    def send_request(self, data):
        self.soc.sendall(bytes(data, encoding="utf-8"))

    def get_response(self):
        return self.soc.recv(10000).decode('utf-8')


def get_free_port():
    return 55555
    # with socketserver.TCPServer(("localhost", 0), None) as s:
    #     return s.server_address[1]


def setup_connection(host, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    while True:
        try:
            s.connect((host, port))
            break
        except Exception as e:
            print(e)
    return s
