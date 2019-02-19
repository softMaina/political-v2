import os

class Config(object):

    DEBUG=False

class Development(Config):
    DEBUG=True
    DB_URL="dbname='politicalv2' host='localhost' port='5432' user='postgres' password='root'"


class Testing(Config):
    DEBUG=True
    Testing=True
    DB_URL="dbname='politicalv2test' host='localhost' port='5432' user='postgres' password='root'"


class Staging(Config):
    DEBUG=True
  
class Production(Config):
    DEBUG=False
    Testing=False
    DB_URL="postgres://eyqsllupjisbqh:fd04574df5a5c1859c55a7f21506ad277acc5f529958186e42ee852dbadaad73@ec2-50-17-193-83.compute-1.amazonaws.com:5432/d885u3udv4uoft"

config = {
    'development': Development,
    'testing': Testing,
    'staging':Staging,
    'production': Production,
    'db_url':"dbname='politicalv2' host='localhost' port='5432' user='postgres' password='root'",
    'test_db_url':"dbname='politicalv2test' host='localhost' port='5432' user='postgres' password='root'"
}