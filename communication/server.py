import communication.protocol as protocol
import socket
from abc import ABC, abstractmethod
import queue
from threading import Thread
import struct


class Server(ABC):
    def __init__(self, port, chosen_protocol):
        self.conn = setup_connection('localhost', port)
        self.protocol = chosen_protocol
        self.queue = queue.Queue()
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
        data_size = struct.unpack('>I', self.conn.recv(4))[0]
        received_payload = b""
        reamining_payload_size = data_size
        while reamining_payload_size != 0:
            received_payload += self.conn.recv(reamining_payload_size)
            reamining_payload_size = data_size - len(received_payload)
        return str(received_payload.decode('utf-8'))

    def answer(self, data):
        serialized_data = bytes(data, encoding="utf-8")
        self.conn.sendall(struct.pack('>I', len(serialized_data)))
        self.conn.sendall(serialized_data)

    def ed_handle_request_loop(self):
        while True:
            data = self.queue.get()
            if data == protocol.RESET:
                self.reset()
                continue
            ed_data = self.handle_request(data)
            response = protocol.create_ed_response(self.protocol, ed_data)
            self.answer(response)

            self.queue.task_done()

    def start_server_loop(self):

        ed_handling_thread = Thread(target=self.ed_handle_request_loop, daemon=True)
        ed_handling_thread.start()

        while True:
            request = self.get_request()
            try:
                data = protocol.parse_request(request, [self.protocol, protocol.TERMINATE, protocol.RESET])
                if data == protocol.TERMINATE:
                    self.answer(protocol.create_terminate_response())
                    self.on_termination()
                    break
                self.queue.put(data)

            except Exception as e:
                error = protocol.create_error_response(str(e))
                self.answer(error)
                break

    @abstractmethod
    def handle_request(self, data):
        pass

    @abstractmethod
    def reset(self):
        pass

    def on_termination(self):
        self.conn.close()


def setup_connection(host, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((host, port))
    s.listen()
    conn, addr = s.accept()
    s.close()
    return conn
