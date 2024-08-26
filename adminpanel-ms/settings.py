import os
import dotenv


dotenv.load_dotenv(dotenv_path=".env")

listen = os.environ.get('LISTEN')
nats_url = os.environ.get('NATS_URL')
mongo_url = os.environ.get('MONGO_URL')
