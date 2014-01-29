"""
Django settings for tourngen project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

#from django import template
 
#django-staticfiles DRY principle
#template.add_to_builtins('django.contrib.staticfiles.templatetags.staticfiles')

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '5x#$=p5$qj#=mq_4a^%evnfmbo2poq)8@@y%%6+wi0d%(a(co)'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'tournament_creator',
    'registration',
    'guardian',
)

ACCOUNT_ACTIVATION_DAYS = 3

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'tourngen.urls'

WSGI_APPLICATION = 'tourngen.wsgi.application'


AUTHENTICATION_BACKENDS = [
            'django.contrib.auth.backends.ModelBackend', # Django's default authbackend
            'rulez.backends.ObjectPermissionBackend',
            'object_permissions.backend.ObjectPermBackend',
            'guardian.backends.ObjectPermissionBackend',
        ]

ANONYMOUS_USER_ID = -1

# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'tourngen',
	'USER': 'root',
	'PASSWORD': 'PokemonDigimon',
	'HOST':'127.0.0.1',
	'PORT': '3306', 
    }
}


from django.core.urlresolvers import reverse_lazy

LOGIN_URL = reverse_lazy('login')
LOGIN_REDIRECT_URL = reverse_lazy('login')
LOGOUT_URL = reverse_lazy('logout')

USER_ROLES = (
	'tourncreator',
	'scorefiller',
	'readonly',
)

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'America/Guayaquil'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_ROOT = ''

STATIC_URL = '/static/'


STATICFILES_DIRS = (
    (  'assets', '/home/calimat/Django/Project/tourngen/tourngen/static'),
)
