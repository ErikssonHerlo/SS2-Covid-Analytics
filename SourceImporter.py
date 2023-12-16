import requests
import pandas as pd
from io import StringIO
from urllib.error import HTTPError
def __init__(self,url):
        self.url=url

    # Método de la clase
    def get_csv_file(self):
        try:
            #response = requests.get(self.url)
            data = pd.read_csv(self.url, low_memory=False)

            print('Archivo CSV leido exitosamente...')
            return data
        except HTTPError as error:
            print(f'Error HTTP al intentar acceder a la URL: {error}')
            return data
        except URLError as error:
            print(f'Error de URL: {error}')
            data = ""
            return data
        except ParserError as error:
            print(f'Error al analizar el archivo CSV: {error}')
            data = ""
            return data
        except Exception as error:
            print(f'Otro error: {error}')
            data = ""
            return data

def request_file(url):
    """Request a file from a URL and return the contents as a string"""
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception("Could not download file from %s" % url)
    return response.content.decode('utf-8')
