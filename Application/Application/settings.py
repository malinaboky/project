"""
Django settings for Application project.

Generated by 'django-admin startproject' using Django 3.2.8.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""
import os.path
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-egat(ow&9$1xuj#^+&v^!)odb$zdw=&meno=!xa^z4+md&auyr'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['127.0.0.1:8000', 'malinaboky.beget.tech', '127.0.0.1']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'junior_group.apps.JuniorGroupConfig',
    'preparatory_group.apps.PreparatoryGroupConfig',
    'middle_group.apps.MiddleGroupConfig',
    'senior_group.apps.SeniorGroupConfig',
    'collection.apps.CollectionConfig',
    'users.apps.UsersConfig',
    'debug_toolbar',
    'rest_framework',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'admin_reorder.middleware.ModelAdminReorder',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
]

ROOT_URLCONF = 'Application.urls'

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
            ],
        },
    },
]

WSGI_APPLICATION = 'Application.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }

    # 'default': {
    #     'ENGINE': 'django.db.backends.mysql',
    #     'NAME': 'malinaboky_data',
    #     'USER': 'malinaboky_data',
    #     'PASSWORD': 'VopZ%9Lu',
    #     'HOST': 'localhost',
    #     'PORT': '3306',
    # }
}

# VopZ%9Lu - mysqlpassword
# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'ru'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = '/static/'

STATIC_ROOT = os.path.join(BASE_DIR, "static")

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

ADMIN_REORDER = (
    {'app': 'junior_group', 'label': 'Младшая группа',
     'models': ('junior_group.Child', 'junior_group.CognitiveDevelop', 'junior_group.Math', 'junior_group.ViewOfWorld',
                'junior_group.PrimaryRepresent', 'junior_group.UniversalPrerequisite', 'junior_group.Cognition',
                'junior_group.Skills', 'junior_group.Activities', 'junior_group.SpeechDevelop', 'junior_group.SpeechActivity',
                'junior_group.Reading', 'junior_group.Communication', 'junior_group.CommunicativeDevelop', 'junior_group.Emotional',
                'junior_group.Work', 'junior_group.Safety', 'junior_group.MasteringCommunicat', 'junior_group.BehaviorManagement',
                'junior_group.ProblemSolving', 'junior_group.Socialization','junior_group.PhysicalDevelop', 'junior_group.Movements',
                'junior_group.Hygiene', 'junior_group.Health', 'junior_group.ArtisticDevelop', 'junior_group.ArtisticPersonalDevelop',
                 'junior_group.Painting', 'junior_group.Modeling', 'junior_group.Application', 'junior_group.Music',
                'junior_group.AttentionAndMemory', 'junior_group.Perception', 'junior_group.ThinkingAndSpeaking',
                'junior_group.EmotionsAndWill', 'junior_group.MotorDevelop', 'junior_group.VisualPerception', 'junior_group.SBO',
                 'junior_group.Orientation', 'junior_group.Touch',)},

    {'app': 'middle_group', 'label': 'Средняя группа',
     'models': ('middle_group.Child', 'middle_group.CognitiveDevelop', 'middle_group.Math', 'middle_group.ViewOfWorld',
                'middle_group.PrimaryRepresent', 'middle_group.UniversalPrerequisite', 'middle_group.Cognition',
                'middle_group.Skills', 'middle_group.Activities', 'middle_group.SpeechDevelop',
                'middle_group.SpeechActivity',
                'middle_group.Reading', 'middle_group.Communication', 'middle_group.CommunicativeDevelop',
                'middle_group.Emotional',
                'middle_group.Work', 'middle_group.Safety', 'middle_group.MasteringCommunicat',
                'middle_group.BehaviorManagement',
                'middle_group.ProblemSolving', 'middle_group.Socialization', 'middle_group.PhysicalDevelop',
                'middle_group.Movements',
                'middle_group.Hygiene', 'middle_group.Health', 'middle_group.ArtisticDevelop',
                'middle_group.ArtisticPersonalDevelop',
                'middle_group.Painting', 'middle_group.Modeling', 'middle_group.Application', 'middle_group.Music',
                'middle_group.AttentionAndMemory', 'middle_group.Perception', 'middle_group.ThinkingAndSpeaking',
                'middle_group.EmotionsAndWill', 'middle_group.MotorDevelop', 'middle_group.VisualPerception',
                'middle_group.SBO',
                'middle_group.Orientation', 'middle_group.Touch',)},

    {'app': 'senior_group', 'label': 'Старшая группа',
     'models': ('senior_group.Child', 'senior_group.CognitiveDevelop', 'senior_group.Math', 'senior_group.ViewOfWorld',
                'senior_group.PrimaryRepresent', 'senior_group.UniversalPrerequisite', 'senior_group.Cognition',
                'senior_group.Skills', 'senior_group.Activities', 'senior_group.SpeechDevelop',
                'senior_group.SpeechActivity',
                'senior_group.Reading', 'senior_group.Communication', 'senior_group.CommunicativeDevelop',
                'senior_group.Emotional',
                'senior_group.Work', 'senior_group.Safety', 'senior_group.MasteringCommunicat',
                'senior_group.BehaviorManagement',
                'senior_group.ProblemSolving', 'senior_group.Socialization', 'senior_group.PhysicalDevelop',
                'senior_group.Movements',
                'senior_group.Hygiene', 'senior_group.Health', 'senior_group.ArtisticDevelop',
                'senior_group.ArtisticPersonalDevelop',
                'senior_group.Painting', 'senior_group.Modeling', 'senior_group.Application', 'senior_group.Music',
                'senior_group.AttentionAndMemory', 'senior_group.Perception', 'senior_group.ThinkingAndSpeaking',
                'senior_group.EmotionsAndWill', 'senior_group.MotorDevelop', 'senior_group.VisualPerception',
                'senior_group.SBO',
                'senior_group.Orientation', 'senior_group.Touch',)},
     {'app': 'preparatory_group', 'label': 'Подготовительная группа',
     'models': ('preparatory_group.Child', 'preparatory_group.CognitiveDevelop', 'preparatory_group.Math', 'preparatory_group.ViewOfWorld',
                'preparatory_group.PrimaryRepresent', 'preparatory_group.UniversalPrerequisite', 'preparatory_group.Cognition',
                'preparatory_group.Skills', 'preparatory_group.Activities', 'preparatory_group.SpeechDevelop',
                'preparatory_group.SpeechActivity',
                'preparatory_group.Reading', 'preparatory_group.Communication', 'preparatory_group.CommunicativeDevelop',
                'preparatory_group.Emotional',
                'preparatory_group.Work', 'preparatory_group.Safety', 'preparatory_group.MasteringCommunicat',
                'preparatory_group.BehaviorManagement',
                'preparatory_group.ProblemSolving', 'preparatory_group.Socialization', 'preparatory_group.PhysicalDevelop',
                'preparatory_group.Movements',
                'preparatory_group.Hygiene', 'preparatory_group.Health', 'preparatory_group.ArtisticDevelop',
                'preparatory_group.ArtisticPersonalDevelop',
                'preparatory_group.Painting', 'preparatory_group.Modeling', 'preparatory_group.Application', 'preparatory_group.Music',
                'preparatory_group.AttentionAndMemory', 'preparatory_group.Perception', 'preparatory_group.ThinkingAndSpeaking',
                'preparatory_group.EmotionsAndWill', 'preparatory_group.MotorDevelop', 'preparatory_group.VisualPerception',
                'preparatory_group.SBO',
                'preparatory_group.Orientation', 'preparatory_group.Touch',)},
     {'app': 'users', 'label': 'Педагоги'}

)

BOOTSTRAP_ADMIN_SIDEBAR_MENU = False

AUTH_USER_MODEL = 'users.CustomUser'

REST_FRAMEWORK = {
    'EXCEPTION_HANDLER': 'Application.exceptions.core_exception_handler',
    'NON_FIELD_ERRORS_KEY': 'error',
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'users.backends.JWTAuthentication',
    ),
}