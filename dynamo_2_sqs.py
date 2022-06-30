from cmath import log
from distutils.log import Log
import json
from logging import Formatter
from urllib import response
import boto3

def lambda_handler(event, context):
    
    DYNAMODB = boto3.resource('dynamodb')
    TABLE = "testtable"
    QUEUE = "producer"
    SQS = boto3.client('sqs')
    
    #SETUP LOGGING
    import logging
    from pythonjsonlogger import jsonlogger
        
    log = logging.getLogger()
    log.setLevel(logging.INFO)
    logHandler = logging.StreamHandler()
    Formatter = jsonlogger.JsonFormatter()
    log.addHandler(logHandler)
    log.info = logHandler.emit

def scan_table(table):
    log.info("Scanning table: %s", table)
    producer_table = DYNAMODB.Table(table)
    response = producer_table.scan()
    items = response['Items']
    log.info("Found %s items", len(items))
    return items
    
def send_to_queue(queue, message):
    queue_url = SQS.get_queue_url(QueueName=queue)['QueueUrl']
    queue_send_log_msg = "Sending message to queue: %s" % queue_url
    json_message = json.dumps(message)
    log.info("Sending message to queue: %s", queue)
    response = SQS.send_message(QueueUrl=queue_url, MessageBody=json_message)
    log.info("Message sent")
    return response
    
def send_emissions(table, queue_name):
    items = scan_table(table)
    for item in items:
        log.info("Sending item: %s, %s", item['id'], item['name'])
        response = send_to_queue(queue_name, item)
        log.debug("Response: %s", response)
            
            
def lambda_handler(event, context):
    send_emissions("testtable", "producer")
    return "Done"
    log.info("Done")

    

