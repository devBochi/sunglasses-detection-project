# Nahuel Montes de Oca

import json
import boto3
import urllib.parse
        
reko_client = boto3.client('rekognition', region_name = 'us-east-2')
s3_client = boto3.client('s3')

def lambda_handler(event, context):

    # Get the object from the event
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = urllib.parse.unquote_plus(event['Records'][0]['s3']['object']['key'], encoding='utf-8')
    try:
        # Rekognition
        face_response = reko_client.detect_faces(
            Image={'S3Object':{'Bucket':'sd-reko-dumps','Name':key}},
            Attributes = [ "ALL" ]
        )
        
        sunglasses = face_response["FaceDetails"][0]["Eyeglasses"]["Value"]
        eyeglasses = face_response["FaceDetails"][0]["Sunglasses"]["Value"]

        sunResponse = ("negative","positive","positive")[sunglasses + eyeglasses]
        print("The photo: {} is {} for sunglasses/eyeglasses".format(key,sunResponse))
    
        response = "The photo: {} is {} for sunglasses/eyeglasses".format(key,sunResponse)
        
        if (sunResponse == "positive"):
            #specify destination bucket
            destination_bucket_name='sd-reko-sunglasses'
            #specify from where file needs to be copied
            copy_object={'Bucket':bucket,'Key':key}
            #write copy statement 
            s3_client.copy_object(CopySource=copy_object,Bucket=destination_bucket_name,Key=key)
            print("Copied!")
            response = "The photo: {} is {} for sunglasses/eyeglasses. The file has been successfully copied to 'nmdo-positive-sunglasses' bucket".format(key,sunResponse)

        return {
            'statusCode': 3000,
            'body': json.dumps(response)
        }
    except Exception as e:
        print(e)
        print('Error getting object from bucket. Make sure they exist and your bucket is in the same region as this function.')
        raise e
