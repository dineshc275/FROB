from django.conf import settings
from storages.backends.s3boto3 import S3Boto3Storage


class StaticStorage(S3Boto3Storage):
    location = settings.STATICFILES_DIRS


class MediaStorage(S3Boto3Storage):
    location = settings.MEDIAFILES_LOCATION


class BookClubMediaStorage(S3Boto3Storage):
    location = settings.AWS_BOOK_CLUB_MEDIA_LOCATION
    file_overwrite = False
    custom_domain = f'{settings.AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com'
    # default_acl = 'public-read'


class EventUserMediaStorage(S3Boto3Storage):
    location = settings.AWS_EVENT_USER_MEDIA_LOCATION
    file_overwrite = False
    custom_domain = f'{settings.AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com'


class EventMediaStorage(S3Boto3Storage):
    location = settings.AWS_EVENT_MEDIA_LOCATION
    file_overwrite = False
    custom_domain = f'{settings.AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com'


class BookClubTalkMediaStorage(S3Boto3Storage):
    location = settings.AWS_BOOK_CLUB_TALK_MEDIA_LOCATION
    file_overwrite = False
    custom_domain = f'{settings.AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com'


class BookMediaStorage(S3Boto3Storage):
    location = settings.AWS_BOOK_MEDIA_LOCATION
    file_overwrite = False
    custom_domain = f'{settings.AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com'


class UserProfileMediaStorage(S3Boto3Storage):
    location = settings.AWS_USER_PROFILE_MEDIA_LOCATION
    file_overwrite = False
    custom_domain = f'{settings.AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com'
    default_acl = 'public'


class BannerMediaStorage(S3Boto3Storage):
    location = settings.AWS_BANNER_MEDIA_LOCATION
    file_overwrite = False
    custom_domain = f'{settings.AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com'

#
# class UserMediaStorage(S3Boto3Storage):
#     location = settings.AWS_UPLOAD_MEDIA_LOCATION
#     file_overwrite = False
#     custom_domain = f'{settings.AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com'