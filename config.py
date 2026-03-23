import os
from dotenv import load_dotenv

load_dotenv()

DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")

PC_HOST = os.getenv("PC_HOST")
OLLAMA_PORT = os.getenv("OLLAMA_PORT")

CHAT_MODEL = os.getenv("CHAT_MODEL")
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL")

OLLAMA_BASE_URL = f"http://{PC_HOST}:{OLLAMA_PORT}"