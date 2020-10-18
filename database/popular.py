import utils
import json
import pandas as pd


class Popular(utils.Utils):

    def __init__(self):
        super().__init__()

        with open('configs.json', 'r') as conf:
            self.configs = json.load(conf)

    def inserir_dados(self):

        conn = self.conectar()
        cursor = conn.cursor()

        sql = """CREATE TABLE IF NOT EXISTS public.documentos (
            id_documento integer NOT NULL PRIMARY KEY,
            titulo text COLLATE pg_catalog."pt_BR.utf8" NOT NULL,
            texto text COLLATE pg_catalog."pt_BR.utf8" NOT NULL,
            data date NOT NULL,
            link text NOT NULL,
            classe text NOT NULL)
            WITH (
            OIDS=FALSE)"""

        cursor.execute(sql)

        # Obtendo as categorias existentes no dataset.
        df = pd.read_csv(self.configs["dataframe"])
        
        lista = []
        for doc in df.itertuples():
            tupla = (doc.Index, doc.title, doc.text,
                doc.date, doc.link, doc.classe,)
            lista.append(tupla)

        lista.sort(key=lambda x: x[3])

        sql = """INSERT INTO documentos (id_documento, titulo, texto, data, link, classe)
                VALUES (%s,%s,%s,%s,%s,%s)"""
        
        cursor.executemany(sql, lista)
        cursor.close()
        conn.commit()

if __name__ == '__main__':

    p = Popular()
    p.inserir_dados()
