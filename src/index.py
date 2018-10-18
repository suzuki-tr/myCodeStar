import json
import logging
import common
import heroes
import annotations
import upload


print('Loading function')

#logger = logging.getLogger(__name__)
#logger.setLevel(logging.DEBUG)
logadapter = common.mylogger(__name__)

#############
# Handler
def handler(event, context):


    logadapter.info('start handler')
    logadapter.set_extra({'id':'0001'})
    logadapter.info("request:{}".format(json.dumps(event)))

    httpMethod = event['httpMethod']
    resourcePath = event.get('path','')
    queryStrings = event.get('queryStringParameters','')
    logadapter.info('{}:{}/param:{}'.format(httpMethod,resourcePath,queryStrings))

    if resourcePath.startswith('/heroes'):
        response = heroes.handler(event)
    elif resourcePath.startswith('/annotations'):
        response = annotations.handler(event)
    elif resourcePath.startswith('/objdetect'):
        import object_detection.tf_objectdetection as tf_objectdetection
        response = tf_objectdetection.handler(event)
    elif resourcePath.startswith('/upload'):
        response = upload.handler(event)
    elif resourcePath.startswith('/keepalive'):
        response = common.create_response(common.OK, 'keep alive')
    elif resourcePath.startswith('/warmup'):
        response = common.create_response(common.OK, 'warmup')
    else :
        response = common.create_response(common.BAD_REQUEST)
        logadapter.error('bad request')
        
    logadapter.info("response:{}".format(response))
    logadapter.info('end handler')
    return response
