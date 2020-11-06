import os
import json


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
    
    def filtro(self, classe):

        if classe == 'PER':
            return True
        return False

    def unir_nomes(self):

        # Unindo nomes por documento.
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
                if self.filtro(doc[2][ents[i]][0]):
                    j = i + 1
                    # Para as demais entidades.
                    while j < len_ents:
                        if self.filtro(doc[2][ents[j]][0]) and \
                            ents[j].find(ents[i]) > 0:
                            ids.append(j)
                            print("Matching: ", ents[i],",", \
                                doc[2][ents[i]][1],",", \
                                len(self.ents[ents[i]]),",", \
                                ents[j],",", \
                                doc[2][ents[j]][1],",", \
                                len(self.ents[ents[j]]))
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
                i += 1
            # Removendo as entidades redefinidas.
            for ent in ents_delete:
                del doc[2][ent]

if __name__=='__main__':

    u = UnirNomes()
    u.unir_nomes()