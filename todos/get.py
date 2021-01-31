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
       language_code = event['pathParameters']['language']
       translate = client.detect_dominant_language(Text=result['Item']['text'])
       language_father = translate['Languages'][0]
       language_code_init = language_father['LanguageCode']
       textTranslate = clientTranslate.translate_text(Text=result['Item']['text'], SourceLanguageCode=language_code_init, TargetLanguageCode=language_code)
       result['Item']['text'] = textTranslate['TranslatedText']
    except Exception:
            raise

    response = {
          "statusCode": 200,
          "body": json.dumps(result['Item'],
                           cls=decimalencoder.DecimalEncoder)
    }

    return response
