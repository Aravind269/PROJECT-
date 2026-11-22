import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-secret-community-energy-2026')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # MySQL connection parameters
    MYSQL_USER = os.environ.get('MYSQL_USER', 'root')
    MYSQL_PASSWORD = os.environ.get('MYSQL_PASSWORD', '')
    MYSQL_HOST = os.environ.get('MYSQL_HOST', 'localhost')
    MYSQL_PORT = os.environ.get('MYSQL_PORT', '3306')
    MYSQL_DB = os.environ.get('MYSQL_DB', 'community_renewable_energy')

    @classmethod
    def get_database_uri(cls):
        # 1. Direct explicit URI
        explicit_uri = os.environ.get('DATABASE_URI')
        if explicit_uri and explicit_uri.strip():
            return explicit_uri.strip()

        # 2. Build MySQL URI
        password_part = f":{cls.MYSQL_PASSWORD}" if cls.MYSQL_PASSWORD else ""
        mysql_uri = (
            f"mysql+pymysql://{cls.MYSQL_USER}{password_part}@"
            f"{cls.MYSQL_HOST}:{cls.MYSQL_PORT}/{cls.MYSQL_DB}?charset=utf8mb4"
        )

        # 3. Test if MySQL is reachable
        try:
            import pymysql
            port = int(cls.MYSQL_PORT) if str(cls.MYSQL_PORT).isdigit() else 3306
            conn = pymysql.connect(
                host=cls.MYSQL_HOST,
                user=cls.MYSQL_USER,
                password=cls.MYSQL_PASSWORD,
                port=port,
                connect_timeout=2
            )
            # Try to ensure database exists
            with conn.cursor() as cursor:
                cursor.execute(f"CREATE DATABASE IF NOT EXISTS `{cls.MYSQL_DB}` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;")
            conn.select_db(cls.MYSQL_DB)
            conn.close()
            return mysql_uri
        except Exception as e:
            # Fallback to local SQLite if MySQL is not currently running or reachable
            sqlite_path = os.path.join(BASE_DIR, 'community_energy.db')
            print(f"[Database Notice] MySQL connection to '{cls.MYSQL_HOST}:{cls.MYSQL_PORT}' not active ({e}).")
            print(f"[Database Notice] Using SQLite fallback at: {sqlite_path}")
            print(f"[Database Notice] To use MySQL, start your MySQL server and run 'python init_db.py'.")
            return f"sqlite:///{sqlite_path}"

# Assign dynamic SQLALCHEMY_DATABASE_URI
Config.SQLALCHEMY_DATABASE_URI = Config.get_database_uri()
