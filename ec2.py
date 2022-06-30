from urllib import response
import boto3
from pprint import pprint
aws_con = boto3.session.Session(profile_name='root')

ec2 = aws_con.client(service_name='ec2',region_name='us-east-1')

response = ec2.describe_instances()['Reservations']

for i in response:
    for i in ['Instances']:
        print("My image id is:{}\nInstance id:{}\nThe launch time is:{}".format(i['ImageId'],ii['InstanceId'],i['LaunchTime'].strftime("%Y-%m-%d %H:%M:%S")))

