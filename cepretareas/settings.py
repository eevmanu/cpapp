# coding=utf-8

import os
import dj_database_url

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '=an+fhs+*wvp2+o(q+=8*%$2la81%%-9t=o^)m1p*5ay7v#*i*'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
# TEMPLATE_DEBUG = True

# ------------------------ Heroku Settings ---------------------------

# Honor the 'X-Forwarded-Proto' header for request.is_secure()
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Allow all host headers
ALLOWED_HOSTS = ['*']

# --------------------------------------------------------------------


# Application definition

DJANGO_APPS = (
    'django.contrib.admin',
    'django.contrib.admindocs',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
)

THIRD_PARTY_APPS = (
    'rest_framework',
    # 'south',
    # 'django_extensions',
    'autofixture',
    's3direct',
)

LOCAL_APPS = (
    'accounts',
    'institutions',
    'enrollments',
    'tasks',
    'utils',
    'extras',
)

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'accounts.backends.EmailAuthBackend',
    'accounts.backends.FacebookAuthBackend',
)

ROOT_URLCONF = 'cepretareas.urls'

WSGI_APPLICATION = 'cepretareas.wsgi.application'

PRODUCTION_DB = True
# PRODUCTION_DB = False
if PRODUCTION_DB:
    DATABASES = {
        'default': os.environ.get('PRODUCTION_DB'),
    }
else:
    DATABASES = {
        'default': os.environ.get('DEV_DB'),
    }

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


STATIC_URL = '/static/'

STATIC_ROOT = 'staticfiles'
# STATICFILES_DIRS = (
#     os.path.join(BASE_DIR, 'accounts/static'),
# )


MEDIA_ROOT = os.path.join(BASE_DIR, 'uploads')
MEDIA_URL = '/uploads/'

# ------------ Google Cloud Messaging Settings ---------------

GCM_URL = 'https://android.googleapis.com/gcm/send'

# manuel.solorzanoc@gmail.com
GCM_PROJECT_ID = os.environ.get('GCM_PROJECT_ID')
GCM_API_KEY = os.environ.get('GCM_API_KEY')

GCM_HEADERS = {
    'Content-Type': 'application/json',
    'Authorization': 'key=' + GCM_API_KEY
}

GCM_DATA = {
    'registration_ids': [],
    'data': {},
}

# ------------------------------------------------------------

# -------------- Payments Settings ------------------------

EMAIL_FOR_ENROLLMENTS = 'cepretareas@gmail.com'
BANK_ACCOUNT_FOR_ENROLLMENTS = os.environ.get('BANK_ACCOUNT_FOR_ENROLLMENTS')

# ------------------------------------------------------------

# --------------- AWS Settings -----------------------------

AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = os.environ.get('AWS_STORAGE_BUCKET_NAME')

S3DIRECT_REGION = os.environ.get('S3DIRECT_REGION')


def fn_cpprofile_photo(filename):
    return create_filename(filename, 'cpprofile_photo')


def fn_tasktype_icon(filename):
    return create_filename(filename, 'tasktype_icon')


def fn_tasktopic_icon(filename):
    return create_filename(filename, 'tasktopic_icon')


def fn_precollege_icon(filename):
    return create_filename(filename, 'precollege_icon')


def fn_problems_image(filename):
    return create_filename(filename, 'problems_image')


def create_filename(filename, folder):
    import uuid
    ext = filename.split('.')[-1]
    filename = '%s.%s' % (uuid.uuid4().hex, ext)
    return os.path.join(folder, filename)


S3DIRECT_DESTINATIONS = {
    'cpprofile_photo': (fn_cpprofile_photo, lambda u: u.is_authenticated(), ['image/jpeg', 'image/png']),
    'tasktype_icon': (fn_tasktype_icon, lambda u: u.is_authenticated(), ['image/jpeg', 'image/png']),
    'tasktopic_icon': (fn_tasktopic_icon, lambda u: u.is_authenticated(), ['image/jpeg', 'image/png']),
    'precollege_icon': (fn_precollege_icon, lambda u: u.is_authenticated(), ['image/jpeg', 'image/png']),
    'problems_image': (fn_problems_image, lambda u: u.is_authenticated(), ['application/pdf', 'image/png', 'image/jpeg']),
}

# ------------------------------------------------------------

# ------------ Send Email Settings ------------------------------

EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'cepretareas@gmail.com'
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')
EMAIL_PORT = 587

# Se necesita habilitar el acceso de app inseguras
# https://www.google.com/settings/security/lesssecureapps

# ------------------------------------------------------------

# ------------ Reset Password Settings -----------------------

RESET_PASSWORD_SUBJECT = u"Recuperar Contraseña"
RESET_PASSWORD_URL = u'http://cepretareas.herokuapp.com/accounts/password/reset?token={token}'
RESET_PASSWORD_MSG = u"Estimado {full_name}. \n\n Para recuperar su contraseña acceda al siguiente link:  \n\n {url}"
RESET_PASSWORD_FROM = 'no-reply@cepretareas.com'

# ------------------------------------------------------------

TICKET_NUMBER_LENGTH = 7
