import os

class DBSettings:
    DB_ENGINE = "mysql+pymysql"
    DB_HOST = os.getenv("RDS_HOSTNAME","tasks-db.cu8jobcum719.sa-east-1.rds.amazonaws.com")
    DB_NAME = os.getenv("RDS_DB_NAME","tasks_db")
    DB_PORT = os.getenv("RDS_PORT","3306")
    DB_USER = os.getenv("RDS_USERNAME","root")
    DB_PASSWORD = os.getenv("RDS_PASSWORD","dinocloud123$")
    SQLALCHEMY_DATABASE_URI = "{0}://{1}:{2}@{3}:{4}/{5}".format(DB_ENGINE, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME)