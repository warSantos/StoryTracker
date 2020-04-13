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

        sql_create = """CREATE TABLE IF NOT EXISTS public.%s (
            id_documento integer NOT NULL PRIMARY KEY,
            texto text COLLATE pg_catalog."pt_BR.utf8" NOT NULL,
            titulo text COLLATE pg_catalog."pt_BR.utf8" NOT NULL,
            data date NOT NULL,
            link text NOT NULL,
            classe text NOT NULL)
            WITH (
            OIDS=FALSE)"""

        # Obtendo as categorias existentes no dataset.
        df = pd.read_csv(self.configs["dataframe"]).sort_values(by=['date'])

        print("Criando tabelas...")
        # Criando as tabelas para cada mês caso elas não existam e
        datas = set(df['date'])
        d_datas = {}
        for data in datas:
            d = data.split('-')
            d.pop()
            tab_nome = 'documentos_'+'_'.join(d)
            if tab_nome not in d_datas:
                d_datas[tab_nome] = list()

            for tab_nome in sorted(d_datas.keys()):
                #cursor.execute("DROP TABLE IF EXISTS %s" % tab_nome)
                cursor.execute(sql_create % tab_nome)

        print("Inserindo documentos...")
        # Inserindo os documentos na base de dados.
        classes = set(df['classe'])
        for classe in classes:
            ndf = df[df['classe'] == classe]
            for doc in ndf.itertuples():
                d = doc.date.split('-')
                d.pop()
                tab_nome = 'documentos_'+'_'.join(d)
                tupla = (doc.Index, doc.text, doc.title,
                         doc.date, doc.link, doc.classe,)
                d_datas[tab_nome].append(tupla)

        for tab_nome in d_datas:

            sql = "INSERT INTO "+tab_nome+"(id_documento, texto, titulo, data, link, classe)"\
                " VALUES (%s,%s,%s,%s,%s,%s)"
            print(d_datas[tab_nome][:1])
            cursor.executemany(sql, d_datas[tab_nome])

        cursor.close()
        conn.commit()
        print("Finalizado com Sucesso!")

if __name__ == '__main__':

    p = Popular()
    p.inserir_dados()
