
from unittest import TestCase
from communication import client
import socket

class TestClient(TestCase):

    def test_get_free_port(self):
        passed = True
        port = client.get_free_port()
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        try:
            s.bind(("127.0.0.1", port))
        except socket.error as e:
            passed = False
        s.close()

        assert passed


