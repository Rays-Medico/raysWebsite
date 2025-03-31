"""
Django settings for website project.
"""

from pathlib import Path
import os
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
SECRET_KEY = 'django-insecure-nv)h0xqkqo+-*+fs=9v1w-6xqt(eud#txg$q3+zf)v49w=v+&2'
DEBUG = True
ALLOWED_HOSTS = []

# Auth User Model
AUTH_USER_MODEL='User.User'

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'games',
    'mlModels',
    'User',
    'storages',
    'healtVault.apps.HealtvaultConfig',
    'timetable',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'website.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'website.wsgi.application'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        '': {
            'handlers': ['console'],
            'level': 'INFO',
        },
    },
}

# Azure Storage Configuration
# IMPORTANT: Setting this first before any Azure operations
AZURE_ACCOUNT_NAME = 'rayshealthvault'
AZURE_ACCOUNT_KEY = 'ZcRa5B1fq63jYuJS8OI4wyhBNpEgLhvZSHrwZIKFsOCNZbbSdPfBchwqM9FllY9F+jCyzu5zHmxY+ASt02x4xw=='
AZURE_CONTAINER = 'medicaldocuments' 
AZURE_CUSTOM_DOMAIN = f'{AZURE_ACCOUNT_NAME}.blob.core.windows.net'

# Set the default storage to Azure BEFORE any operations
DEFAULT_FILE_STORAGE = 'storages.backends.azure_storage.AzureStorage'

# Media settings for Azure
MEDIA_URL = f"https://{AZURE_ACCOUNT_NAME}.blob.core.windows.net/{AZURE_CONTAINER}/"
MEDIA_ROOT = ""

# Database settings
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Static files
STATIC_URL = 'static/'
STATICFILES_DIRS=[os.path.join(BASE_DIR,'static')]

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

LOGIN_URL = 'login'

# Log that settings were loaded correctly
print(f"Settings loaded. DEFAULT_FILE_STORAGE: {DEFAULT_FILE_STORAGE}")

# If you want to test Azure connectivity, do it here AFTER all settings are configured
# But I recommend moving this to a management command instead of your settings file

# Email settings for Gmail
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'ayushbhosale70@gmail.com'
EMAIL_HOST_PASSWORD = 'gxbcgepiykhisevj'  
DEFAULT_FROM_EMAIL = 'ayushbhosale70@gmail.com'
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

"""
def test_azure_connection():
    try:
        from azure.storage.blob import BlobServiceClient
        connection_string = f"DefaultEndpointsProtocol=https;AccountName={AZURE_ACCOUNT_NAME};AccountKey={AZURE_ACCOUNT_KEY};EndpointSuffix=core.windows.net"
        blob_service_client = BlobServiceClient.from_connection_string(connection_string)
        container_client = blob_service_client.get_container_client(AZURE_CONTAINER)
        container_client.upload_blob("settings_test.txt", b"Settings test upload!", overwrite=True)
        print("Azure connection test successful!")
    except Exception as e:
        print(f"Azure connection test failed: {str(e)}")

# Uncomment only if you need to test during startup
# test_azure_connection()
"""