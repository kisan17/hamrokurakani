import os

basedir = os.path.abspath(os.path.dirname(__file__))
dotenvsecrets = os.path.join(basedir, '.env')
database = os.path.join(basedir, 'site.db')


class Configuration:

    SECRET_KEY = '5791628bb0b13ce0c676dfde280ba245'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + database
    SQLALCHEMY_TRACK_MODIFICATIONS = False