from unittest import TestCase
import json

from communication import protocol


class TestProtocol(TestCase):

    def test_parse_syn_request(self):
        request = protocol.create_syn_request()
        assert protocol.parse_request(request) == protocol.SYN

    def test_parse_reset_request(self):
        request = protocol.create_reset_request()
        assert protocol.parse_request(request) == protocol.RESET

    def test_parse_terminate_request(self):
        request = protocol.create_terminate_request()
        assert protocol.parse_request(request) == protocol.TERMINATE

    def test_parse_detect_request(self):
        request = protocol.create_detection_request('test_path', [1, 2])
        assert protocol.parse_request(request) == ('test_path', [1, 2], False)

    def test_parse_im_detect_request(self):
        request = protocol.create_image_detection_request('123')
        assert protocol.parse_request(request) == ('123', False)

    def test_parse_unknown_request(self):
        request = json.dumps({'type': 'test'})
        self.assertRaises(Exception, protocol.parse_request, request)

    def test_parse_known_request_not_expected(self):
        request = protocol.create_terminate_request()
        self.assertRaises(Exception, protocol.parse_request, request, [protocol.SYN])

    def test_parse_syn_response(self):
        response = protocol.create_syn_response(protocol.DETECT)
        assert protocol.parse_response(response) == protocol.DETECT

    def test_parse_terminate_response(self):
        response = protocol.create_terminate_response()
        assert protocol.parse_response(response) == protocol.TERMINATE

    def test_parse_detect_response(self):
        response = protocol.create_ed_response(protocol.DETECT, ({}, None))
        assert protocol.parse_response(response) == ({}, None)

    def test_parse_im_detect_response(self):
        response = protocol.create_ed_response(protocol.IM_DETECT, ({}, None))
        assert protocol.parse_response(response) == ({}, None)

    def test_parse_unknown_response(self):
        response = {'type': 'test'}
        self.assertRaises(Exception, protocol.parse_response, response)




