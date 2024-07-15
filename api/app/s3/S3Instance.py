from __future__ import annotations

import logging
import os
from dataclasses import dataclass

import boto3

logger = logging.getLogger("django.request")


@dataclass
class S3Instance:
    """
    Initializes a new instance of the S3Instance class.
    This constructor sets the AWS access key ID, secret access key, region name, and S3 bucket name
    by retrieving the corresponding environment variables.

    Parameters:
        None
    Returns:
        None
    """

    def __init__(self):
        """
        Initializes a new instance of the S3Instance class.
        This constructor sets the AWS access key ID, secret access key, region name, and S3 bucket name
        by retrieving the corresponding environment variables.

        Parameters:
            None
        Returns:
            None
        """
        self.aws_access_key_id = os.getenv("AWS_S3_ACCESS_KEY_ID")
        self.aws_secret_access_key = os.getenv("AWS_S3_SECRET_ACCESS_KEY")
        self.aws_region_name = os.getenv("AWS_S3_REGION_NAME")
        self.aws_s3_bucket_name = os.getenv("AWS_S3_BUCKET_NAME")

    def get_s3_instance(self):
        """
        Returns a boto3 S3 client instance using the provided AWS credentials and region.

        :return: A boto3 S3 client instance.
        :rtype: boto3.client
        """
        return boto3.client(
            "s3",
            aws_access_key_id=self.aws_access_key_id,
            aws_secret_access_key=self.aws_secret_access_key,
            region_name=self.aws_region_name,
        )
