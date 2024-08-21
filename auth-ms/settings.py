import os
import dotenv


dotenv.load_dotenv(dotenv_path=".env")

listen = os.environ.get('LISTEN')
market_url = os.environ.get('MARKET_URL')
adminpanel_url = os.environ.get('ADMINPANEL_URL')

def get_db_config():
    dbconfig = {
        'host': os.environ.get('MYSQl_HOST'),
        'user': os.environ.get('MYSQL_USER'),
        'password': os.environ.get('MYSQL_PASSWORD'),
        'database': os.environ.get('MYSQL_DATABASE')
    }
    return dbconfig
