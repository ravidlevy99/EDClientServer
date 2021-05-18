import json

SYN = 'SYN'
DETECT = 'DETECT'
CLASSIFY = 'CLASSIFY'
ERROR = 'ERROR'
TERMINATE = 'TERMINATE'

"""
    The format of the messages is:
        {
          'type': MESSAGE_TYPE,
          'data':
            {
              ANYTHING
            }
        }
"""


def create_syn_request():
    request = {'type': SYN}
    return request


def create_detection_request(image_path, region, bbox=False):
    request = {'type': DETECT, 'data': {'image_path': image_path, 'region': region, 'bbox': bbox}}
    return json.dumps(request)


def create_classification_request(image_path):
    request = {'type': CLASSIFY, 'data': {'image_path': image_path}}
    return json.dumps(request)


def create_terminate_request():
    request = {'type': TERMINATE}
    return json.dumps(request)


def parse_response(response):
    data = json.loads(response)
    if data['type'] == SYN:
        return data['data']['protocol']
    elif data['type'] == DETECT:
        return data['data']['detections'], data['data']['bbox'] if 'bbox' in data['data'] else None
    elif data['type'] == CLASSIFY:
        return data['data']['classification']
    elif data['type'] == ERROR:
        raise Exception('The event detector has return the following error:\n' + data['message'])
    else:
        raise Exception('Unknown response from server')


def create_error_response(message):
    response = {'type': ERROR, 'message': message}
    return response


def create_syn_response(protocol):
    response = {'type': SYN, 'data': {'protocol': protocol}}
    return response


def create_ed_response(protocol, response):
    if protocol == DETECT:
        detection, bbox = response
        return create_detection_response(detection, bbox)
    elif protocol == CLASSIFY:
        return create_classification_response(response)


def create_detection_response(detections, bbox=None):
    response = {'type': DETECT, 'data': {'detections': detections}}
    if bbox is not None:
        response['data']['bbox'] = bbox
    return json.dumps(response)


def create_classification_response(classification):
    response = {'type': CLASSIFY, 'data': {'classification': classification}}
    return response


def parse_request(request, expected_types=None):
    data = json.loads(request)
    if expected_types is not None and request['type'] not in expected_types:
        raise Exception('Incompatible request type')

    if data['type'] == SYN:
        return SYN
    elif data['type'] == DETECT:
        return data['data']['image_path'], data['data']['region'], data['data']['bbox']
    elif data['type'] == CLASSIFY:
        return data['data']['image_path']
    elif data['type'] == TERMINATE:
        return TERMINATE
    else:
        raise Exception('Unknown request from client')
