import os

SECRET_KEY = os.environ.get('SECRET_KEY', 'your_production_secret_key')
WTF_CSRF_ENABLED = True 