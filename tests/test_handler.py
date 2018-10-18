import sys
sys.path.append('.')
sys.path.append('src')
print('sys.path:',sys.path)
import index

# mock
current_module = sys.modules[__name__]
print('current_module:',current_module)

def test_index_handler_heroes():
    event = {}
    event['httpMethod'] = 'GET'
    event['path'] = '/heroes'
    event['queryStringParameters'] = {}
    response = index.handler(event,None)
    print(response)
    assert response['statusCode'] == 200
    
    
def test_index_handler_annotations():
    event = {}
    event['httpMethod'] = 'GET'
    event['path'] = '/annotations'
    event['queryStringParameters'] = {}
    response = index.handler(event,None)
    print(response)
    assert response['statusCode'] == 200
    

# mock case
# https://docs.python.jp/3/library/unittest.mock-examples.html
from unittest.mock import patch
def test_index_handler_objdetect_post():
    event = {}
    event['httpMethod'] = 'POST'
    event['path'] = '/objdetect'
    event['queryStringParameters'] = {}
    event['body'] = {}
    
    with patch('base64.b64decode') as mock_base64decode:
        mock_base64decode.return_value = b'd\x00\xb0\x04'
        with patch('object_detection.tf_objectdetection.image_classifier.run_inference_file') as mock_run_inference_file:
            mock_run_inference_file.return_value = {'class':'1.0'}
            response = index.handler(event,None)
            print(response)
            assert response['statusCode'] == 200
