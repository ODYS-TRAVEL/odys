from django.conf import settings
from .base import AirtableBase

airtable_service = AirtableBase(
    settings.AIRTABLE_API_TOKEN,
    settings.AIRTABLE_BASE_ID
)

__all__ = [
    'airtable_service',
]
