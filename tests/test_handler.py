import sys
sys.path.append('.')
sys.path.append('src')
sys.path.append('src/awslib')
import index
from unittest.mock import patch
import importlib
import common

# mock
current_module = sys.modules[__name__]
print('current_module:',current_module)

class TestHandler(object):
    def setup_method(self, method):
        print('called TestHandler.setup_method')
    def teardown_method(self, method):
        print('called TestHandler.teardown_method')
        
    def test_index_handler_heroes(self):
        event = {}
        event['httpMethod'] = 'GET'
        event['path'] = '/heroes'
        event['queryStringParameters'] = {}
        response = index.handler(event,None)
        print(response)
        assert response['statusCode'] == 200
        
        
    def test_index_handler_annotations(self):
        event = {}
        event['httpMethod'] = 'GET'
        event['path'] = '/annotations'
        event['queryStringParameters'] = {}
        response = index.handler(event,None)
        print(response)
        assert response['statusCode'] == 200

    
'''
# mock case
# https://docs.python.jp/3/library/unittest.mock-examples.html
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
'''

def test_dynamotest():
    event = {}
    event['httpMethod'] = 'GET'
    event['path'] = '/dynamo'
    event['queryStringParameters'] = {}
    event['body'] = {}


    with patch('boto3.resource') as boto3resource:
        def get_dynamo(name):
            class tbl():
                calledcount = 0
                def scan(self,params):
                    if self.calledcount < 5:
                        self.calledcount += 1
                        return {'items': [{'value': str(self.calledcount) }], 'flag':'next'}
                    else:
                        return {'items': [{'value': str(self.calledcount) }]}
            class dyn():
                def Table(self,str):
                    return tbl()
            return dyn()
        
        boto3resource.side_effect = get_dynamo

        # solution to mock global class instance
        #  reload module after mock
        #   therefore, this mock effect other test case. 
        #    so re-reload after with statement.
        importlib.reload(common)

        response = index.handler(event,None)
        print(response)
        assert response['items'][0]['value'] == '5'
    importlib.reload(common)

# better solution
#  explicity reload and re-reload in setup and teardown method
class TestDynamo(object):
    event = {
        'httpMethod' : 'GET',
        'path' : '/dynamo',
        'queryStringParameters' : {},
        'body' : {}
    }

    def setup_method(self, method):
        print('called TestHandler.setup_method')
        with patch('boto3.resource') as boto3resource:
            def get_dynamo(name):
                class tbl():
                    calledcount = 0
                    def scan(self,params):
                        if self.calledcount < 5:
                            self.calledcount += 1
                            return {'items': [{'value': str(self.calledcount) }], 'flag':'next'}
                        else:
                            return {'items': [{'value': str(self.calledcount) }]}
                class dyn():
                    def Table(self,str):
                        return tbl()
                return dyn()
            boto3resource.side_effect = get_dynamo
            importlib.reload(common)

    def teardown_method(self, method):
        print('called TestHandler.teardown_method')
        importlib.reload(common)

    def test_dynamo(self):
        response = index.handler(self.event,None)
        print(response)
        assert response['items'][0]['value'] == '5'

'''
def test_dynamo3():

    event = {}
    event['httpMethod'] = 'GET'
    event['path'] = '/dynamo'
    event['queryStringParameters'] = {}
    event['body'] = {}
    response = index.handler(event,None)
    print(response)
    assert False
'''