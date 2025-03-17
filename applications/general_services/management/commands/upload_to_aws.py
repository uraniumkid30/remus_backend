import os

from django.conf import settings
from django.core.management.base import BaseCommand

from services.cloud.aws.s3 import S3Resource, AWSCredentials


class Command(BaseCommand):
    help = "Upload db to aws"

    def add_arguments(self, parser):
        parser.add_argument(
            "filename", type=str, help="Indicates the name of the file to upload"
        )

    def handle(self, *args, **kwargs):
        filename = kwargs.get("filename")
        path_to_file = os.path.join(settings.DATABASE_DIR, filename)
        filename = path_to_file.split("/")[-1]
        s3_agent = S3Resource()
        s3_agent.upload_file(path_to_file, f"files/db/{filename}")
        self.stdout.write(self.style.SUCCESS("Upload successful"))
