from multiprocessing.connection import wait
import boto3
from pprint import pprint
aws_con = boto3.session.Session(profile_name='root')

ec2 = aws_con.client(service_name='ec2',region_name='us-east-1')
ec2_res = aws_con.resource(service_name='ec2',region_name='us-east-1')

