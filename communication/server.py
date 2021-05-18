import communication.protocol as protocol
import socket
from abc import ABC, abstractmethod


class Server(ABC):
    def __init__(self, port, chosen_protocol):
        self.conn = setup_connection('localhost', port)
        self.protocol = chosen_protocol
        if self.get_syn_request(chosen_protocol):
            self.start_server_loop()

    def get_syn_request(self, chosen_protocol):
        request = self.get_request()
        try:
            protocol.parse_request(request, [protocol.SYN])
        except Exception as e:
            error = protocol.create_error_response(str(e))
            self.answer(error)
            return False

        response = protocol.create_syn_response(chosen_protocol)
        self.answer(response)
        return True

    def get_request(self):
        return str(self.conn.recv(1024).decode('utf-8'))

    def answer(self, data):
        self.conn.sendall(bytes(data, encoding="utf-8"))

    def start_server_loop(self):
        while True:
            request = self.get_request()
            try:
                data = protocol.parse_request(request, [self.protocol, protocol.TERMINATE])
                if data == protocol.TERMINATE:
                    break

                ed_data = self.handle_request(data)
                response = protocol.create_ed_response(self.protocol, ed_data)
                self.answer(response)
            except Exception as e:
                error = protocol.create_error_response(str(e))
                self.answer(error)
                break

    @abstractmethod
    def handle_request(self, data):
        pass


def setup_connection(host, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((host, port))
    s.listen()
    conn, addr = s.accept()
    return conn
