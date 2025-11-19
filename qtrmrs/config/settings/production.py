from .base import *
import dj_database_url
import os

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

# Render provides the host in the RENDER_EXTERNAL_HOSTNAME env var
ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', '').split(',')
RENDER_EXTERNAL_HOSTNAME = os.environ.get('RENDER_EXTERNAL_HOSTNAME')
if RENDER_EXTERNAL_HOSTNAME:
    ALLOWED_HOSTS.append(RENDER_EXTERNAL_HOSTNAME)

# --- 1. Database (Render PostgreSQL) ---
DATABASES = {
    'default': dj_database_url.config(
        default=os.environ.get('DATABASE_URL'),
        conn_max_age=600
    )
}

# --- 2. Static Files (WhiteNoise) ---
# Insert WhiteNoise after SecurityMiddleware
try:
    middleware_idx = MIDDLEWARE.index('django.middleware.security.SecurityMiddleware') + 1
    MIDDLEWARE.insert(middleware_idx, 'whitenoise.middleware.WhiteNoiseMiddleware')
except ValueError:
    MIDDLEWARE.insert(0, 'whitenoise.middleware.WhiteNoiseMiddleware')

# --- 3. Storage Configuration (Django 5.0+ Style) ---
STORAGES = {
    # Static files (CSS/JS) -> Served by WhiteNoise
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
    # Media files (Uploads) -> Served by Supabase (via S3)
    "default": {
        "BACKEND": "storages.backends.s3boto3.S3Boto3Storage",
        "OPTIONS": {
            "access_key": os.environ.get("AWS_ACCESS_KEY_ID"),
            "secret_key": os.environ.get("AWS_SECRET_ACCESS_KEY"),
            "bucket_name": os.environ.get("AWS_STORAGE_BUCKET_NAME"),
            "endpoint_url": os.environ.get("AWS_S3_ENDPOINT_URL"),
            "region_name": os.environ.get("AWS_S3_REGION_NAME"),
            "default_acl": "public-read", # Makes uploaded files public by default
            "querystring_auth": False,    # Removes annoying signature params from URLs
            "object_parameters": {
                "CacheControl": "max-age=86400",
            },
        },
    },
}

# Required for django-storages
INSTALLED_APPS += ['storages']