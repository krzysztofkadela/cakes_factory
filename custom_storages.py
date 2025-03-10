from django.conf import settings
from storages.backends.s3boto3 import S3Boto3Storage


class StaticStorage(S3Boto3Storage):
    location = settings.STATICFILES_LOCATION
    default_acl = "public-read"  # Ensures static files are publicly accessible
    querystring_auth = False  # Removes authentication query parameters from URLs


class MediaStorage(S3Boto3Storage):
    location = settings.MEDIAFILES_LOCATION
    file_overwrite = False  # Prevents media files from being overwritten