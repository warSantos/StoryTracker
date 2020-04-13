from django.db import models
import sys
from gensim.models.doc2vec import Doc2Vec

sys.path.append('../database')
import utils
# Create your models here.

#m_texto = '../modelos/modelos/doc2vec.text_0_100_10'
#modelo_texto = Doc2Vec.load(m_texto)
m_titulo = '../modelos/modelos/doc2vec.classificados_title_0_100_10'
modelo_titulo = Doc2Vec.load(m_titulo)

class PageRanking(models.Model):

    def ranking(self, texto, data):
        
        conn = utils.Utils().conectar()
        cursor = conn.cursor()
        vetor = modelo_titulo.infer_vector(texto.split())
        documentos = modelo_titulo.wv.most_similar(vetor)
        conn.close()