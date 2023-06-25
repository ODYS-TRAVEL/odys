import json
from django.conf import settings
from functools import wraps
from requests.exceptions import HTTPError
from rest_framework.response import Response

from .base import AirtableBase

airtable_service = AirtableBase(
    settings.AIRTABLE_API_TOKEN,
    settings.AIRTABLE_BASE_ID
)

def catch_airtable_error(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except HTTPError as e:
            error_message = json.loads(e.response.text)
            status_code = e.response.status_code
            return Response({'message': error_message}, status=status_code)
    return wrapper

__all__ = [
    'catch_airtable_error',
    'airtable_service',
]
