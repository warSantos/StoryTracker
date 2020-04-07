from sys import argv, exit
import os
import time
import multiprocessing as mp
import pandas as pd
from gensim.models.doc2vec import Doc2Vec
from sklearn.metrics.pairwise import cosine_similarity


class Comparador():

    def agrupar(self, df):

        intervalos = {}
        for index, row in df.items():
            tokens = row.split('-')
            dia = int(tokens[2])
            chave = tokens[0]+'-'+tokens[1]+'-i'
            if dia <= 7:
                chave += '_1'
            elif dia <= 14:
                chave += '_2'
            elif dia <= 21:
                chave += '_3'
            else:
                chave += '_4'
            if chave not in intervalos:
                intervalos[chave] = list()
            intervalos[chave].append(index)
        return intervalos

    def comparar(self, classe, intervalos, inter1, inter2, modelo):

        dst = 'distancias/'+classe+'/'
        pt = open(dst+inter1, 'w')
        for doc in intervalos[inter1]:
            d1 = 'DOC_'+str(doc)
            for doc_viz in intervalos[inter2]:
                d2 = 'DOC_'+str(doc_viz)
                distancia = cosine_similarity(
                    [modelo[d1]], [modelo[d2]])[0][0]
                pt.write(str(doc)+','+str(doc_viz)+','+str(distancia)+'\n')
        pt.close()

    def executar(self, dataset, caminho_modelo):

        df = pd.read_csv(dataset)
        classes = set(df['classe'])
        for classe in classes:
            dst = 'distancias/'+classe+'/'
            if not os.path.exists(dst):
                os.makedirs(dst)

        for classe in classes:
            print("Processando classe: ", classe)
            intervalos = self.agrupar(df[df['classe'] == classe]['date'])
            chaves = list(intervalos.keys())
            chaves.sort()
            # Comparando os documentos de uma semana com a próxima.
            index = 0
            max_p = 15
            processos = list()
            modelo = Doc2Vec.load(caminho_modelo)
            while index < (len(chaves)-1):
                processos = list(filter(lambda x: x.is_alive(), processos))
                if len(processos) == max_p:
                    time.sleep(0.5)
                else:
                    p = mp.Process(name=str(index), target=self.comparar,
                                   args=(classe, intervalos, chaves[index], chaves[index+1], modelo))
                    processos.append(p)
                    p.start()
                    index += 1

            for processo in processos:
                processo.join()


if __name__ == '__main__':

    c = Comparador()
    c.executar(argv[1], argv[2])
