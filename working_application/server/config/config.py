import os

DB_CONFIG = {
    "db_name": "map_server",
    "db_host": os.environ['DB_HOST'],
    "db_user": os.environ['DB_USER'],
    "db_pass": os.environ['DB_PASS'],
    "db_port": os.environ['DB_PORT'],
    "table_list": [
        "sessions"
    ]
}