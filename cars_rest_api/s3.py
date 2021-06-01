import environ
import uuid
import typing as t

import boto3
from requests import Response

env = environ.Env()

ENDPOINT_URL = env("S3_ENDPOINT_URL")
ACCESS_KEY = env("AWS_ACCESS_KEY_ID")
SECRET_KEY = env("AWS_SECRET_ACCESS_KEY")
AWS_REGION = env("AWS_REGION")


class S3:
    connection_options = dict(
        endpoint_url=ENDPOINT_URL,
        aws_access_key_id=ACCESS_KEY,
        aws_secret_access_key=SECRET_KEY,
        region_name=AWS_REGION,
    )

    s3_resource = boto3.resource("s3", **connection_options)
    s3_client = boto3.client("s3", **connection_options)

    @classmethod
    def create_bucket_name(cls, bucket_prefix: str):
        return "".join([bucket_prefix, "-", str(uuid.uuid4())])

    @classmethod
    def create_bucket(
        cls, bucket_prefix: str, s3_connection: t.Union["boto3.botocore.client.S3", "boto3.s3.ServiceResource"]
    ) -> t.Tuple[str, Response]:
        bucket_name: str = cls.create_bucket_name(bucket_prefix)
        bucket_response: Response = s3_connection.create_bucket(
            Bucket=bucket_name, CreateBucketConfiguration={"LocationConstraint": AWS_REGION}
        )

        return bucket_name, bucket_response

    @classmethod
    def get_buckets_name(cls) -> t.List[str]:
        """Get buckets list using client or resource"""
        # buckets = [bucket["Name"] for bucket in cls.s3_client.list_buckets()["Buckets"]]
        buckets = [bucket.name for bucket in cls.s3_resource.buckets.all()]
        return buckets
