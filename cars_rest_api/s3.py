import environ
import uuid
import typing as t

import boto3
from botocore.config import Config
from requests import Response

env = environ.Env()

ENDPOINT_URL = env("S3_ENDPOINT_URL")
ACCESS_KEY = (env("AWS_ACCESS_KEY_ID"),)
SECRET_KEY = (env("AWS_SECRET_ACCESS_KEY"),)
AWS_REGION = env("AWS_REGION")

s3_config = Config(
    region_name=AWS_REGION,
)

s3_client = boto3.client(
    "s3",
    endpoint_url=ENDPOINT_URL,
    aws_access_key_id=ACCESS_KEY,
    aws_secret_access_key=SECRET_KEY,
    region_name=AWS_REGION,
    config=s3_config,
)

s3_resource = boto3.resource(
    "s3",
    endpoint_url=ENDPOINT_URL,
    aws_access_key_id=ACCESS_KEY,
    aws_secret_access_key=SECRET_KEY,
    region_name=AWS_REGION,
    config=s3_config,
)


def create_bucket_name(bucket_prefix: str):
    return "".join([bucket_prefix, "-", str(uuid.uuid4())])


def create_bucket(
    bucket_prefix: str, s3_connection: t.Union["boto3.botocore.client.S3", "boto3.s3.ServiceResource"]
) -> t.Tuple[str, Response]:
    bucket_name: str = create_bucket_name(bucket_prefix)
    bucket_response: Response = s3_connection.create_bucket(
        bucket_name, CreateBucketConfiguration={"LocationConstraint": AWS_REGION}
    )

    return bucket_name, bucket_response


if __name__ == "__main__":
    # print(s3)
    # for bucket in s3_client.buckets.all():
    #     print(bucket.name)
    print(create_bucket_name("test"))
