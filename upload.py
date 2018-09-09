import os
import json
import common
import base64
from datetime import datetime

myBucket = os.environ.get('bucket_name','uswestbucket-suzuki')
myPrefix = os.environ.get('prefix','voc_sample/JPEGImages/')

#################################
def handler(event):
    
    httpMethod = event['httpMethod']
    resourcePath = event.get('path','')
    queryStrings = event.get('queryStringParameters',None)
    targetKey = event['queryStringParameters'].get('key','') if queryStrings != None else ''
    print('{}:{}/{}'.format(httpMethod,resourcePath,targetKey))


    response = ''
    if httpMethod == 'POST':
        imageBody = base64.b64decode(event["body"])
        myKey  = myPrefix + datetime.now().strftime("%Y%m%d%H%M%S") + '.jpg'
        response = common.put_s3obj(myBucket,myKey,imageBody)
        print('file uploaded.',myKey)
        response = common.create_response(common.OK, response)
    else:
        response = common.create_response(common.METHOD_NOT_ALLOWED)
    return response
