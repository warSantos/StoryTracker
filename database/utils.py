import psycopg2
from configparser import ConfigParser

class Utils():

    def config(self, confs='database.ini', section='storytracker'):

        parser = ConfigParser()
        parser.read(confs)

        # get section, default to postgresql
        db = {}
        if parser.has_section(section):
            params = parser.items(section)
            for param in params:
                db[param[0]] = param[1]
        else:
            raise Exception(
                'Section {0} not found in the {1} file'.format(section, confs))

        return db

    def conectar(self, confs=None):

        conn = None
        try:
            # read connection parameters
            params = None
            if confs is None:
                params = self.config()
            else:
                params = self.config(confs)

            # connect to the PostgreSQL server
            print('Connecting to the PostgreSQL database...')
            conn = psycopg2.connect(**params)

            return conn
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
