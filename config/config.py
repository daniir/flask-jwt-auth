from dotenv import load_dotenv
import os

load_dotenv()

port=os.environ['PORT']
secret_key=os.environ['SECRET_KEY']
database_uri = os.environ['DATABASE_URI']