from dotenv import load_dotenv
import os
load_dotenv()

DATABASE_CONFIG = {
    "host": os.environ.get("DB_HOST"),
    "user": os.environ.get("DB_USER"),
    "port": int(os.environ.get("DB_PORT")),  # Convert to integer if needed
    "password": os.environ.get("DB_PASSWORD"),
    "database": os.environ.get("DB_DATABASE"),
}
CONNECTION_STRING = "dbname={} user={} password={} host={} port={}".format(
    DATABASE_CONFIG['database'],
    DATABASE_CONFIG['user'],
    DATABASE_CONFIG['password'],
    DATABASE_CONFIG['host'],
    DATABASE_CONFIG['port']
)

JWT_KEY = os.environ.get("JWT_KEY")