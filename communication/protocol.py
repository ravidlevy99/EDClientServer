import json

DETECT = 'DETECT'
RECTS = 'RECTS'

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


def create_detection_request(image_path, region):
    request = {'type': DETECT, 'data': {'image_path': image_path, 'region': region}}
    return json.dumps(request)


def parse_request(request):
    data = json.loads(request)
    if data['type'] == DETECT:
        return data['data']['image_path'], data['data']['region']
    else:
        raise Exception('Unknown request from client')

def create_detection_response(detections):
    response = {'type': DETECT, 'data': {'detections': detections}}
    return json.dumps(response)

def parse_response(response):
    data = json.loads(response)
    if data['type'] == DETECT:
        return data['data']['detections']
    else:
        raise Exception('Unknown response from server')
