from conf.env_manager import py_env


AWS_ACCESS_KEY_ID = py_env.str("AWS_ACCESS_KEY")
AWS_SECRET_ACCESS_KEY = py_env.str("AWS_SECRET_KEY")
AWS_STORAGE_BUCKET_NAME = py_env.str("AWS_STORAGE_BUCKET_NAME")
AWS_S3_CUSTOM_DOMAIN = f"{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com"
AWS_DEFAULT_ACL = "public-read"
AWS_S3_CUSTOM_DOMAIN = f"{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com"
AWS_S3_OBJECT_PARAMETERS = {"CacheControl": "max-age=86400"}
# static files settings
AWS_LOCATION = "static"
STATIC_URL = f"https://{AWS_S3_CUSTOM_DOMAIN}/{AWS_LOCATION}/"
STATICFILES_LOCATION = "static"
STATICFILES_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"

# public media settings
PUBLIC_MEDIA_LOCATION = "media"
MEDIAFILES_LOCATION = "media"
MEDIA_URL = f"https://{AWS_S3_CUSTOM_DOMAIN}/{PUBLIC_MEDIA_LOCATION}/"
DEFAULT_FILE_STORAGE = "core.storage_backends.PublicMediaStorage"

# pivate media
PRIVATE_MEDIA_LOCATION = "private"
PRIVATE_FILE_STORAGE = "core.storage_backends.PrivateMediaStorage"

STORAGES = {
    "default": {"BACKEND": "conf.storage_backends.MediaStorage"},
    "staticfiles": {"BACKEND": "conf.storage_backends.StaticStorage"},
}
