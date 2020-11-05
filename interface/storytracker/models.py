from django.db import models
import sys
from gensim.models.doc2vec import Doc2Vec
from numpy.lib.function_base import append
from scipy import spatial
import copy
from .base import Base
import json

sys.path.append('../database')
import utils
# Create your models here.

m_texto = '../modelos/modelos/doc2vec.classificados_text_1_100_10'
#m_texto = '../modelos/modelos/doc2vec.classificados_title_0_100_10'
modelo_texto = Doc2Vec.load(m_texto)


class PageRanking(models.Model):

    def ranking(self, texto, data, meses, n_docs, classes):

        modulo_base = Base()
        # Abrindo conexão com a base de dados.
        conn = utils.Utils().conectar('../database/database.ini')

        # Criando vetor de representação do texto inserido pelo usuário.
        # TODO: VOLTAR PARA O BACKUP DO MODELO PARA A VERSÃO FINAL.
        # Estratégia 1
        vetor_pesquisa = modulo_base.inferir_vetor(texto, modelo_texto)
        # Estratégia 2
        #vetor_pesquisa = modelo_texto.infer_vector(texto.lower().split())
        # Estratégia 3
        #temporario = copy.deepcopy(modelo_texto)
        #vetor_pesquisa = temporario.infer_vector(texto.lower().split())

        # Resgatando os ids dos documentos do mês.
        # TODO: Os documentos estão sendo comparados somente com de uma tabela.
        cursor = conn.cursor()
        f_classes = modulo_base.formatar_classes(classes)
        sql = """SELECT id_documento FROM documentos WHERE data >= %s AND data <= %s AND classe IN ({0})""".format(f_classes)
        
        data_ini, data_fim = modulo_base.datas_raio(data, meses)
        cursor.execute(sql, (data_ini, data_fim,))
        comparacoes = list()

        # Obtendo o valor de comparação dos vetores com o vetor de pesquisa.
        for id_doc in cursor.fetchall():
            v = modelo_texto['DOC_%s' % id_doc[0]]
            score = spatial.distance.cosine(v, vetor_pesquisa)
            comparacoes.append([str(id_doc[0]), 1-score])
        comparacoes.sort(key=lambda x: x[1], reverse=True)

        # Resgatando os documentos mais parecidos.
        valores = ','.join([t[0] for t in comparacoes[:n_docs]])
        print("Valores: ", valores)
        sql = """SELECT * FROM documentos WHERE id_documento IN (%s)""" % valores
        cursor.execute(sql)

        # Criando json de resposta.
        resposta = modulo_base.queryset_para_json(cursor)
        cursor.close()
        conn.close()
        return resposta


