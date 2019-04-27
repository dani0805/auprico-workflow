INSTALLED_APPS = (
    'auprico_core',
    'auprico_auth',
    'auprico_workflow',
    'django.contrib.auth',
    'django.contrib.contenttypes',

)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
}
SECRET_KEY = "secret_key_for_testing"
AUTH_USER_MODEL = "auprico_auth.User"
USE_TZ=True
