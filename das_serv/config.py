class Config:
    print('CONFIG')
    SQLALCHEMY_DATABASE_URI = 'sqlite://'
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    SECRET_KEY = 'SECRET_KEY'
    FLASK_RUN_HOST = 'localhost'
    FLASK_RUN_PORT = 8001


config = Config
