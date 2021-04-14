from os import path, sep, pardir

basedir = path.abspath(path.dirname(__file__))
rootdir = path.normpath(basedir + sep + pardir)
dotenvsecrets = path.join(basedir, '.env')
database = path.join(rootdir, 'site.db')


class Configuration:

    SECRET_KEY = '5791628bb0b13ce0c676dfde280ba245'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + database
    SQLALCHEMY_TRACK_MODIFICATIONS = False
