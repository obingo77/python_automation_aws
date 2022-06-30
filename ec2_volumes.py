from urllib import response
import boto3
from pprint import pprint
aws_con = boto3.session.Session(profile_name='root')

ec2 = aws_con.client(service_name='ec2',region_name='us-east-1')

response = ec2.describe_volumes()['Volumes']
for i in response:
    print("Volume id:{}\nVolume size:{}\nVolume type:{}\nVolume state:{}".format(i['VolumeId'],i['Size'],i['VolumeType'],i['State']))


