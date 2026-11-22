import os
from urllib.parse import urlsplit, urlunsplit, parse_qsl, urlencode
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
CA_FILE = os.path.join(BASE_DIR, "ca.pem")

class Config:
    SECRET_KEY = os.environ.get(
        "SECRET_KEY",
        "dev-secret-community-energy-2026"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    DATABASE_URI = os.environ.get("DATABASE_URI", "").strip()

    if DATABASE_URI:
        uri = DATABASE_URI

        if uri.startswith("mysql://"):
            uri = uri.replace("mysql://", "mysql+pymysql://", 1)

        if uri.startswith("mysql+pymysql://"):
            parts = urlsplit(uri)
            query = [
                (key, value)
                for key, value in parse_qsl(parts.query)
                if key.lower() != "ssl-mode"
            ]
            uri = urlunsplit((
                parts.scheme,
                parts.netloc,
                parts.path,
                urlencode(query),
                parts.fragment
            ))

            if not os.path.isfile(CA_FILE):
                raise RuntimeError("Aiven CA certificate not found: " + CA_FILE)

            SQLALCHEMY_ENGINE_OPTIONS = {
                "connect_args": {
                    "ssl": {"ca": CA_FILE}
                },
                "pool_pre_ping": True,
                "pool_recycle": 280
            }

        SQLALCHEMY_DATABASE_URI = uri

    elif os.environ.get("MYSQL_HOST"):
        from urllib.parse import quote_plus

        user = os.environ.get("MYSQL_USER", "root")
        password = quote_plus(os.environ.get("MYSQL_PASSWORD", ""))
        host = os.environ["MYSQL_HOST"]
        port = os.environ.get("MYSQL_PORT", "3306")
        database = os.environ.get("MYSQL_DB", "defaultdb")

        SQLALCHEMY_DATABASE_URI = (
            f"mysql+pymysql://{user}:{password}@{host}:{port}/{database}"
        )

    else:
        SQLALCHEMY_DATABASE_URI = (
            "sqlite:///" + os.path.join(BASE_DIR, "community_energy.db")
        )