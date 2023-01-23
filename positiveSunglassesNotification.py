# Nahuel Montes de Oca

import json
import urllib.parse
import boto3

print('Loading function')

sns_client = boto3.client('sns')
snsArn = '---------------'

def lambda_handler(event, context):
    # Get the object from the event and show its content type
    bucket = event['Records'][0]['s3']['bucket']['name']
    file_name = urllib.parse.unquote_plus(event['Records'][0]['s3']['object']['key'], encoding='utf-8')
    try:
        response = "The photo {} is positive for sunglasses! You can check it in your s3 bucket.".format(file_name)
        return sns_client.publish(
                TopicArn = snsArn,
                Message = response ,
                Subject='Rekogntion Project'
            )
    except Exception as e:
        print(e)
        print('Error getting object {} from bucket {}. Make sure they exist and your bucket is in the same region as this function.'.format(file_name, bucket))
        raise e