class TimelineModel(models.Model):

    # Retorna o id do documento do vizinho mais próximo ao documento de
    # referência e os jsons dos documentos do intervalo.
    def vizinhos(self, id_doc_ref, query_doc, vetor_query, data_ini, data_end, f_classes, cursor, n_vizinhos=10):

        # Obtendo o valor de comparação dos vetores com o vetor de pesquisa.
        sql = """SELECT id_documento FROM documentos WHERE data >= %s AND data <= %s AND classe IN ({0})""".format(f_classes)
        comparacoes = list()

        cursor.execute(sql, (data_ini, data_end,))
        # Obtendo o vetor do documento de referência.
        vetor_doc_ref = modelo_texto['DOC_%s' % id_doc_ref]
        # Para cada documento.
        for id_doc_viz in cursor.fetchall():
            v = modelo_texto['DOC_%s' % id_doc_viz[0]]
            score = ((1 - query_doc) * spatial.distance.cosine(v, vetor_doc_ref) + \
                    query_doc * spatial.distance.cosine(v, vetor_query))
            comparacoes.append([id_doc_viz[0], 1-score])
        # Se não existir documentos no intervalo.
        if not comparacoes:
            return -1, []

        comparacoes.sort(key=lambda x: x[1], reverse=True)
        #print("IDs: ", id_doc_ref, comparacoes[0][0])
        # Resgatando N vizinhos mais parecidos.
        valores = ','.join([str(t[0]) for t in comparacoes[:n_vizinhos]])
        sql = """SELECT titulo, link, data FROM documentos WHERE id_documento IN (%s)""" % valores
        cursor.execute(sql)
        docs = Base().queryset_para_json(cursor)
        id_doc_ref = comparacoes[0][0]
        return id_doc_ref, docs

    # Retorna Realiza a expansão de documentos para o passado e futuro.
    # limite: quantidade de dias a frente ou atrás de uma expansão.
    # salto: tamanho da janela de comparação ex.:(2020-01-01 - 2020-01-16)
    # para 15 dias de janela.
    # sentido: -1 passado 1 futuro.
    def expansao(self, id_doc, query_doc, vetor_query, data_doc, f_classes, cursor, limite=60, salto=15, sentido=-1):

        id_doc_ref = id_doc
        data_fim = data_doc
        cont = 0
        docs_set = []
        modulo_base = Base()
        while cont < limite:
            data_ini = str(modulo_base.data_relativa(
                data_fim, meses=0, dias=15*sentido))
            # Se a expansão for para o passado.
            if sentido == -1:
                id_doc_ref, docs = self.vizinhos(
                    id_doc_ref, query_doc, vetor_query, data_ini, data_fim, f_classes, cursor)
                # Se a expansão chegou ao limite da base de dados.
                if id_doc_ref == -1:
                    break
                docs_set.insert(0, docs)
            # Se a expansão for para o futuro no código seguinte a variável
            # data_ini vai ser maior que a data data_fim, dessa forma basta
            # inverter a ordem das datas.
            else:
                id_doc_ref, docs = self.vizinhos(
                    id_doc_ref, query_doc, vetor_query, data_fim, data_ini, f_classes, cursor)
                # Se a expansão chegou ao limite da base de dados.
                if id_doc_ref == -1:
                    break
                docs_set.append(docs)
            # Atualizando a data de borda.
            data_fim = data_ini
            cont += salto

        return docs_set

    def timeline(self, info):

        # Selecionando os dados.
        id_doc = int(info["id_doc"].replace("checkbox_",""))
        query = info["query"]
        query_doc = float(info["query_doc"])
        meses = int(info["meses"])
        salto = int(info["tam_intervalo"])
        classes = info["classes"]

        # Abrindo conexão com a base de dados.
        conn = utils.Utils().conectar('../database/database.ini')

        # Retorna a data do documento.
        sql = """SELECT data FROM documentos WHERE id_documento = %s"""
        cursor = conn.cursor()
        cursor.execute(sql, (id_doc,))
        data_doc = str(cursor.fetchall()[0][0])

        # TODO: Os primeiros testes vão ser feitos resgatando somente
        # 60 dias a frente e após uma data prefixada, com a seleção de
        # apenas um documento podendo ser expandido depois.
        tempo = meses * 30

        # Gerando vetor de representação da query.
        #vetor_query = modelo_texto.infer_vector(query.lower().split())
        modulo_base = Base()
        vetor_query = modulo_base.inferir_vetor(query, modelo_texto)

        # Formatando as classes dos documentos.
        f_classes = modulo_base.formatar_classes(classes)

        # Procuando os documentos referentes ao passado.
        passado = self.expansao(
            id_doc, query_doc, vetor_query, data_doc, f_classes, cursor, limite=tempo, salto=salto)

        # Expandindo em direção aos documentos no futuro.
        futuro = self.expansao(
            id_doc, query_doc, vetor_query, data_doc, f_classes, cursor, limite=tempo, salto=salto, sentido=1)

        return self.formatar(passado, futuro)
        # return passado + futuro

    def formatar(self, passado, futuro):

        tml = passado + futuro
        # Para cada intervalo de tempo.
        # TODO a timeline tem a opção de marcar onde começar
        # a sua visualização.
        # Adicionando o slide inicial como o primeiro item do json.
        eventos = [len(passado), {"events": []}]
        # Selecionando o evento base para fazer ele como
        # a página inicial da timeline.
        for intervalo in tml:

            evento = {}
            # Selecionando o documento de referência (mais similar).
            doc_principal = intervalo.pop(0)

            # Configurando a data do intervalo como a do documento principal.
            ano, mes, dia = str(doc_principal["data"]).split("-")
            evento["start_date"] = {
                "day": dia,
                "month": mes,
                "year": ano
            }

            # Configurando o título.
            headline = "<a href=\"#\"> %s </a>" % doc_principal["titulo"]
            evento["text"] = {
                "headline": headline
            }

            # Configurando o texto
            # Configurando o texto do documento principal.
            # Configurando a div para deixar os documentos em linha.
            div_mae = "<div class=\"d-flex flex-row\">"
            text = div_mae + """<div class=\"card m-2\" style=\"width: 18rem;\">
                <div class=\"card-body\"><p class=\"card-text\">
                    <p>"""+doc_principal["titulo"]+"""</p>
                    <a href=\""""+doc_principal["link"]+"""\" class=\"btn btn-info\">Visitar notícia</a>
                </div>
            </div>"""
            cont = 1
            # Para cada documento no intervalo.
            for doc in intervalo:
                text += """<div class=\"card m-2\" style=\"width: 18rem;\">
                    <div class=\"card-body\"><p class=\"card-text\">
                        <p>"""+doc["titulo"]+"""</p>
                        <a href=\""""+doc["link"]+"""\" class=\"btn btn-info\">Visitar notícia</a>
                    </div>
                </div>"""
                if cont == 4:
                    text += "</div>"
                    text += div_mae
                    cont = -1
                cont += 1

            evento["text"]["text"] = text
            eventos[1]["events"].append(evento)
        return json.dumps(eventos)
