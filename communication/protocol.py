import json

DETECT = 'DETECT'
CLASSIFY = 'CLASSIFY'

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


def create_detection_request(image_path, region, bbox=False):
    request = {'type': DETECT, 'data': {'image_path': image_path, 'region': region, 'bbox': bbox}}
    return json.dumps(request)


def create_classification_request(image_path):
    request = {'type': CLASSIFY, 'data': {'image_path': image_path}}
    return json.dumps(request)


def parse_response(response):
    data = json.loads(response)
    if data['type'] == DETECT:
        return data['data']['detections'], data['data']['bbox'] if 'bbox' in data['data'] else None
    elif data['type'] == CLASSIFY:
        return data['data']['classification']
    else:
        raise Exception('Unknown response from server')


def create_detection_response(detections, bbox=None):
    response = {'type': DETECT, 'data': {'detections': detections}}
    if bbox is not None:
        response['data']['bbox'] = bbox
    return json.dumps(response)


def create_classification_response(classification):
    response = {'type': CLASSIFY, 'data': {'classification': classification}}
    return response


def parse_request(request):
    data = json.loads(request)
    if data['type'] == DETECT:
        return data['data']['image_path'], data['data']['region'], data['data']['bbox']
    elif data['type'] == CLASSIFY:
        return data['data']['image_path']
    else:
        raise Exception('Unknown request from client')
