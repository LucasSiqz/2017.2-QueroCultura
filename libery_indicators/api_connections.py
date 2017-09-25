import requests, json
#from datetime import datetime, timedelta

class RequestLibraryRawData(object):
    def __init__(self, last_update_time):
        self._get_time = last_update_time
        self._url = 'http://bibliotecas.cultura.gov.br/api/space/find/'
        self._filters = {'@select' : 'En_Estado, esfera, esfera_tipo, terms, createTimestamp', 'createTimestamp' : "GT("+self._get_time+")"}
        self._response = requests.get(self._url, self._filters)
        self._data = json.loads(self._response.text)

    @property
    def response(self):
        return self._response

    @property
    def data(self):
        return self._data

    @property
    def data_length(self):
        return len(self._data)

'''
#Código para testar o funcionamento da classe.
get_time = datetime.now() - timedelta(days=50)
museu = RequestLibraryRawData(get_time.__str__())
print(museu.data[1])
print(museu.data_length)
'''
