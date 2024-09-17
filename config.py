import os

class Config:
    MYSQL_USER = os.getenv('MYSQL_USER', 'root')
    MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD', 'Mayson@0902')
    MYSQL_DB = os.getenv('MYSQL_DB', 'logifact_db')
    MYSQL_HOST = os.getenv('MYSQL_HOST', 'localhost')
    SECRET_KEY = os.getenv('FLASK_SECRET_KEY', 'p9FZ!Q3Ys5X@4mD8Z7FJqP#dPa2lT$W')