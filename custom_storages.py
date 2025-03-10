from django.conf import settings
from storages.backends.s3boto3 import S3Boto3Storage


class StaticStorage(S3Boto3Storage):
    location = settings.STATICFILES_LOCATION
    default_acl = None  # ✅ Remove ACLs
    querystring_auth = False  # Prevents authentication query parameters


class MediaStorage(S3Boto3Storage):
    location = settings.MEDIAFILES_LOCATION
    default_acl = None  # ✅ Remove ACLs
    file_overwrite = False  # Prevents overwriting media files