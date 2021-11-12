import boto3
import time
import urllib.parse
from botocore.vendored import requests
import json

domain_endpoint = 'https://search-photos-v42yewxkxht7djeodjqsksdp2m.us-east-1.es.amazonaws.com'
index = 'photos'
type = 'photo'
es_req_url = '/'.join([domain_endpoint, index, type]) + "/"
headers = {
    "Content-Type": "application/json"
    }

def get_labels_from_response(response):
    print("Labels are: ")
    labels = list()
    for label in response['Labels']:
        labels.append(label['Name'])
        print(label['Name'])
    
    return labels

def extract_labels(photo_name, bucket_name):
    client = boto3.client('rekognition', 'us-east-1')
    s3_object_dict = {
        'S3Object': {
            'Bucket': bucket_name,
            'Name': photo_name
        }
    }
    response = client.detect_labels(Image = s3_object_dict, MaxLabels = 12)
    labels = get_labels_from_response(response)

    #Getting custom labels
    s3client = boto3.client('s3')
    metadata = s3client.head_object(Bucket='storephotos3', Key=photo_name)
    
    try:
        customlabels = metadata['ResponseMetadata']['HTTPHeaders']['x-amz-meta-customlabels'].split(',')
        labels.append(customlabels)
    except:
        print("No custom labels")
    
    return labels

def send_es_post_request(photo_name, bucket_name, labels):
    es_post_request_data = {
        'objectKey': photo_name,
        'bucket': bucket_name,
        'createdAtTimestamp': time.time(),
        'labels': labels
    }
    es_post_request_result = requests.post(es_req_url + photo_name, 
                                            data = json.dumps(es_post_request_data).encode('utf-8'), 
                                            headers = headers,
                                            auth = ('Gursifath', 'CCBDCol123!'))
    
    return es_post_request_result.status_code == 200

def lambda_handler(event, context):
    s3_records_data = event['Records'][0]['s3']
    bucket_name = s3_records_data['bucket']['name']
    bucket_key = urllib.parse.unquote_plus(s3_records_data['object']['key'], encoding = 'utf-8')
    
    print("About bucket: " + bucket_key + " : " + bucket_name)

    labels = extract_labels(bucket_key, bucket_name)

    is_es_post_request_success = send_es_post_request(bucket_key, bucket_name, labels)
    if not(is_es_post_request_success):
        return
        {
            'statusCode': 400,
            'body': json.dumps('Lambda does not run successfully!')
        }
    
    return
    {
        'statusCode': 200,
        'body': json.dumps('Lambda Run Successfully!')
    }