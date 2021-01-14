import utils
import json
import pandas as pd


class RemoverTabelas(utils.Utils):

    def __init__(self):
        super().__init__()

        with open('configs.json', 'r') as conf:
            self.configs = json.load(conf)

    def remover_tabelas(self):

        conn = self.conectar()
        cursor = conn.cursor()

        sql = """SELECT table_name FROM information_schema.tables WHERE table_schema = 'public' AND table_catalog = 'storytracker'"""
        cursor.execute(sql)

        for t in cursor.fetchall():

            sql = """DROP TABLE %s""" % t[0]
            cursor.execute(sql)

        cursor.close()
        conn.commit()

if __name__ == '__main__':

    p = RemoverTabelas()
    p.remover_tabelas()
