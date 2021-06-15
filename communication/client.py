import communication.protocol as protocol
import socket
import struct


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
        serialized_data = bytes(data, encoding="utf-8")
        self.soc.sendall(struct.pack('>I', len(serialized_data)))
        self.soc.sendall(serialized_data)

    def get_response(self):
        data_size = struct.unpack('>I', self.soc.recv(4))[0]
        received_payload = b""
        reamining_payload_size = data_size
        while reamining_payload_size != 0:
            received_payload += self.soc.recv(reamining_payload_size)
            reamining_payload_size = data_size - len(received_payload)
        return str(received_payload.decode('utf-8'))


def get_free_port():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(("", 0))
    port = s.getsockname()[1]
    s.close()
    return port


def setup_connection(host, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    while True:
        try:
            s.connect((host, port))
            break
        except Exception as e:
            print(e)
    return s
