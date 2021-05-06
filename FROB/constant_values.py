from django.db.models import Q
from pathlib import Path

otp_validity_minutes = 10
otp_attempts = 10

api_versions = "v1"

default_query_1 = Q(is_deleted=False) & Q(is_active=True)

source_list = ["webapp", "postman", "ios", "android"]

project_path = Path(__file__).resolve().parent.parent
