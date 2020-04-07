import pandas as pd
from gensim.models import Doc2Vec
from gensim.models.doc2vec import TaggedDocument
from sys import argv, exit
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer


class Modelo():

    def pre_proc(self, dataset, atributo):

        df = pd.read_csv(dataset)
        df = df[df[atributo].notna()]
        tokenizer = RegexpTokenizer(r'\w+')
        documentos = list()
        stpw = {}
        for p in stopwords.words("portuguese"):
            stpw[p] = True

        for index, row in df.iterrows():
            doc = list()
            for p in tokenizer.tokenize(row[atributo].lower()):
                if p not in stpw:
                    doc.append(p)
            documentos.append(TaggedDocument(
                words=doc, tags=['DOC_'+str(index)]))
        return documentos

    def treinar(self, documentos, atributo, dim, tipo, epocas):

        config = 'classificados_'+atributo+'_'+str(tipo)+'_'+str(dim)+'_'+str(epocas)
        print("MODELO COM CONFIGURAÇÃO: ", config)
        modelo = Doc2Vec(vector_size=dim, dm=tipo, window=10, min_count=1, alpha=0.025, min_alpha=0.025, workers=20)
        modelo.build_vocab(documentos)
        for epoca in range(epocas):
            modelo.train(documentos, total_examples=modelo.corpus_count, epochs=1)
            modelo.alpha -= 0.002
            modelo.min_alpha = modelo.alpha
        modelo.save('modelos/doc2vec.'+config)

    def gerar_modelos(self, dataset, atributo):
        
        dimensoes = [100]
        tipos = [0, 1]
        epocas = [10]
        documentos = self.pre_proc(dataset, atributo)
        for dim in dimensoes:
            for tipo in tipos:
                for epoca in epocas:
                    self.treinar(documentos, atributo, dim, tipo, epoca)

if __name__ == '__main__':

    m = Modelo()
    m.gerar_modelos(argv[1], argv[2])