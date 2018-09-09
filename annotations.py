import os
import json
import common
import base64

myBucket = os.environ.get('BUCKET_NAME','samplebucket-suzuki')
datasetdir = os.environ.get('DATASET_DIR','dataset')
datasetname = os.environ.get('DATASET_NAME','mahjong')
jsonPrefix = os.environ.get('annotation_dir','Annotations/')
jpegPrefix = os.environ.get('jpeg_dir','JPEGImages/')
thisResource = '/annotations'

#################################
def handler(event):
    print(thisResource,' is called')
    httpMethod = event['httpMethod']
    resourcePath = event.get('path','')
    queryStrings = event.get('queryStringParameters',None)
    targetKey = event['queryStringParameters'].get('key','') if queryStrings != None else ''
    print('{}:{}/{}'.format(httpMethod,resourcePath,targetKey))

    if not resourcePath.startswith(thisResource):
        response = common.create_response(common.BAD_REQUEST)
        print(resourcePath,' is not ',thisResource)
        return response

    response = ''
    if httpMethod == 'GET':
        if targetKey == '':
            key_prefix = os.path.join(datasetdir,datasetname,jsonPrefix)
            print(myBucket,key_prefix)
            annotationKeys = common.get_s3list(myBucket,key_prefix,'.json')
            keys = [os.path.splitext(key)[0] for key in annotationKeys]
            response = common.create_response(common.OK, keys)
        else:
            try:
                jsonKey = os.path.join(datasetdir,datasetname,jsonPrefix,targetKey + '.json')
                print('GET',myBucket,jsonKey)
                myJson = common.get_s3json(myBucket,jsonKey)
                print(json.dumps(myJson))#,indent=2))
                jpegKey = os.path.join(datasetdir,datasetname,jpegPrefix,targetKey + '.jpg')
                print('GET',myBucket,jpegKey)
                myJpeg = common.get_s3obj(myBucket,jpegKey)
                result = {
                    'image_data': base64.b64encode( myJpeg ).decode("ascii"),
                    'annotation': myJson
                }
                #print('json.dumps(result))',json.dumps(result))
                response = common.create_response(common.OK,result)#json.dumps(result))
            except:
                import traceback
                print('Exception occured.')
                traceback.print_exc()
                response = common.create_response(common.NOT_FOUND)#not found
            
    elif httpMethod == 'POST':
        if targetKey == '':
            response = common.create_response(common.BAD_REQUEST)
        else:
            newKey = os.path.join(datasetdir,datasetname,jsonPrefix,targetKey + '.json')
            newJson = json.loads(event['body'])
            print('POST',myBucket,'/',newKey,'/',newJson)
            common.put_s3json(myBucket,newKey,newJson)
            response = common.create_response(common.CREATED, newJson)
    else:
        response = common.create_response(common.METHOD_NOT_ALLOWED)
    return response
