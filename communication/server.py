import socket


class Server:
    def __init__(self, port):
        self.conn = setup_connection('localhost', port)

    def get_request(self):
        return str(self.conn.recv(1024).decode('utf-8'))

    def answer(self, data):
        self.conn.sendall(bytes(data, encoding="utf-8"))



def setup_connection(host, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((host, port))
    s.listen()
    conn, addr = s.accept()
    return conn
