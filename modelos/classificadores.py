from sys import argv, exit
import pandas as pd
import numpy as np
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.neural_network import MLPClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.svm import LinearSVC
from gensim.models.doc2vec import Doc2Vec

class Classificador():

    def pre_proc(self, df):

        ## Pré processamento do dataset.
        # Definindo quais vão ser as categorias enviadas para classificação.
        categorias_finais = ['tec', 'esporte', 'ilustrada', 'mercado', 'poder', 'mundo']

        categorias_diluidas = list(set(df['category']) - set(categorias_finais))

        # Agrupando coluna de tecnologia com ciência.
        df["category"]= df["category"].replace("ciencia", "tec")

        # Criando dataset com categorias finais para teste
        docs_classif = df#.copy(deep=True)#.sample(frac=1)
        for cat in categorias_diluidas:
            docs_classif = docs_classif[docs_classif['category'] != cat]

        docs_sem_classif = df#.copy(deep=True)#.sample(frac=1)
        for cat in categorias_finais:
            docs_sem_classif = docs_sem_classif[docs_sem_classif['category'] != cat]
        
        return docs_classif, docs_sem_classif
    
    def dataset_treino(self, docs_classif, docs_sem_classif, modelo):

        vetores_treino = list()
        classes_treino = list()

        vetores_teste = list()
        classes_teste = list()

        for index, row in docs_classif.iterrows():
            try:
                vetores_treino.append(modelo['DOC_'+str(index)])
                classes_treino.append(row['category'])
            except:
                print("PADRÃO: ", index)

        for index, row in docs_sem_classif.iterrows():
            try:
                vetores_teste.append(modelo['DOC_'+str(index)])
                classes_teste.append(row['category'])
            except:
                print("GENÉRICOS: ", index)

        docs_classif["vetor"] = vetores_treino
        docs_classif["classe"] = classes_treino
        docs_sem_classif["vetor"] = vetores_teste

    def cross_valid(self, clf, vetores, classes):

        scores = cross_val_score(clf, vetores, classes,\
            cv=5, scoring='f1_macro')    
        print("F1-Measure: ", scores)

    def treinar(self, treino, alg):

        # Regressão Logistica.
        if alg == 1:
            clf = LogisticRegression(random_state=0, max_iter=150, solver='sag')#C=0.8)
        # Naive Bayes.
        elif alg == 2:
            clf = GaussianNB()
        # Rede Neural.
        elif alg == 3:
            clf = MLPClassifier(solver='adam', hidden_layer_sizes=(10,10), learning_rate_init=0.002, \
                    learning_rate= 'adaptive', max_iter=200)
        else:
            clf = RandomForestClassifier(max_depth=2, random_state=0)
            
        self.cross_valid(clf, list(treino['vetor']), list(treino['classe']))

    def classificar(self, treino, teste, alg):
        
        # Regressão Logistica.
        if alg == 1:
            clf = LogisticRegression(random_state=0, max_iter=150, solver='sag')#, C=0.8)
        # Naive Bayes.
        elif alg == 2:
            clf = GaussianNB()
        # Rede Neural.
        elif alg == 3:
            clf = MLPClassifier(solver='adam', alpha=1e-5,\
                hidden_layer_sizes=(100, 2), random_state=1, learning_rate= 'adaptive', max_iter=300)
        elif alg == 5:
            print("Aplicando: LinearSVC")
            clf = LinearSVC(random_state=0, tol=1e-5)
        else:
            clf = RandomForestClassifier(max_depth=2, random_state=0)
        
        clf.fit(list(treino['vetor']), list(treino['classe']))

        # Classificando as novas amostras.
        classificados = clf.predict(list(teste['vetor']))
        teste["classe"] = classificados
        ndf_teste = teste.drop(columns=['vetor'])
        ndf_treino = treino.drop(columns=['vetor'])
        ndf = pd.concat([ndf_treino, ndf_teste]).sort_index()
        ndf.to_csv('../dados/classificados.csv', index=False)

    def executar(self, dataset, caminho_modelo, operacao='treinar', alg=1):

        modelo = Doc2Vec.load(caminho_modelo)
        df = pd.read_csv(dataset)
        docs_classif, docs_sem_classif = self.pre_proc(df)
        self.dataset_treino(docs_classif, docs_sem_classif, modelo)
        if operacao == 'treinar':
            self.treinar(docs_classif, alg)
        elif operacao == 'classif':
            self.classificar(docs_classif, docs_sem_classif, alg)

    
if __name__=='__main__':

    c = Classificador()
    c.executar(argv[1], argv[2], argv[3], int(argv[4]))
    
