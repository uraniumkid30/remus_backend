from storages.backends.s3boto3 import S3Boto3Storage


class PublicMediaStorage(S3Boto3Storage):
    location = "media"
    file_overwrite = False
    default_acl = "public-read"


class PrivateMediaStorage(S3Boto3Storage):
    location = "private"
    default_acl = "private"
    file_overwrite = False
    custom_domain = False


class MediaStorage(S3Boto3Storage):
    location = "media"
    file_overwrite = False


class MediaAttachmentStorage(S3Boto3Storage):
    location = "media"
    file_overwrite = False

    def get_object_parameters(self, name):
        return {"ContentDisposition": "attachment"}


class StaticStorage(S3Boto3Storage):
    location = "static"
    querystring_auth = False
    file_overwrite = False
