from django.db import models
import sys
from gensim.models.doc2vec import Doc2Vec
from scipy import spatial
import copy

sys.path.append('../database')
import utils
# Create your models here.

m_texto = '../modelos/modelos/doc2vec.classificados_text_0_100_10'
modelo_texto = Doc2Vec.load(m_texto)

class PageRanking(models.Model):

    def queryset_para_json(self, cursor):

        colunas = [i[0] for i in cursor.description]
        queryset = cursor.fetchall()
        json_data = list()
        for tupla in queryset:
            json_data.append(dict(zip(colunas, tupla)))
        return json_data

    def ranking(self, texto, data):

        # Abrindo conexão com a base de dados.
        conn = utils.Utils().conectar('../database/database.ini')
        
        # Criando vetor de representação do texto inserido pelo usuário.
        print("Query: ", texto)
        #TODO: VOLTAR PARA O BACKUP DO MODELO PARA A VERSÃO FINAL.
        vetor_pesquisa = modelo_texto.infer_vector(texto.lower().split())
        #temporario = copy.deepcopy(modelo_texto)
        #vetor_pesquisa = temporario.infer_vector(texto.lower().split())

        # Resgatando os ids dos documentos do mês.
        # TODO: Os documentos estão sendo comparados somente com de uma tabela.
        cursor = conn.cursor()
        d = data.split('-')
        d.pop()
        tab_nome = 'documentos_'+'_'.join(d)
        sql = "SELECT id_documento FROM "+tab_nome
        cursor.execute(sql)
        comparacoes = list()

        # Obtendo o valor de comparação dos vetores com o vetor de pesquisa.
        for id_doc in cursor.fetchall():
            v = modelo_texto['DOC_%s' % id_doc[0]]
            score = spatial.distance.cosine(v, vetor_pesquisa)
            comparacoes.append([str(id_doc[0]), 1-score])
        comparacoes.sort(key=lambda x: x[1], reverse=True)

        # Resgatando os documentos mais parecidos.
        valores = ','.join([t[0] for t in comparacoes[:12]])
        sql = "SELECT * FROM "+tab_nome+" WHERE id_documento IN ("+valores+")"
        cursor.execute(sql)
        
        # Criando json de resposta.
        resposta = self.queryset_para_json(cursor)
        cursor.close()
        conn.close()
        return resposta

    def timeline(self, id_doc):

        # Abrindo conexão com a base de dados.
        conn = utils.Utils().conectar('../database/database.ini')

        sql = """SELECT data FROM """
        
        return

    """
    # TODO: Esse ranking pega arquivos de todos os tempos e deve ser utilizado
    # no algoritmo de construir a timeline não no PageRanking a princípio.
    def ranking_geral(self, texto, data):

        conn = utils.Utils().conectar('../database/database.ini')
        cursor = conn.cursor()
        vetor = modelo_titulo.infer_vector(texto.split())
        documentos = modelo_titulo.docvecs.most_similar([vetor])
        indices = [doc[0].split('_')[1] for doc in documentos]
        valores = ','.join(indices)
        d = data.split('-')
        d.pop()
        tab_nome = 'documentos_'+'_'.join(d)
        sql = "SELECT * FROM "+tab_nome+" WHERE id_documento IN ("+valores+")"
        print(sql)
        cursor.execute(sql)
        print(cursor.fetchall())
        conn.close()
    """
