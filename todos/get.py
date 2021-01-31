import os
import json

from todos import decimalencoder
import boto3
dynamodb = boto3.resource('dynamodb')

client = boto3.client('comprehend')
clientTranslate = boto3.client('translate')

def get(event, context):
    table = dynamodb.Table(os.environ['DYNAMODB_TABLE'])

    # fetch todo from the database
    result = table.get_item(
        Key={
            'id': event['pathParameters']['id']
        }
    )

    # create a response
    response = {
        "statusCode": 200,
        "body": json.dumps(result['Item'],
                           cls=decimalencoder.DecimalEncoder)
    }

    return response

def get_todo(event, context):
    table = dynamodb.Table(os.environ['DYNAMODB_TABLE'])

    # fetch todo from the database
    result = table.get_item(
        Key={
            'id': event['pathParameters']['id']
        }
    )
    try:
       objeto = json.dumps(result['Item'],
                           cls=decimalencoder.DecimalEncoder)
       print('1')     
       language_code = event['pathParameters']['language']
       print('2')     
       translate = client.detect_dominant_language(Text=result['Item']['text'])
       print('3')     
       print(json.dumps(translate))
       language_code_init = translate['Languages'][0]['LanguageCode']
       print('4')     
       print('language_code= ' + language_code)
       print('language_code_init= ' + language_code_init)
       print('5')     
       textTranslate = clientTranslate.translate_text(Text=result['Item']['text'], SourceLanguageCode=language_code_init, TargetLanguageCode=language_code)
       print('6')     
       # create a response
   
       
    except Exception:
            raise

    response = {
          "statusCode": 200,
          "body": ''
    }

    return response
