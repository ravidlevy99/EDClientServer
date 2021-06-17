from unittest import TestCase
from unittest.mock import patch, MagicMock, Mock
from communication import server, protocol


class MockServer(server.Server):

    def handle_request(self, data):
        return 1

    def reset(self):
        return


class TestServer(TestCase):

    @patch('communication.server.setup_connection')
    @patch('struct.unpack')
    def setUp(self, setup_conn, unpack):
        self.s = MockServer(1, protocol.DETECT)
        mock_conn = MagicMock()
        mock_conn.recv = Mock(return_value=[1])
        setup_conn.return_value = mock_conn
        unpack.return_value = 1


