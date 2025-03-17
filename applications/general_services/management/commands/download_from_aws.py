import os
from django.conf import settings
from django.core.management.base import BaseCommand

from services.cloud.aws.s3 import S3Resource


class Command(BaseCommand):
    help = "download db from aws"

    def add_arguments(self, parser):
        parser.add_argument(
            "filename", type=str, help="Indicates the name of the file to download"
        )

    def handle(self, *args, **kwargs):
        filename = kwargs.get("filename")
        path_to_file = os.path.join(settings.DATABASE_DIR, filename)
        s3_agent = S3Resource()
        s3_agent.download_file(path_to_file, f"files/db/{filename}")
        self.stdout.write(self.style.SUCCESS("Download successful"))
