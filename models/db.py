import json
import psycopg2
from psycopg2.extras import RealDictCursor
from instance.config import app_config


class AppDb:

    def __init__(self, config_name):


        DATABASE_URL = app_config[config_name].DATABASE_URL

        try:
            self.connection = psycopg2.connect (DATABASE_URL)
        except:
            print("Unable to connect to the database")
        self.cursor = self.connection.cursor()


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
        self.connection.close()


db = AppDb('development')