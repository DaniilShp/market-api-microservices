import os
import re
import dotenv


dotenv.load_dotenv(dotenv_path=".env")

listen = os.environ.get('LISTEN')
market_url = os.environ.get('MARKET_URL')
adminpanel_url = os.environ.get('ADMINPANEL_URL')


"""Proxy server config"""
not_protected_routes = [  # no need authorization
    re.compile('/market/get_name'),
    re.compile('/market/get_all_products'),
    re.compile('/adminpanel/get_name')
]

print(bool(re.fullmatch(not_protected_routes[0], '/market/get_name')))

def get_db_config():
    dbconfig = {
        'host': os.environ.get('MYSQl_HOST'),
        'user': os.environ.get('MYSQL_USER'),
        'password': os.environ.get('MYSQL_PASSWORD'),
        'database': os.environ.get('MYSQL_DATABASE')
    }
    return dbconfig
