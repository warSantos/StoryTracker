from sys import argv, exit
import pandas as pd
import numpy as np
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.neural_network import MLPClassifier
from sklearn.linear_model import LogisticRegression
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
        
        """
        d = {'vetor': vetores_treino, 'classe': classes_treino}
        df_class = pd.DataFrame(d)
        d = {'vetor': vetores_teste, 'classe': classes_teste}
        df_noclass = pd.DataFrame(d)
        return df_class, df_noclass
        """

        docs_classif["vetor"] = vetores_treino
        docs_classif["classe"] = classes_treino
        docs_sem_classif["vetor"] = vetores_teste
        docs_sem_classif["classe"] = classes_teste


    def cross_valid(self, clf, vetores, classes):

        scores = cross_val_score(clf, vetores, classes,\
            cv=5, scoring='f1_macro')    
        print("F1-Measure: ", scores)

    def treinar(self, treino, alg):
        
        vetores = list()
        classes = list()
        for index, row in treino.iterrows():
            vetores.append(row['vetor'])
            classes.append(row['classe'])

        # Regressão Logistica.
        if alg == 1:
            clf = LogisticRegression(random_state=0, max_iter=150, solver='sag')#C=0.8)
        # Naive Bayes.
        elif alg == 2:
            clf = GaussianNB()
        # Rede Neural.
        elif alg == 3:
            clf = MLPClassifier(solver='sgd', alpha=1e-5,\
                hidden_layer_sizes=(100, 1), random_state=1, learning_rate= 'adaptive')
        else:
            clf = RandomForestClassifier(max_depth=2, random_state=0)
            
        self.cross_valid(clf, vetores, classes)

    def classificar(self, treino, teste, alg):
        
        # Regressão Logistica.
        if alg == 1:
            clf = LogisticRegression(random_state=0, max_iter=150, solver='sag')#, C=0.8)
        # Naive Bayes.
        elif alg == 2:
            clf = GaussianNB()
        # Rede Neural.
        elif alg == 3:
            clf = MLPClassifier(solver='sgd', alpha=1e-5,\
                hidden_layer_sizes=(100, 1), random_state=1, learning_rate= 'adaptive', max_iter=300)
        else:
            clf = RandomForestClassifier(max_depth=2, random_state=0)
        
        # Treinando o modelo.
        vetores = list()
        classes = list()
        for index, row in treino.iterrows():
            vetores.append(row['vetor'])
            classes.append(row['classe'])
        
        clf.fit(vetores, classes)

        # Classificando as novas amostras.
        vetores = list()
        for index, row in teste.iterrows():
            vetores.append(row['vetor'])
        classificados = clf.predict(vetores)
        
        return classificados


    def executar(self, dataset, caminho_modelo, operacao='treinar', alg=1):

        modelo = Doc2Vec.load(caminho_modelo)
        df = pd.read_csv(dataset)
        docs_classif, docs_sem_classif = self.pre_proc(df)
        #treino, teste = self.dataset_treino(docs_classif, docs_sem_classif, modelo)
        self.dataset_treino(docs_classif, docs_sem_classif, modelo)
        if operacao == 'treinar':
            #self.treinar(treino, alg)
            self.treinar(docs_classif, alg)
        elif operacao == 'classif':
            #classificados = self.classificar(treino, teste, alg)
            classificados = self.classificar(docs_classif, docs_sem_classif, alg)
            # Persistindo o novo dataframe com documentos classificados.

    
if __name__=='__main__':

    c = Classificador()
    c.executar(argv[1], argv[2], argv[3], int(argv[4]))
    