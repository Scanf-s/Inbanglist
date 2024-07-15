import os

import boto3
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Set the default profile image in S3 bucket to be publicly readable"

    def handle(self, *args, **kwargs):
        bucket_name = "live-streaming-list-profile"
        object_key = "profile_images/default_profile.png"
        public_url = f"https://{bucket_name}.s3.amazonaws.com/{object_key}"
        self.stdout.write(self.style.SUCCESS(f"Public URL: {public_url}"))
