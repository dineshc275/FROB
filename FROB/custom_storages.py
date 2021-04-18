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


class UserProfileMediaStorage(S3Boto3Storage):
    location = settings.AWS_USER_PROFILE_MEDIA_LOCATION
    file_overwrite = False
    custom_domain = f'{settings.AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com'
    default_acl = 'public'

# class ProductMediaStorage(S3Boto3Storage):
#     location = settings.AWS_PRODUCT_MEDIA_LOCATION
#     file_overwrite = False
#     custom_domain = f'{settings.AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com'
#
#
# class CategoryMediaStorage(S3Boto3Storage):
#     location = settings.AWS_CATEGORY_MEDIA_LOCATION
#     file_overwrite = False
#     custom_domain = f'{settings.AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com'
#
#
# class StoreMediaStorage(S3Boto3Storage):
#     location = settings.AWS_STORE_MEDIA_LOCATION
#     file_overwrite = False
#     custom_domain = f'{settings.AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com'
#
#
# class OfferMediaStorage(S3Boto3Storage):
#     location = settings.AWS_STORE_MEDIA_LOCATION
#     file_overwrite = False
#     custom_domain = f'{settings.AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com'
#
#
# class UserMediaStorage(S3Boto3Storage):
#     location = settings.AWS_UPLOAD_MEDIA_LOCATION
#     file_overwrite = False
#     custom_domain = f'{settings.AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com'