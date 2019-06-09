import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'c1.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # currently testing with one assessment
    ASSESSMENT_ID = 272
    NUMBER_OF_QUESTIONS = 5
    TIME_LIMIT_IN_SECONDS = 3600
