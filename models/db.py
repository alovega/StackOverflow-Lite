import psycopg2
from psycopg2.extras import RealDictCursor
from instance.config import app_config
import os


class AppDb:

    def __init__(self, config_name):

        DATABASE_URL = app_config[config_name].DATABASE_URL

        try:
            self.connection = psycopg2.connect(DATABASE_URL)
        except:
            print("Unable to connect to the database")
        self.cursor = self.connection.cursor(cursor_factory=RealDictCursor)

    def commit(self):
        self.connection.commit()

    def create_tables(self, table):
        self.cursor.execute(table)
        self.commit()

    def drop_table(self, table_name):
        self.cursor.execute("DROP TABLE IF EXISTS " + table_name + ";")
        self.commit()

    def close(self):
        self.cursor.close()


current_environment = os.getenv("APP_SETTINGS")
print (current_environment)

db = AppDb(current_environment)