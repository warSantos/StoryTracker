import os
import json
import igraph
from igraph import Graph


class Rede():

    def __init__(self):

        # Se o grafo já existir carregue-o.
        if os.path.exists('redes/rede.gml'):
            self.rede = igraph.read('redes/rede.gml')
        # Se o grafo não existir.
        else:
            fd = open('preproc/entidades_exemplo.json', 'r')
            self.ents = json.load(fd)
            fd.close()

            fd = open('preproc/map_ents_exemplo.json', 'r')
            self.map_ents = json.load(fd)
            fd.close()

            fd = open('preproc/docs_ents_exemplo.json', 'r')
            self.docs_ents = json.load(fd)
            fd.close()
            
            fd = open('configs/classes.json', 'r')
            self.classes = json.load(fd)
            fd.close()
            
            self.rede = self.construir_rede()
            
    def filtro(self, ent, classe):
        
        # Se for uma classe válida e a entidade estiver associada
        # a mais de N documentos.
        if classe in self.classes and len(list(self.ents[ent])) > 80:
            return True
        return False
            

    def construir_rede(self):

        d_arestas = {}
        d_vertices = {}
        # Para cada documento.
        for doc in self.docs_ents:
            # Para cada entidade no documento.
            ents = list(doc[2].keys())
            ents.sort()
            i = 0
            while i < len(ents):
                # Se a entidade tiver uma classe válida e estiver em mais de N
                # documentos.
                if self.filtro(ents[i], doc[2][ents[i]][0]):
                    j = i + 1
                    # Combinando o documento i com os demais documentos.
                    while j < len(ents):
                        if self.filtro(ents[j], doc[2][ents[j]][0]):
                            chave = ents[i]+'|'+ents[j]
                            if chave not in d_arestas:
                                d_arestas[chave] = 0
                            d_arestas[chave] += 1
                        j += 1
                    # Capturando as entidades de forma única.
                    if ents[i] not in d_vertices:
                        d_vertices[ents[i]] = True
                i += 1
        comb_arestas = list(d_arestas.keys())
        comb_arestas.sort()
        vertices = list(d_vertices.keys())
        vertices.sort()
        # Criando o grafo.
        rede = Graph()
        # Adicionando os vértices no grafo com os labels.
        rede.add_vertices(len(vertices))
        index = 0
        for v in vertices:
            # Mapeando o dicionário para as arestas.
            d_vertices[v] = index
            # Adicionando label no vértice.
            rede.vs[index]["id"] = index
            rede.vs[index]["label"] = v
            index += 1

        arestas = []
        pesos = []
        # Adicionando arestas no grafo.
        for aresta in comb_arestas:
            v1, v2 = aresta.split('|')
            ind_v1 = d_vertices[v1]
            ind_v2 = d_vertices[v2]
            arestas.append((ind_v1, ind_v2))
            pesos.append(d_arestas[aresta])
        
        rede.add_edges(arestas)
        rede.es["weight"] = pesos
        rede.es["label"] = pesos

        # Imprimindo o grafo.
        cont = 0
        for i in rede.degree():
            rede.vs[cont]["size"] = 7+i*1.5
            cont += 1

        layout = rede.layout_kamada_kawai()
        #layout = rede.layout_lgl()
        igraph.plot(rede,"plots/rede.pdf", layout=layout, bbox = (2500, 2500))
        return rede


if __name__ == '__main__':

    r = Rede()