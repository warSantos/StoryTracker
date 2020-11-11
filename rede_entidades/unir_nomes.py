import os
import json
from Levenshtein import ratio


class UnirNomes():

    def __init__(self):
    
        fd = open('preproc/entidades.json', 'r')
        self.ents = json.load(fd)
        fd.close()

        fd = open('preproc/map_ents.json', 'r')
        self.map_ents = json.load(fd)
        fd.close()

        fd = open('preproc/docs_ents.json', 'r')
        self.docs_ents = json.load(fd)
        fd.close()
        
        fd = open('configs/classes.json', 'r')
        self.classes = json.load(fd)
        fd.close()
    
    def filtro(self, classe, ent):

        if classe == 'PER' and len(ent) > 3 and len(self.ents[ent]) > 50:
            return True
        return False

    # Unindo nomes por documento.
    def unir_nomes(self):

        # Para cada documento.
        for doc in self.docs_ents:
            print("NOVO DOC: ",'*'*70)
            ents_delete = []
            ents = list(doc[2].keys())
            ents.sort(key=lambda x: len(x))
            i = 0
            len_ents = len(ents)
            # Para cada entidade.
            while i < len_ents:
                ids = []
                # Se a classe dela for de uma pessoa.
                if self.filtro(doc[2][ents[i]][0], ents[i]):
                    j = i + 1
                    # Para as demais entidades.
                    while j < len_ents:
                        if self.filtro(doc[2][ents[j]][0], ents[j]):
                            if ents[j].find(ents[i]) > 0:
                                ids.append(j)
                                print("Matching: ", ents[i],",", \
                                    doc[2][ents[i]][1],",", \
                                    len(self.ents[ents[i]]),",", \
                                    ents[j],",", \
                                    doc[2][ents[j]][1],",", \
                                    len(self.ents[ents[j]]))
                        else:
                            #print("ORG: ", ents[j], doc[2][ents[j]])
                            ents_delete.append(ents[j])
                        j += 1
                    
                    # Unindo as entidades.
                    if ids:
                        quant = -1
                        index = -1
                        for id_ent in ids:
                            if quant < len(self.ents[ents[id_ent]]):
                                quant = len(self.ents[ents[id_ent]])
                                index = id_ent
                        
                        # Atualizando a quantidade de aparições da entidade acolhedora no documento.
                        doc[2][ents[index]][1] += doc[2][ents[i]][1]
                        # Atualizando na lista de entidades a serem removidas.
                        ents_delete.append(ents[i])
                        print(ents[i], len(self.ents[ents[i]]), "Foi para ->: ", ents[index], len(self.ents[ents[index]]))
                else:
                    ents_delete.append(ents[i])
                i += 1
            # Removendo as entidades redefinidas.
            for ent in set(ents_delete):
                del doc[2][ent]

    # Unindo os documentos nível global
    def unir_nomes_global(self):
        
        # Unindo todas as entidades em um único dicionário.
        global_ents = {}
        # Para cada documento.
        for doc in self.docs_ents:
            for ent in doc[2]:
                if ent not in global_ents:
                    global_ents[ent] = doc[2][ent]
        
        ents = list(global_ents.keys())
        ents.sort(key=lambda x: len(x))
        
        # Combinando entidades par a par.
        i = 0
        lista_ents = []
        while i < len(ents):
            j = i + 1    
            while j < len(ents):
                #lista_ents.append([ents[i], ents[j], ratio(ents[i], ents[j])])
                if ents[j].find(ents[i]) > -1:
                    print(ents[i],ents[j])
                j += 1
            i += 1
        

if __name__=='__main__':

    u = UnirNomes()
    u.unir_nomes()
    u.unir_nomes_global()