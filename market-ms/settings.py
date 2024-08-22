import os
import dotenv


dotenv.load_dotenv(dotenv_path=".env")

listen = os.environ.get('LISTEN')
redis_url = os.environ.get('REDIS_URL')


def get_db_config():
    dbconfig = {
        'host': os.environ.get('MYSQl_HOST'),
        'user': os.environ.get('MYSQL_USER'),
        'password': os.environ.get('MYSQL_PASSWORD'),
        'database': os.environ.get('MYSQL_DATABASE')
    }
    return dbconfig
