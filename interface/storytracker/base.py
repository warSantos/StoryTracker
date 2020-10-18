import datetime
from dateutil.relativedelta import relativedelta


class Base():

    def queryset_para_json(self, cursor):

        colunas = [i[0] for i in cursor.description]
        queryset = cursor.fetchall()
        json_data = list()
        for tupla in queryset:
            json_data.append(dict(zip(colunas, tupla)))
        return json_data

    # Dado uma data base, essa função retorna outra data M meses e D dias
    # anterior ou posterior a data base.
    def data_relativa(self, data, meses=2, dias=0):

        tokens = data.split('-')

        ano = int(tokens[0])
        mes = int(tokens[1])
        dia = int(tokens[2])
        
        return datetime.date(ano, mes, dia)+relativedelta(months=+meses, days=+dias)


    # Retorna das datas da borda de outra data a partir de um raio M de meses.
    # Ex.: data centro: 2020-01-01, raio M=2 datas bordas são: 2019-011, 2020-03
    def datas_raio(self, data, meses=2, dias=0):

        
        data_ini = self.data_relativa(data, -1*meses, dias)
        data_fim = self.data_relativa(data, meses, dias)

        return data_ini.strftime('%Y-%m-%d'), data_fim.strftime('%Y-%m-%d')
