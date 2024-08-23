import os
import dotenv


dotenv.load_dotenv(dotenv_path=".env")

nats_url = os.environ.get('NATS_URL')
