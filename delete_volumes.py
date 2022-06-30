import boto3
from pprint import pprint
aws_con = boto3.session.Session(profile_name='root')

ec2 = aws_con.client(service_name='ec2',region_name='us-east-1')
ec2_res = aws_con.resource(service_name='ec2',region_name='us-east-1')

# f_ebs_unsused = {"Name": "status", "Values": ["available"]}
# for each_volume in ec2_res.volumes.filter(Filters=[f_ebs_unsused]):
#     print(each_volume.id, each_volume.state,each_volume.tags)
# # each_volume.delete()

# print("All volumes are deleted")

for each_item in ec2_res.volumes.all():
    print(each_item.id, each_item.state,each_item.tags)
    each_item.delete()