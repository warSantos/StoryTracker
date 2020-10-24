#!/usr/bin/env python
# coding: utf-8

import os
import pandas as pd
from operator import index
from sklearn.ensemble import AdaBoostClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import LinearSVC
from sklearn.linear_model import LogisticRegression
from sklearn.neural_network import MLPClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import cross_val_score
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer

from classificadores import Classificador


class TfIdf():

    def __init__(self):

        # Se o dataset de treino já foi processado e salvo,
        # carregue ele ao lugar de processar tudo novamente.
        if os.path.exists('../dados/dataset_treino.csv'):
            print("Carregando dataset pré-processado.")
            self.df_treino = pd.read_csv('../dados/dataset_treino.csv')
            return

        df = pd.read_csv('../dados/articles_limpo.csv')  # ,nrows=2000)
        df = df[df['text'].notna()]

        categorias_finais = ['tec', 'esporte',
                             'ilustrada', 'mercado', 'poder', 'mundo']
        categorias_diluidas = list(
            set(df['category']) - set(categorias_finais))

        # Agrupando coluna de tecnologia com ciência.
        df["category"] = df["category"].replace("ciencia", "tec")

        # Criando dataset com categorias finais para teste.
        docs_classif = df
        for cat in categorias_diluidas:
            docs_classif = docs_classif[docs_classif['category'] != cat]

        tokenizer = RegexpTokenizer(r'\w+')
        documentos = list()
        stpw = {}
        for p in stopwords.words("portuguese"):
            stpw[p] = True

        for row in docs_classif.itertuples():
            doc = list()
            for p in tokenizer.tokenize(row.text.lower()):
                if p not in stpw:
                    doc.append(p)
            documentos.append(' '.join(doc))

        docs_classif['texto_limpo'] = documentos
        self.df_treino = docs_classif[['texto_limpo', 'category']]
        self.df_treino.to_csv('../dados/dataset_treino.csv', index=False)

    def salvar_scores(self, scores, label):

        pt = open('tf_idf/'+label+'.txt', 'w')
        for score in scores:
            pt.write(str(score)+'\n')
        pt.close()

    def tf_idf(self):

        count_vect = CountVectorizer()
        X_train_counts = count_vect.fit_transform(
            self.df_treino['texto_limpo'])
        tfidf_transformer = TfidfTransformer()
        X_train_tfidf = tfidf_transformer.fit_transform(X_train_counts)

        return X_train_counts, X_train_tfidf

    def avaliar_classificacao(self, X_train_counts, X_train_tfidf, alg=1, vezes=1):

        scores = []

        label = {
            1: "LogisticRegression",
            2: "GaussianNB",
            3: "MLPClassifier",
            4: "AdaBoostClassifier",
            5: "LinearSVC",
            6: "KNeighborsClassifier",
            7: "RandomForestClassifier"
        }

        for i in range(0, vezes):

            # Regressão Logistica.
            if alg == 1:
                print("Aplicando: ", label[alg])
                clf = LogisticRegression(
                    random_state=0, max_iter=300, solver='saga')
            # Naive Bayes.
            elif alg == 2:
                print("Aplicando: ", label[alg])
                clf = GaussianNB()
            # Rede Neural.
            elif alg == 3:
                print("Aplicando: ", label[alg])
                clf = MLPClassifier(solver='adam', hidden_layer_sizes=(
                    100), learning_rate_init=0.002, learning_rate='adaptive', max_iter=200)
            elif alg == 4:
                print("Aplicando: ", label[alg])
                clf = clf = AdaBoostClassifier(n_estimators=100)
            elif alg == 5:
                print("Aplicando: ", label[alg])
                clf = LinearSVC(random_state=0, tol=1e-5)
            elif alg == 6:
                print("Aplicando: ", label[alg])
                clf = KNeighborsClassifier(n_neighbors=3)
            elif alg == 7:
                print("Aplicando: ", label[alg])
                clf = RandomForestClassifier(max_depth=2, random_state=0)

            scores += list(cross_val_score(clf, X_train_counts,
                                           self.df_treino['category'], cv=5, scoring='f1_macro', n_jobs=25))
        print("F1-Measure: ", label[alg], scores)
        self.salvar_scores(scores, label[alg])

    def executar(self):

        X_train_counts, X_train_tfidf = self.tf_idf()
        vezes = 6
        for alg in range(1, 8):
            self.avaliar_classificacao(X_train_counts,
                                       X_train_tfidf, alg, vezes)


if __name__ == '__main__':

    tf = TfIdf()
    tf.executar()
