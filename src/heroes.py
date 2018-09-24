# encoding=UTF-8
# this sample is simple REST API of heroes database.
# this use s3 json object as database.

import os
import json
import boto3
import common

s3 = boto3.resource('s3')

myBucket = os.environ.get('BUCKET_NAME','samplebucket-suzuki')
myKey = os.environ.get('HEROES_JSON_KEY','dataset/heroes/Annotations/sample.json')
thisResource = '/heroes'

def handler(event):
    
    httpMethod = event['httpMethod']
    resourcePath = event.get('path','')
    queryStrings = event.get('queryStringParameters',None)
    targetId = event['queryStringParameters'].get('id','') if queryStrings != None else ''
    print('{}:{}/{}'.format(httpMethod,resourcePath,targetId))

    if not resourcePath.startswith(thisResource):
        response = common.create_response(common.BAD_REQUEST)
        return response

    myJson = common.get_s3json(myBucket,myKey)
    myHeroes = myJson['heroes']

    response = ''
    if httpMethod == 'GET':
        if targetId == '':
            response = common.create_response(common.OK, myHeroes)
        else:
            for hero in myHeroes:
                print('check id:',str(hero['id']),targetId)
                if str(hero['id']) == targetId:
                    response = common.create_response(common.OK, hero)
                    break
            if response == '':
                response = common.create_response(common.NOT_FOUND)#not found
            
    elif httpMethod == 'POST':
        newid = 1
        newName = json.loads(event['body'])['name']
        
        for hero in sorted(myHeroes, key=lambda k: k['id']):
            if hero['id'] == newid:
                newid +=1
        newHero = {
            'id'   : newid,
            'name' : newName
        }
        myHeroes.append(newHero)
        print('newHero:{}'.format(newHero))
        myJson['heroes'] = myHeroes
        common.put_s3json(myBucket,myKey,myJson)
        response = common.create_response(common.CREATED, newHero)
        
    elif httpMethod == 'DELETE':
        if targetId == '':
            response = common.create_response(common.BAD_REQUEST)
        else:
            for hero in myHeroes:
                if str(hero['id']) == targetId:
                    myHeroes.remove(hero)
                    myJson['heroes'] = myHeroes
                    common.put_s3json(myBucket,myKey,myJson)
                    response = common.create_response(common.NO_CONTENT)
                    break
            if response == '':
                response = common.create_response(common.NOT_FOUND)#not found
        
    else:
        response = common.create_response(common.METHOD_NOT_ALLOWED)
    return response
