from .common import *

import os
import dj_database_url


AIRTABLE_API_TOKEN = os.environ.get('AIRTABLE_API_TOKEN')
AIRTABLE_BASE_ID = os.environ.get('AIRTABLE_BASE_ID')

DATABASES['default'] = dj_database_url.config(conn_max_age=600, ssl_require=True)

STATIC_ROOT = BASE_DIR / "staticfiles"
