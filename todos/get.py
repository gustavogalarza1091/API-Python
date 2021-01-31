import os
import json

from todos import decimalencoder
import boto3
dynamodb = boto3.resource('dynamodb')

client = boto3.client('comprehend')


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

    # create a response
    response = {
        "statusCode": 200,
        "body": json.dumps(result['Item'],
                           cls=decimalencoder.DecimalEncoder)
    }
    
    language_code = event['pathParameters']['language']
    
    try:
        response = client.detect_syntax(
                Text=response, LanguageCode=language_code)
    except Exception:
            raise

    return response
