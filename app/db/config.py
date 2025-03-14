import os

DB_URL = os.environ.get('DB_URL', 'mysql+pymysql://root:root@localhost:3306/db')
