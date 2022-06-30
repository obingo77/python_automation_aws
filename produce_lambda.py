import json
from urllib import response

import boto3
import botocore
import pandas
import wikipedia
from io import StringIO

#Setup logging
import logging
from pythonjsonlogger import jsonlogger

log = logging.getLogger()
log.setLevel(logging.INFO)
log.setLevel(logging.DEBUG)
logHandler = logging.StreamHandler()
formatter = jsonlogger.JsonFormatter()
logHandler.setFormatter(formatter)
log.addHandler(logHandler)

#S3 bucket

Region = 'us-east-1'

#############################################################################################
#-- SQS Utility Functions --################################################################

def sqs_queque_resource(queue_name):
    log.info("Creating SQS resource")
    sqs = boto3.resource('sqs', region_name=Region)
    queue = sqs.get_queue_by_name(QueueName=queue_name)
    return queue


def sqs_connection():
    
    log.info("Creating SQS connection")
    sqs = boto3.client('sqs', region_name=Region)
    return sqs

def sqs_approximate_number_of_messages(queue_name):
    queue = sqs_queque_resource(queue_name)
    response = queue.attributes
    return response['ApproximateNumberOfMessages']

def delete_sqs_messages(queue_name):
    sqs = sqs_connection()
    queue = sqs_queque_resource(queue_name)
    queue.purge()
    
def delete_sqs_msg(queue_name, receipt_handle):
    sqs_client = sqs_connection()
    try:
        queue_url = sqs_client.get_queue_url(QueueName=queue_name)['QueueUrl']
        delete_sqs_messages = "Deleting message from queue: %s" % queue_url
        log.info(delete_sqs_messages)
        response = sqs_client.delete_message(QueueUrl=queue_url, ReceiptHandle=receipt_handle)
    except botocore.exceptions.ClientError as e:
        log.error(e)
        exception_message = "Error deleting message from queue: %s" % queue_url
        log.exception(exception_message)
        return False   
    
def names_to_wikipedia_urls(names):
    urls = []
    for name in names:
        urls.append(wikipedia.page(name).url)
    return urls

def create_sentiment(row):
    
    log.info("Creating sentiment for row: %s", row)
    comprehend = boto3.client('comprehend')
    payload = comprehend.detect_sentiment(Text=row['text'], LanguageCode='en')
    log.debug("Payload: %s", payload)
    sentiment = payload['Sentiment']
    return sentiment
def apply_sentiment(df, column_name):
    df['sentiment'] = df.apply(create_sentiment, axis=1)
    return df     

#S3
def write_to_s3(bucket_name, file_name, data):
    s3 = boto3.client('s3')
    s3.put_object(Bucket=bucket_name, Key=file_name, Body=data)
    log.info("Wrote data to S3 bucket: %s, file: %s", bucket_name, file_name)
    response = s3.get_object(Bucket=bucket_name, Key=file_name)
    
    
def lambda_handler(event, context):
    #Setup logging
    import logging
    from pythonjsonlogger import jsonlogger
    
    log = logging.getLogger()
    log.setLevel(logging.INFO)
    log.setLevel(logging.DEBUG)
    logHandler = logging.StreamHandler()
    formatter = jsonlogger.JsonFormatter()
    logHandler.setFormatter(formatter)
    log.addHandler(logHandler)
    
    #SQS
    queue_name = 'producer'
    queue = sqs_queque_resource(queue_name)
    queue_url = queue.url
    log.info("Queue URL: %s", queue_url)
    sqs = sqs_connection()
    queue_url = sqs.get_queue_url(QueueName=queue_name)['QueueUrl']
    log.info("Queue URL: %s", queue_url)   