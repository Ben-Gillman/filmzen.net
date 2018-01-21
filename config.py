class Config(object):
    # TODO change this to be secure
    SECRET_KEY = 'change me!'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///data.sqlite3'
    SQLALCHEMY_TRACK_MODIFICATIONS = False