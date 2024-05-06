import os
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def get_db_uri():
    db_user = os.getenv("DB_USER")
    db_password = os.getenv("DB_PASSWORD")
    db_host = os.getenv("DB_HOST")
    db_name = os.getenv("DB_NAME")
    return "mysql+pymysql://{user}:{password}@{host}/{name}".format(user=db_user, password=db_password, host=db_host, name=db_name)