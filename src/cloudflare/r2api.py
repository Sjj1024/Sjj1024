import os
import boto3
from botocore.client import Config


def init_s3(end_point, access_key, secret_key, region_name='auto'):
    return boto3.client(
        's3',
        aws_access_key_id=access_key,
        aws_secret_access_key=secret_key,
        use_ssl=True,
        region_name=region_name,
        endpoint_url=end_point,
        config=Config(s3={"addressing\_style": "path"})
    )


s3_endpoint = "httpsddddddddddd"  # 换成你自己的
s3_access_key = "httpsddddddddddd"  # 换成你自己的
s3_secret_key = "httpsddddddddddd"  # 换成你自己的
region_name = "auto"
s3 = init_s3(s3_endpoint, s3_access_key, s3_secret_key, region_name)

buckets = s3.list_buckets()['Buckets']
print(buckets)
