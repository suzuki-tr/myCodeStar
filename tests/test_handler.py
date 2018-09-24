import sys
sys.path.append('.')
sys.path.append('../src')
print('sys.path:',sys.path)
import index

# mock
current_module = sys.modules[__name__]

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
import object_detection.tf_objectdetection as tf_objectdetection
def test_index_handler_objdetect(monkeypatch):
    
    # mock function
    def dummy_function(arg):
        return {'statusCode':200}

    # replace to mock        
    monkeypatch.setattr(tf_objectdetection,
                        'handler',
                        dummy_function)
    event = {}
    event['httpMethod'] = 'GET'
    event['path'] = '/objdetect'
    event['queryStringParameters'] = {}
    response = index.handler(event,None)
    print(response)
    assert response['statusCode'] == 200
