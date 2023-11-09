import os

class Sms:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'

    PILVO_AUTH_ID = 'YOUR_AUTH_ID'
    PILVO_AUTH_TOKEN = 'YOUR_AUTH_TOKEN'
    PILVO_NUMBER = 'SOURCE_NUMBER'
    PHLO_ID = 'PHLO_ID'
