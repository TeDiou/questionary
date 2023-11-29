import os


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'questionnaireDemo'

    @staticmethod
    def init_app(app):
        pass

config = {
    'default': Config,
    'MYSQL_PASSWORD': '123456',
    'DATABASE_NAME': 'trainplan'
}

