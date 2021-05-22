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
    return json.dumps(request)


def create_detection_request(image_path, region, b_boxes=False):
    request = {'type': DETECT, 'data': {'image_path': image_path, 'region': region, 'b_boxes': b_boxes}}
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
        return data['data']['detection'], data['data']['b_boxes'] if 'b_boxes' in data['data'] else None
    elif data['type'] == CLASSIFY:
        return data['data']['classification']
    elif data['type'] == ERROR:
        raise Exception('The event detector has return the following error:\n' + data['message'])
    elif data['type'] == TERMINATE:
        return TERMINATE
    else:
        raise Exception('Unknown response from server')


def create_error_response(message):
    response = {'type': ERROR, 'message': message}
    return json.dumps(response)


def create_syn_response(protocol):
    response = {'type': SYN, 'data': {'protocol': protocol}}
    return json.dumps(response)


def create_ed_response(protocol, response):
    if protocol == DETECT:
        detection, b_boxes = response
        return create_detection_response(detection, b_boxes)
    elif protocol == CLASSIFY:
        return create_classification_response(response)


def create_detection_response(detection, b_boxes=None):
    response = {'type': DETECT, 'data': {'detection': detection}}
    if b_boxes is not None:
        response['data']['b_boxes'] = b_boxes
    return json.dumps(response)


def create_classification_response(classification):
    response = {'type': CLASSIFY, 'data': {'classification': classification}}
    return json.dumps(response)

def create_terminate_response():
    request = {'type': TERMINATE}
    return json.dumps(request)


def parse_request(request, expected_types=None):
    data = json.loads(request)
    if expected_types is not None and data['type'] not in expected_types:
        raise Exception('Incompatible request type')

    if data['type'] == SYN:
        return SYN
    elif data['type'] == DETECT:
        return data['data']['image_path'], data['data']['region'], data['data']['b_boxes']
    elif data['type'] == CLASSIFY:
        return data['data']['image_path']
    elif data['type'] == TERMINATE:
        return TERMINATE
    else:
        raise Exception('Unknown request from client')
