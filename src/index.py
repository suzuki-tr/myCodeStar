import os
import json
import logging

import common
import heroes
import annotations
import upload
import sys
sys.path.append('awslib')
from aws_xray_sdk.core import xray_recorder

print('Loading function')

logadapter = common.mylogger(__name__)

#############
# Handler
def handler(event, context):
    
    #xray_recorder.begin_segment(__name__)
    #xray_recorder.begin_subsegment('preprocess')
    logadapter.info(__name__)
    logadapter.set_extra({'id':'0001'})
    logadapter.info("request:{}".format(json.dumps(event)))

    httpMethod = event['httpMethod']
    resourcePath = event.get('path','')
    queryStrings = event.get('queryStringParameters','')
    logadapter.info('{}:{}/param:{}'.format(httpMethod,resourcePath,queryStrings))
    #xray_recorder.end_subsegment()

    if resourcePath.startswith('/heroes'):
        #xray_recorder.begin_subsegment('heroes')
        response = heroes.handler(event)
        #xray_recorder.end_subsegment()
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
    elif resourcePath.startswith('/dynamo'):
        response = common.dynamotest()
    else :
        response = common.create_response(common.BAD_REQUEST)
        logadapter.error('bad request')
        
    logadapter.info("response:{}".format(response))
    logadapter.info('end handler')
    
    #xray_recorder.end_segment()
    return response
