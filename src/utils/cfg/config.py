from dotenv import load_dotenv
import os

load_dotenv()

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data', 'users.db')