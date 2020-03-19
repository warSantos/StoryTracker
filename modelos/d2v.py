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
                words=doc, tags=['DOC_%s' % index]))
        return documentos

    def treinar(self, dataset, atributo):

        documentos = self.pre_proc(dataset, atributo)
        modelo = Doc2Vec(vector_size=100, window=10, min_count=1, alpha=0.025, min_alpha=0.025, workers=20)
        modelo.build_vocab(documentos)
        for epoca in range(10):
            modelo.train(documentos, total_examples=modelo.corpus_count, epochs=1)
            modelo.alpha -= 0.002
            modelo.min_alpha = modelo.alpha

        modelo.save('modelos/doc2vec.'+atributo)


if __name__ == '__main__':

    m = Modelo()
    m.treinar(argv[1], argv[2])
