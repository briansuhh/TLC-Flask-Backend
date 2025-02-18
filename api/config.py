import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY")
    SQLALCHEMY_DATABASE_URI = os.getenv("SQLALCHEMY_DATABASE_URI")
    NOSQLDB_URI = os.getenv("NOSQLDB_URI")
    NOSQLDB_NAME = os.getenv("NOSQLDB_NAME")
    LOGGING_COLLECTION_NAME = os.getenv("LOGGING_COLLECTION_NAME")
    SENSITIVE_FIELDS = {"password"}
