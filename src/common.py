import json
import boto3

s3 = boto3.resource('s3')
client = boto3.client('s3')

#############
# STATUR CODE
OK                  = 200
CREATED             = 201 #success create
NO_CONTENT          = 204 #success delete
BAD_REQUEST         = 400
NOT_FOUND           = 404
METHOD_NOT_ALLOWED  = 405
def create_response(code, body=None):
    return {
        'statusCode' : code,
        'isBase64Encoded': False,
        'headers' : {
            "x-custom-header" : "custom header",
            "Access-Control-Allow-Origin" : "*"
        },
        'body':json.dumps(body) if body != None else ''
    }
    
#############
# S3 Accessor
def download_s3file(bucket,key,localpath):
    s3.Bucket(bucket).download_file(key,localpath)
    return localpath
    
def get_s3text(bucket,key):
    obj = s3.Object(bucket, key)
    response = obj.get()
    body = response['Body'].read()
    return body.decode('utf-8')

def get_s3json(bucket,key):
    obj = s3.Object(bucket, key)
    response = obj.get()
    body = response['Body'].read()
    return json.loads(body.decode('utf-8'))

def get_s3obj(bucket,key):
    print('get_s3obj',bucket, key)
    obj = s3.Object(bucket, key)
    print('obj',obj)
    response = obj.get()
    print('response',response)
    body = response['Body'].read()
    #print('body',body)
    return body


def put_s3json(bucket,key,jsondata):
    obj = s3.Object(bucket, key)
    body = json.dumps(jsondata,ensure_ascii=False, indent=4)
    response = obj.put(
        Body=body.encode('utf-8'),
        ContentEncoding='utf-8',
        ContentType='application/json' #'text/plane'
    )
    return response

def put_s3obj(bucket,key,data):
    obj = s3.Object(bucket, key)
    response = obj.put(
        Body=data,
        ContentType='binary/octet-stream'
    )
    return response
    
    

def get_s3list(bucket,prefix,postfix=''):
    keylist=[]
    response = client.list_objects(
        Bucket=bucket,
        Prefix=prefix
        )
    contents = response['Contents']
    for content in contents:
        if content['Key'] == prefix:
            continue
        if not content['Key'].endswith(postfix):
            continue
        keylist.append(content['Key'].replace(prefix,''))
    return keylist

