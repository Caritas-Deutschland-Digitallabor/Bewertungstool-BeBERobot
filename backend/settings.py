from pathlib import Path
import os
import dj_database_url
from django_storage_url import dsn_configured_storage_class
# from django.utils.translation import gettext

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
#LOGIN_REDIRECT_URL = 'setting/'

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY', '<a string of random characters>')

# SECURITY WARNING: don't run with debug turned on in production!
#DEBUG = os.environ.get('DEBUG') == "False"
DEBUG="True"
ALLOWED_HOSTS = ["*",]

#ALLOWED_HOSTS = [os.environ.get('DOMAIN'),]
#This is very risky. Running under your own risk
#if DEBUG:
ALLOWED_HOSTS = ["*"]

# Redirect to HTTPS by default, unless explicitly disabled
# SECURE_SSL_REDIRECT = os.environ.get('SECURE_SSL_REDIRECT') != "False"
# For debugging
SECURE_SSL_REDIRECT = "False" != "False"

X_FRAME_OPTIONS = 'SAMEORIGIN'

# Email configuration
# EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend' # comment when we have it on the server and we are using a real email
EMAIL_USE_TLS = True
EMAIL_HOST = 'your email host'
EMAIL_HOST_USER = 'your host user'
EMAIL_HOST_PASSWORD = 'your password!' # Stablish the app password we have to generate on the email account
EMAIL_PORT = 587
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
SERVER_EMAIL = EMAIL_HOST_USER

# Application definition
INSTALLED_APPS = [
    'backend',

    # optional, but used in most projects
    'djangocms_admin_style',

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'whitenoise.runserver_nostatic',  # http://whitenoise.evans.io/en/stable/django.html#using-whitenoise-in-development
    'django.contrib.staticfiles',
    'django.contrib.sites',

    # key django CMS modules
    'cms',
    'menus',
    'treebeard',
    'sekizai',

    # Django Filer - optional, but used in most projects
    'filer',
    'easy_thumbnails',

    # the default CKEditor - optional, but used in most projects
    'djangocms_text_ckeditor',

    # some content plugins - optional, but used in most projects
    'djangocms_file',
    'djangocms_icon',
    'djangocms_link',
    'djangocms_picture',
    'djangocms_style',
    'djangocms_googlemap',
    'djangocms_video',

    # optional django CMS Bootstrap 4 modules
    'djangocms_bootstrap4',
    'djangocms_bootstrap4.contrib.bootstrap4_alerts',
    'djangocms_bootstrap4.contrib.bootstrap4_badge',
    'djangocms_bootstrap4.contrib.bootstrap4_card',
    'djangocms_bootstrap4.contrib.bootstrap4_carousel',
    'djangocms_bootstrap4.contrib.bootstrap4_collapse',
    'djangocms_bootstrap4.contrib.bootstrap4_content',
    'djangocms_bootstrap4.contrib.bootstrap4_grid',
    'djangocms_bootstrap4.contrib.bootstrap4_jumbotron',
    'djangocms_bootstrap4.contrib.bootstrap4_link',
    'djangocms_bootstrap4.contrib.bootstrap4_listgroup',
    'djangocms_bootstrap4.contrib.bootstrap4_media',
    'djangocms_bootstrap4.contrib.bootstrap4_picture',
    'djangocms_bootstrap4.contrib.bootstrap4_tabs',
    'djangocms_bootstrap4.contrib.bootstrap4_utilities',

    # django crispy forms
    'crispy_forms',

    # django-dbbackup
    'dbbackup',

    # # polls application
    'polls_cms_integration',
    'polls'
]

DBBACKUP_STORAGE = 'django.core.files.storage.FileSystemStorage'
DBBACKUP_STORAGE_OPTIONS = {'location': '/app/backup'}

CRISPY_TEMPLATE_PACK = 'uni_form'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.locale.LocaleMiddleware',

    'cms.middleware.user.CurrentUserMiddleware',
    'cms.middleware.page.CurrentPageMiddleware',
    'cms.middleware.toolbar.ToolbarMiddleware',
    'cms.middleware.language.LanguageCookieMiddleware',
]

ROOT_URLCONF = 'backend.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.media',
                'django.template.context_processors.csrf',
                'django.template.context_processors.tz',
                'django.template.context_processors.i18n',

                'cms.context_processors.cms_settings',
                'sekizai.context_processors.sekizai',

            ],
        },
    },
]

CMS_TEMPLATES = [
    # a minimal template to get started with
    ('minimal.html', 'Minimal template'),
    ('whitenoise-static-files-demo.html', 'Static File Demo'),

    # optional templates that extend base.html, to be used with Bootstrap 5
    ('page.html', 'Bootstrap 4 Demo'),
    ('feature.html', 'Bootstrap 4 Demo with two placeholders')
]

WSGI_APPLICATION = 'backend.wsgi.application'


# #
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

# Configure database using DATABASE_URL; fall back to sqlite in memory when no
# environment variable is available, e.g. during Docker build
DATABASE_URL = os.environ.get('DATABASE_URL', 'sqlite:////app/db.sqlite')
DATABASES = {'default': dj_database_url.parse(DATABASE_URL)}


# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

# if not DEBUG:
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
     'NAME': 'polls_cms_integration.validators.NumberValidator',
         'OPTIONS': {
             'min_digits': 3, }},
 {
     'NAME': 'polls_cms_integration.validators.UppercaseValidator', 
 },
 {
     'NAME': 'polls_cms_integration.validators.LowercaseValidator',
 },
 {
     'NAME': 'polls_cms_integration.validators.SymbolValidator',
 },
 # {
 #     'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
 # },
]

# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'de'

LANGUAGES = [
   # ('en', 'English'),
    ('de', 'German'),
]

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles_collected')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Media files
# DEFAULT_FILE_STORAGE is configured using DEFAULT_STORAGE_DSN

# read the setting value from the environment variable
DEFAULT_STORAGE_DSN = os.environ.get('DEFAULT_STORAGE_DSN')

# dsn_configured_storage_class() requires the name of the setting
DefaultStorageClass = dsn_configured_storage_class('DEFAULT_STORAGE_DSN')

# Django's DEFAULT_FILE_STORAGE requires the class name
DEFAULT_FILE_STORAGE = 'backend.settings.DefaultStorageClass'

# only required for local file storage and serving, in development
MEDIA_URL = 'media/'
MEDIA_ROOT = os.path.join('/data/media/')

DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'

SITE_ID = 1
