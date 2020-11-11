import pandas as pd
import spacy
import json

class Extracao():

    def __init__(self):

        self.nlp = spacy.load('pt_core_news_lg')
        df = pd.read_csv('../dados/articles_limpo.csv')
        df = df[(df['date'] >= '2016-05-01') & (df['date'] <= '2016-12-01')]
        self.df = df[(df["category"] == 'poder') | (df["category"] == 'mundo') | (df["category"] == 'mercado')]
        with open('configs/ext_classes.json', 'r') as f:
            self.classes = json.load(f)

    def extrair(self):

        lista_docs = []
        entidades = {}
        dic_ents = {}

        doc_id = 0
        # Extração de nomes de entidades.
        #for tupla in self.df.head(100).itertuples(index=False):
        for tupla in self.df.itertuples(index=False):
            doc = self.nlp(tupla.text)
            ents_doc = {}
            # Para toda entidade no documento.
            for ent in doc.ents:
                nome_ent = ent.text.lower()
                # Se for a primeira aparição da entidade.
                if nome_ent not in dic_ents:
                    # Adicionando a entidade no dicionário de entidades.
                    dic_ents[nome_ent] = ent.label_
                ## Reunindo as entidades por documentos.
                # Se a entidade pertencer a alguma das classes de interesse.
                if ent.label_ in self.classes:
                    if nome_ent not in ents_doc:
                        ents_doc[nome_ent] = [ent.label_, 0]
                    ents_doc[nome_ent][1] += 1
                ## Agrupando os documentos e suas frequências pelas entidades.
                if nome_ent not in entidades:
                    entidades[nome_ent] = {}
                if doc_id not in entidades[nome_ent]:
                    entidades[nome_ent][doc_id] = 0
                entidades[nome_ent][doc_id] += 1
            # Adicionando o documento a lista.
            lista_docs.append([doc_id, tupla.date, ents_doc])
            doc_id += 1

        #pt = open('preproc/docs_ents_exemplo.json','w')
        #json.dump(lista_docs, pt, ensure_ascii=False, indent=4)
        pt = open('preproc/docs_ents.json','w')
        json.dump(lista_docs, pt, ensure_ascii=False)
        pt.close()

        #pt = open('preproc/entidades_exemplo.json','w')
        #json.dump(entidades, pt, ensure_ascii=False, indent=4)
        pt = open('preproc/entidades.json','w')
        json.dump(entidades, pt, ensure_ascii=False)

        #pt = open('preproc/map_ents_exemplo.json','w')
        #json.dump(dic_ents, pt, ensure_ascii=False, indent=4)
        pt = open('preproc/map_ents.json','w')
        json.dump(dic_ents, pt, ensure_ascii=False)
        pt.close()

if __name__=='__main__':

    e = Extracao()
    e.extrair()