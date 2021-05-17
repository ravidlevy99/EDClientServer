import socketserver
import socket


class Client:
    def __init__(self, port):
        self.soc = setup_connection('localhost', port)

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






















