import json
import common
import heroes
import annotations
import upload

print('Loading function')

#############
# Handler
def handler(event, context):
    print("request: " + json.dumps(event))#, indent=2))

    httpMethod = event['httpMethod']
    resourcePath = event.get('path','')
    queryStrings = event.get('queryStringParameters','')
    print('{}:{}/param:{}'.format(httpMethod,resourcePath,queryStrings))

    if resourcePath.startswith('/heroes'):
        response = heroes.handler(event)
    elif resourcePath.startswith('/annotations'):
        response = annotations.handler(event)
    elif resourcePath.startswith('/upload'):
        response = upload.handler(event)
    elif resourcePath.startswith('/keepalive'):
        response = common.create_response(common.OK, 'keep alive')
    elif resourcePath.startswith('/warmup'):
        response = common.create_response(common.OK, 'warmup')
        
    else :
        response = common.create_response(common.BAD_REQUEST)
        
    print(response)
    return response
